import asyncio
import logging
from datetime import datetime, timedelta
from typing import Callable, Optional, final

import aiohttp
from dateutil.tz import tzutc

from . import api, models

_LOGGER = logging.getLogger(__name__)


def _to_kmh(value: float) -> float:
    """Convert a value in knots to kilometers per hour."""

    return value * 1.85200


@final
class Account:
    """
    An `Account` instance is responsible for accessing devices and providing
    updates.
    """

    _devices: dict[int, models.Device]
    _positions: dict[int, models.Position]
    _subscriptions: dict[str, models.Subscription]
    _trips: dict[str, dict[tuple[datetime, datetime], models.Trip]]
    _sorted_trips: dict[str, list[models.Trip]]

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
        self._sorted_trips = {}

        self._update_task = None

    async def update_devices(self) -> None:
        _LOGGER.debug("Updating devices")

        self._devices = {
            device.id: device for device in await self.traccar_api.get_devices()
        }

    def start(self, on_update: Callable[[], None] = None) -> None:
        """Start the update task.

        Args:
            on_update: Callback to invoke on an update. Defaults to None.
        """

        _LOGGER.debug("Starting the websocket task.")

        if self._update_task is None:
            self._update_task = asyncio.create_task(self.update_task(on_update))

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
                    "Client error while reading from websocket, error counter is %d.",
                    errors,
                    exc_info=e,
                )

                if self._update_task is not None:
                    _LOGGER.debug("Adding exponential backoff delay.")

                    errors += 1
                    await asyncio.sleep(2.0 ** max(errors, 6))
            except Exception as e:
                _LOGGER.exception(
                    "Unhandled exception while reading from websocket.",
                    errors,
                    exc_info=e,
                )

                raise

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
    retrieves the latest version of the data from an `Account` instance using a
    device identifier.
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
        _LOGGER.debug("Updating positions of device %s", self._id)

        self._account._positions[
            self._id
        ] = await self._account.traccar_api.get_position(
            self._id, self._device.position_id
        )

    async def update_subscription(self) -> None:
        """
        Update the subscription information of the device.
        """
        _LOGGER.debug("Updating subscription of device %s", self._id)

        self._account._subscriptions[
            self._id
        ] = await self._account.admin_api.get_subscription(self._device.unique_id)

    async def update_trips(
        self, from_date: datetime = None, to_date: datetime = None
    ) -> None:
        """
        Update the trips information of the device.

        Args:
            from_date: The from filter.
            to_date: The to filter.

        Raises:
            ValueError: if the `from_date` or `to_date` do not include timezone
                information.
        """

        _LOGGER.debug("Updating trips of device %s", self._id)

        if to_date is None:
            to_date = datetime.now(tzutc())

        if from_date is None:
            from_date = to_date - timedelta(days=7)

        trips = await self._account.traccar_api.get_trips(self._id, from_date, to_date)

        if self._id not in self._account._trips:
            self._account._trips[self._id] = {}

        self._account._trips[self._id].update(
            {(trip.start_time, trip.end_time): trip for trip in trips}
        )
        self._account._sorted_trips[self._id] = sorted(
            self._account._trips[self._id].values(), key=lambda t: t.start_time
        )

    async def set_guarded(self, guarded: bool) -> None:
        _LOGGER.debug("Setting guarded state of device %s to %s", self._id, guarded)

        if guarded:
            await self._account.admin_api.post_arm(self._device.unique_id)
        else:
            await self._account.admin_api.post_disarm(self._device.unique_id)

        # Update guarded state optimistically.
        self._device.attributes.guarded = guarded

    async def set_stolen(self, stolen: bool) -> None:
        _LOGGER.debug("Setting stolen state of device %s to %s", self._id, stolen)

        device = models.Device.from_dict(self._device.to_dict())

        device.attributes.stolen = stolen

        self._account._devices[self._id] = await self._account.traccar_api.put_device(
            self._id, device
        )

    async def set_tracking_enabled(self, tracking_enabled: bool) -> None:
        _LOGGER.debug(
            "Setting tracking enabled state of device %s to %s",
            self._id,
            tracking_enabled,
        )

        device = models.Device.from_dict(self._device.to_dict())

        device.disabled = not tracking_enabled

        self._account._devices[self._id] = await self._account.traccar_api.put_device(
            self._id, device
        )

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
    def _trips(self) -> dict[tuple[datetime, datetime], models.Trip]:
        """
        Get the trips as dictionary.
        """
        return self._account._trips.get(self._id, {})

    @property
    def _sorted_trips(self) -> list[models.Trip]:
        """
        Get the trips sorted by start time.
        """
        return self._account._sorted_trips.get(self._id, [])

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._device.name

    @property
    def is_deleted(self) -> bool:
        return self._device is None

    @property
    def is_alarm_triggered(self) -> Optional[bool]:
        return self._device.attributes.alarm

    @property
    def is_tracking_enabled(self) -> bool:
        return not self._device.disabled

    @property
    def is_stolen(self) -> Optional[bool]:
        return self._device.attributes.stolen

    @property
    def is_guarded(self) -> Optional[bool]:
        return self._device.attributes.guarded

    @property
    def is_auto_guarded(self) -> Optional[bool]:
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
    def speed(self) -> Optional[float]:
        if not self._position:
            return None

        return _to_kmh(self._position.speed)

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
    def trips(self) -> list["Trip"]:
        return [
            Trip(self, (trip.start_time, trip.end_time)) for trip in self._sorted_trips
        ]


@final
class Trip:
    """
    A `Trip` instance is a view of `models.Trip`. It retrieves the latest
    version of the data from a `Device` instance using a key that consists of
    the start time and end time of a trip.
    """

    # Device instance.
    _device: Device

    # Trip unique key.
    _key: tuple[datetime, datetime]

    def __init__(self, device: Device, key: tuple[datetime, datetime]) -> None:
        """Construct a new instance.

        Args:
            device: The `Device` instance.
            key: The unique key of the instance.
        """
        self._device = device
        self._key = key

    @property
    def _trip(self) -> models.Trip:
        """
        Get the trip.
        """
        return self._device._trips[self._key]

    @property
    def key(self) -> tuple[datetime, datetime]:
        return self._key

    @property
    def is_deleted(self) -> bool:
        return self._trip is None

    @property
    def distance(self) -> float:
        return self._trip.distance

    @property
    def duration(self) -> timedelta:
        return timedelta(milliseconds=self._trip.duration)

    @property
    def end_latitude(self) -> float:
        return self._trip.end_lat

    @property
    def end_longitude(self) -> float:
        return self._trip.end_lon

    @property
    def end_odometer(self) -> float:
        return self._trip.end_odometer

    @property
    def end_time(self) -> datetime:
        return self._trip.end_time

    @property
    def average_speed(self) -> float:
        return _to_kmh(self._trip.average_speed)

    @property
    def max_speed(self) -> float:
        return _to_kmh(self._trip.max_speed)

    @property
    def start_latitude(self) -> float:
        return self._trip.start_lat

    @property
    def start_longitude(self) -> float:
        return self._trip.start_lon

    @property
    def start_odometer(self) -> float:
        return self._trip.start_odometer

    @property
    def start_time(self) -> datetime:
        return self._trip.start_time
