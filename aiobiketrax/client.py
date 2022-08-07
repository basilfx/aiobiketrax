import asyncio
import logging
from datetime import datetime
from typing import Callable, Optional, final

import aiohttp

from . import api, models

_LOGGER = logging.getLogger(__name__)


@final
class Account:
    """
    An `Account` instance is responsible for accessing devices and providing
    updates.
    """

    _devices: dict[int, models.Device]
    _positions: dict[int, models.Position]
    _subscriptions: dict[str, models.Subscription]
    _trips: dict[int, models.Trip]

    def __init__(
        self, username: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Construct a new instance.

        Args:
            username: The username of the account.
            password: The password of the account.
            session: The HTTP session to use.
        """

        self.identity_api = api.IdentityApi(username, password)
        self.traccar_api = api.TraccarApi(self.identity_api, session)
        self.admin_api = api.AdminApi(self.identity_api, session)

        self._devices = {}
        self._positions = {}
        self._subscriptions = {}
        self._trips = {}

        self._update_task = None

    async def update_devices(self) -> None:
        self._devices = {
            device.id: device
            for device in await self.traccar_api.get_devices()
        }

    def start(self, on_update: Callable[[], None] = None) -> None:
        """Start the update task.

        Args:
            on_update: Callback to invoke on an update. Defaults to None.
        """

        _LOGGER.debug("Starting the websocket task.")

        if self._update_task is None:
            self._update_task = asyncio.create_task(
                self.update_task(on_update)
            )

    async def stop(self) -> None:
        """Stop the update task."""

        _LOGGER.debug("Stopping the websocket task.")

        if self._update_task:
            self._update_task.cancel()
            self._update_task = None

    async def update_task(self, on_update: Callable[[], None] = None):
        """Run the update task and process updates.

        Args:
            on_update: Callback to invoke on an update. Defaults to None.
        """
        errors = 0

        while True:
            _LOGGER.debug("Connecting to websocket.")

            try:
                async for update in self.traccar_api.create_socket():
                    updates = False

                    # Reset number of errors, because it connected and received
                    # a message.
                    errors = 0

                    if isinstance(update, models.Position):
                        self._positions[update.device_id] = update
                        updates = True
                    elif isinstance(update, models.Device):
                        self._devices[update.id] = update
                        updates = True

                    if updates and on_update:
                        on_update()

                _LOGGER.debug("Websocket connection terminated gracefully.")
            except aiohttp.ClientError as e:
                _LOGGER.exception(
                    "Exception while reading from websocket, error counter is %d.",
                    errors,
                    exc_info=e,
                )

                if self._update_task is not None:
                    _LOGGER.debug("Adding exponential backoff delay.")

                    errors += 1
                    asyncio.sleep((8 if errors > 8 else errors) ** 2)

    @property
    def devices(self) -> list["Device"]:
        """
        Return the devices.

        Note: run `Account.update_devices()` first to retrieve the list of
        devices associated with this account.
        """
        return [Device(self, device.id) for device in self._devices.values()]


@final
class Device:
    """
    A `Device` instance is a view of `models.Device` and `models.Position`. It
    retrieves the data from an `Account` instance using a device identifier.
    """

    # Account instance.
    _account: Account

    # Device identifier.
    _id: int

    def __init__(self, account: Account, id: int) -> None:
        """Construct a new instance.

        Args:
            account: The `Account` instance.
            id: The identifier of the device.
        """
        self._account = account
        self._id = id

    async def update_position(self) -> None:
        """
        Update the position information of the device.
        """
        self._account._positions[
            self._id
        ] = await self._account.traccar_api.get_position(
            self._id, self._device.position_id
        )

    async def update_subscription(self) -> None:
        """
        Update the subscription information of the device.
        """
        self._account._subscriptions[
            self._id
        ] = await self._account.admin_api.get_subscription(
            self._device.unique_id
        )

    async def update_trip(self) -> None:
        """
        Update the last trip information of the device. Trip is None, if none is found in the last week.
        """
        self._account._trips[
            self._id
        ] = await self._account.traccar_api.get_trip(self._id)

    async def set_guarded(self, guarded: bool) -> None:
        if guarded:
            await self._account.admin_api.post_arm(self._device.unique_id)
        else:
            await self._account.admin_api.post_disarm(self._device.unique_id)

        # Update guarded state optimistically.
        self._device.attributes.guarded = guarded

    async def set_stolen(self, stolen: bool) -> None:
        device = models.Device.from_dict(self._device.to_dict())

        device.attributes.stolen = stolen

        self._account._devices[
            self._id
        ] = await self._account.traccar_api.put_device(self._id, device)

    async def set_tracking_enabled(self, tracking_enabled: bool) -> None:
        device = models.Device.from_dict(self._device.to_dict())

        device.disabled = not tracking_enabled

        self._account._devices[
            self._id
        ] = await self._account.traccar_api.put_device(self._id, device)

    @property
    def _device(self) -> models.Device:
        """
        Get the device data.
        """
        return self._account._devices.get(self._id)

    @property
    def _position(self) -> Optional[models.Position]:
        """
        Get the position. Can be `None` if no position data is available yet.
        """
        return self._account._positions.get(self._id)

    @property
    def _subscription(self) -> Optional[models.Subscription]:
        """
        Get the subscription. Can be `None` if no subscription data is
        available (yet).
        """
        return self._account._subscriptions.get(self._id)

    @property
    def _trip(self) -> Optional[models.Trip]:
        """Get the trip. Can be `None` if no trip data is available yet."""
        return self._account._trips.get(self._id)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._device.name

    @property
    def is_deleted(self) -> bool:
        return self._id in self._device

    @property
    def is_alarm_triggered(self) -> bool:
        return self._device.attributes.alarm

    @property
    def is_tracking_enabled(self) -> bool:
        return not self._device.disabled

    @property
    def is_stolen(self) -> bool:
        return self._device.attributes.stolen

    @property
    def is_guarded(self) -> bool:
        return self._device.attributes.guarded

    @property
    def is_auto_guarded(self) -> bool:
        return self._device.attributes.auto_guard

    @property
    def latitude(self) -> Optional[float]:
        if not self._position:
            return None

        return self._position.latitude

    @property
    def longitude(self) -> Optional[float]:
        if not self._position:
            return None

        return self._position.longitude

    @property
    def altitude(self) -> Optional[float]:
        if not self._position:
            return None

        return self._position.altitude

    @property
    def accuracy(self) -> Optional[int]:
        if not self._position:
            return None

        return self._position.accuracy

    @property
    def speed(self) -> Optional[int]:
        if not self._position:
            return None

        return self._position.speed

    @property
    def course(self) -> Optional[float]:
        if not self._position:
            return None

        return self._position.course

    @property
    def battery_level(self) -> Optional[float]:
        if not self._position:
            return None

        return self._position.attributes.battery_level

    @property
    def total_distance(self) -> Optional[float]:
        if not self._position:
            return None

        return self._position.attributes.total_distance / 1000.0

    @property
    def subscription_until(self) -> Optional[datetime]:
        if not self._subscription:
            return None

        # TODO: unable to verify, but this will probably will not work for
        # expired trial subscriptions.
        return self._subscription.trial_end

    @property
    def last_updated(self) -> datetime:
        return self._device.last_update

    @property
    def status(self) -> str:
        return self._device.status

    @property
    def trip(self) -> Optional[models.Trip]:
        """Get the trip."""
        return self._trip
