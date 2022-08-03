import logging
import time
from datetime import datetime, timedelta
from decimal import InvalidOperation
from typing import Any, AsyncIterable, Optional, Union

import aiohttp
import jwt
from auth0.v3.asyncify import asyncify
from auth0.v3.authentication import Database

from . import models
from .consts import API_ADMIN_ENDPOINT, API_CLIENT_ID, API_TRACCAR_ENDPOINT

_LOGGER = logging.getLogger(__name__)

# Set to true to enable logging of responses.
LOG_RESPONSES = False

AsyncDatabase = asyncify(Database)


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
        if self.id_token is None:
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

    def logout(self):
        self.id_token = None

    @property
    def traccar_password(self) -> str:
        """
        Return the password necessary for the Traccar API.
        """

        if self.id_token is None:
            raise InvalidOperation("Not signed in.")

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
        """_summary_

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

    async def put_device(
        self, id: int, device: models.Device
    ) -> models.Device:
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
        """

        response = await self._get(
            "positions",
            params={
                "device_id": device_id,
                "from": from_date.isoformat(),
                "to": to_date.isoformat(),
            },
        )

        return [models.position_from_dict(position) for position in response]

    async def get_position(
        self, device_id: str, id: str
    ) -> Optional[models.Position]:
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
        """
        response = await self._get(
            "reports/trips",
            params={
                "deviceId": device_id,
                "from": time.strftime("%Y-%m-%dT%H:%M:%SZ", from_date.timetuple()),
                "to": time.strftime("%Y-%m-%dT%H:%M:%SZ", to_date.timetuple()),
            },
        )

        return [models.trip_from_dict(trip) for trip in response]

    async def get_trip(self, device_id: str) -> models.Trip | None:
        """Get the last trip in the last week or None using a filter.
        Args:
            device_id: The filter for device identifier.
        Returns:
            The last trip in the last week or None.
        """
        trips = await self.get_trips(
            device_id, datetime.now() - timedelta(days=7), datetime.now()
        )
        return trips[-1] if trips else None

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

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()


            if LOG_RESPONSES:
                _LOGGER.debug(json)

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

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            if LOG_RESPONSES:
                _LOGGER.debug(json)

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

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            if LOG_RESPONSES:
                _LOGGER.debug(json)

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

                if LOG_RESPONSES:
                    _LOGGER.debug(message)

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

    async def get_subscription(
        self, unique_id: str
    ) -> Optional[models.Subscription]:
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

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            if LOG_RESPONSES:
                _LOGGER.debug(json)

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

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            json = await response.json()

            if LOG_RESPONSES:
                _LOGGER.debug(json)

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

            if response.status == 401:
                self.identity_api.logout()
                continue

            response.raise_for_status()

            return
