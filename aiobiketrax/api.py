import logging
from datetime import datetime
from decimal import InvalidOperation
from typing import Any, AsyncIterable, Optional, Union

import aiohttp
import jwt
from auth0.v3.asyncify import asyncify
from auth0.v3.authentication import Database
from dateutil.tz import tzutc

from . import models
from .consts import API_ADMIN_ENDPOINT, API_CLIENT_ID, API_TRACCAR_ENDPOINT

_LOGGER = logging.getLogger(__name__)
_RESPONSE_LOGGER = logging.getLogger(__name__ + ".responses")

AsyncDatabase = asyncify(Database)


def _to_isoformat(value: datetime) -> str:
    """Format a `datetime` into a properly formatted timestamp for API usage.

    Args:
        value: The input timestamp.

    Returns:
        An ISO-formatted timestamp, expressed as UTC.

    Raises:
        ValueError: The input value is not timezone-aware.
    """

    if value.tzinfo is None:
        raise ValueError("Timezone information is missing from input value.")

    return (
        value.astimezone(tzutc()).isoformat(timespec="seconds").replace("+00:00", "Z")
    )


class IdentityApi:
    """
    Identity client.
    """

    username: str
    password: str

    database: AsyncDatabase
    id_token: Optional[dict[str, Any]]

    def __init__(self, username: str, password: str) -> None:
        """Construct a new instance.

        Args:
            username: The username to login with.
            password: The password.
        """
        self.username = username
        self.password = password

        self.database = AsyncDatabase("powunity.eu.auth0.com")
        self.id_token = None

    async def login(self):
        if self.id_token is not None:
            return

        _LOGGER.debug("Commencing login for '%s'.", self.username)

        response = await self.database.login_async(
            client_id=API_CLIENT_ID,
            username=self.username,
            password=self.password,
            connection="Username-Password-Authentication",
            scope="openid profile email",
        )

        self.id_token = jwt.decode(
            response["id_token"], options={"verify_signature": False}
        )

        _LOGGER.debug("Retrieved JWT token.")

    def logout(self):
        _LOGGER.debug("Logging out for user '%s'.", self.username)

        self.id_token = None

    @property
    def traccar_password(self) -> str:
        """
        Return the password necessary for the Traccar API.
        """

        if self.id_token is None:
            raise InvalidOperation("Not signed in.")

        if "traccarPassword" not in self.id_token:
            raise InvalidOperation("Traccar password is missing.")

        return self.id_token["traccarPassword"]


class TraccarApi:
    """
    API client for the Traccar endpoint.
    """

    def __init__(
        self, identity_api: IdentityApi, session: aiohttp.ClientSession
    ) -> None:
        """Construct a new instance.

        Args:
            identity_api: The identity API.
            session: The HTTP session to use.
        """
        self.identity_api = identity_api
        self.session = session

    async def get_devices(self) -> list[models.Device]:
        """Get all devices.

        Returns:
            A list of devices.
        """
        response = await self._get("devices")

        return [models.device_from_dict(device) for device in response]

    async def get_device(self, id: int) -> models.Device:
        """Get a device by its identifier.

        Args:
            id: The device identifier.

        Returns:
            A device.
        """
        response = await self._get(f"devices/{id}")

        return models.device_from_dict(response)

    async def put_device(self, id: int, device: models.Device) -> models.Device:
        """Update a device.

        Args:
            id: The device identifier.
            device: The updated device.

        Returns:
            The updated device.
        """
        response = await self._put(f"devices/{id}", json=device.to_dict())

        return models.device_from_dict(response)

    async def post_session(self) -> models.Session:
        """Post a session.

        This sets a cookie that is necessary for the WebSocket to connect.

        Returns:
            A session instance.
        """

        await self.identity_api.login()

        response = await self._post(
            "session",
            data=aiohttp.FormData(
                {
                    "email": self.identity_api.username,
                    "password": self.identity_api.traccar_password,
                }
            ),
        )

        return models.session_from_dict(response)

    async def get_positions(
        self, device_id: str, from_date: datetime, to_date: datetime
    ) -> list[models.Position]:
        """Get positions using a filter.

        Args:
            device_id: The filter for device identifier.
            from_date: The from date.
            to_date: The to date.

        Returns:
            A list of positions.

        Raises:
            ValueError: if the `from_date` or `to_date` do not include timezone
                information.
        """

        response = await self._get(
            "positions",
            params={
                "deviceId": device_id,
                "from": _to_isoformat(from_date),
                "to": _to_isoformat(to_date),
            },
        )

        return [models.position_from_dict(position) for position in response]

    async def get_position(self, device_id: str, id: str) -> Optional[models.Position]:
        """Get a position by its identifier.

        Args:
            device_id: The device identifier.
            id: The position identifier.

        Returns:
            The position.
        """

        response = await self._get(
            "positions", params={"device_id": device_id, "id": id}
        )

        # The result is a list, but an object is more appropriate.
        return models.position_from_dict(response[0]) if response else None

    async def get_trips(
        self, device_id: str, from_date: datetime, to_date: datetime
    ) -> list[models.Trip]:
        """Get trips using a filter.

        Args:
            device_id: The filter for device identifier.
            from_date: The from date.
            to_date: The to date.

        Returns:
            A list of trips.

        Raises:
            ValueError: if the `from_date` or `to_date` do not include timezone
                information.
        """
        response = await self._get(
            "reports/trips",
            params={
                "deviceId": device_id,
                "from": _to_isoformat(from_date),
                "to": _to_isoformat(to_date),
            },
        )

        return [models.trip_from_dict(trip) for trip in response]

    async def _get(self, endpoint, params=None) -> dict:
        while True:
            await self.identity_api.login()

            response = await self.session.get(
                f"{API_TRACCAR_ENDPOINT}/{endpoint}",
                auth=aiohttp.BasicAuth(
                    self.identity_api.username,
                    self.identity_api.traccar_password,
                ),
                params=params,
            )

            _LOGGER.debug(
                "GET request to '%s' returned HTTP status code %d.",
                f"{API_TRACCAR_ENDPOINT}/{endpoint}",
                response.status,
            )

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            _RESPONSE_LOGGER.debug(json)

            return json

    async def _post(self, endpoint, data=None, json=None) -> dict:
        while True:
            await self.identity_api.login()

            response = await self.session.post(
                f"{API_TRACCAR_ENDPOINT}/{endpoint}",
                auth=aiohttp.BasicAuth(
                    self.identity_api.username,
                    self.identity_api.traccar_password,
                ),
                data=data,
                json=json,
            )

            _LOGGER.debug(
                "POST request to '%s' returned HTTP status code %d.",
                f"{API_TRACCAR_ENDPOINT}/{endpoint}",
                response.status,
            )

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            _RESPONSE_LOGGER.debug(json)

            return json

    async def _put(self, endpoint, data=None, json=None) -> dict:
        while True:
            await self.identity_api.login()

            response = await self.session.put(
                f"{API_TRACCAR_ENDPOINT}/{endpoint}",
                auth=aiohttp.BasicAuth(
                    self.identity_api.username,
                    self.identity_api.traccar_password,
                ),
                data=data,
                json=json,
            )

            _LOGGER.debug(
                "PUT request to '%s' returned HTTP status code %d.",
                f"{API_TRACCAR_ENDPOINT}/{endpoint}",
                response.status,
            )

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            _RESPONSE_LOGGER.debug(json)

            return json

    async def create_socket(
        self,
    ) -> AsyncIterable[Union[models.Position, models.Device]]:
        """Connect to the websocket.

        Consumes messages until the connection is closed.

        Yields:
            The updated position or device.
        """

        # This will set the cookie necessary for creating a connection.
        await self.post_session()

        # Create a connection and consume all messages until reading is
        # stopped.
        async with self.session.ws_connect(
            f"{API_TRACCAR_ENDPOINT}/socket"
        ) as websocket:
            async for message in websocket:
                _LOGGER.debug("Received WebSocket message.")

                handled = False

                message = message.json()

                _RESPONSE_LOGGER.debug(message)

                if "positions" in message:
                    handled = True

                    for position in message["positions"]:
                        yield models.position_from_dict(position)

                if "devices" in message:
                    handled = True

                    for device in message["devices"]:
                        yield models.device_from_dict(device)

                if not handled:
                    _LOGGER.debug(
                        "Received a WebSocket message that could not be handled."
                    )


class AdminApi:
    """
    API client for the admin endpoint.
    """

    def __init__(
        self, identity_api: IdentityApi, session: aiohttp.ClientSession
    ) -> None:
        """Construct a new instance.

        Args:
            identity_api: The identity API.
            session: The HTTP session to use.
        """

        self.identity_api = identity_api
        self.session = session

    async def post_arm(self, unique_id: str) -> None:
        """Post an arm-alarm request.

        Args:
            unique_id: The unique identifier of the device.
                This is not its regular identifier.
        """
        await self._post_no_response(f"devices/{unique_id}/arm", json={})

    async def post_disarm(self, unique_id: str) -> None:
        """Post a disarm-alarm request.

        Args:
            unique_id: The unique identifier of the device.
                This is not its regular identifier.
        """
        await self._post_no_response(f"devices/{unique_id}/disarm", json={})

    async def get_subscription(self, unique_id: str) -> Optional[models.Subscription]:
        """Get the subscription.

        Args:
            unique_id: The unique identifier of the device.
                This is not its regular identifier.

        Returns:
            The subscription.
        """
        response = await self._get(f"subscriptions/{unique_id}")

        return models.subscription_from_dict(response)

    async def _get(self, endpoint, params=None) -> dict:
        while True:
            await self.identity_api.login()

            response = await self.session.get(
                f"{API_ADMIN_ENDPOINT}/{endpoint}",
                headers={
                    "Username": self.identity_api.username,
                    "Password": self.identity_api.traccar_password,
                },
                params=params,
            )

            _LOGGER.debug(
                "GET request to '%s' returned HTTP status code %d.",
                f"{API_ADMIN_ENDPOINT}/{endpoint}",
                response.status,
            )

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            _RESPONSE_LOGGER.debug(json)

            return json

    async def _post(self, endpoint, data=None, json=None) -> dict:
        while True:
            await self.identity_api.login()

            response = await self.session.post(
                f"{API_ADMIN_ENDPOINT}/{endpoint}",
                headers={
                    "Username": self.identity_api.username,
                    "Password": self.identity_api.traccar_password,
                },
                data=data,
                json=json,
            )

            _LOGGER.debug(
                "POST request to '%s' returned HTTP status code %d.",
                f"{API_ADMIN_ENDPOINT}/{endpoint}",
                response.status,
            )

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            _RESPONSE_LOGGER.debug(json)

            return json

    async def _post_no_response(self, endpoint, data=None, json=None) -> None:
        while True:
            await self.identity_api.login()

            response = await self.session.post(
                f"{API_ADMIN_ENDPOINT}/{endpoint}",
                headers={
                    "Username": self.identity_api.username,
                    "Password": self.identity_api.traccar_password,
                },
                data=data,
                json=json,
            )

            _LOGGER.debug(
                "POST request to '%s' returned HTTP status code %d.",
                f"{API_ADMIN_ENDPOINT}/{endpoint}",
                response.status,
            )

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            return
