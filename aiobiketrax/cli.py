import argparse
import asyncio
import logging
import pprint
import sys

import aiohttp

from .client import Account, Device, Trip


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=argv[0])

    parser.add_argument(
        "-u", "--username", action="store", required=True, help="username for login"
    )
    parser.add_argument(
        "-p", "--password", action="store", required=True, help="password for login"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable debug logging"
    )

    sub_parsers = parser.add_subparsers(dest="command", help="command to execute")

    _ = sub_parsers.add_parser("devices", help="display all devices")

    _ = sub_parsers.add_parser("stream", help="stream device updates")

    trips_parser = sub_parsers.add_parser("trips", help="display all devices")

    trips_parser.add_argument(
        "-d",
        "--device-id",
        action="store",
        required=True,
        help="device identifier to retrive trips of",
    )

    # Parse command line
    return parser.parse_args(argv[1:])


def setup_logging() -> None:
    logging.basicConfig(level=logging.DEBUG)


async def command_devices(arguments: argparse.Namespace):
    async with aiohttp.ClientSession() as session:
        account = Account(
            username=arguments.username, password=arguments.password, session=session
        )

        await account.update_devices()

        for device in account.devices:
            await device.update_position()

            sys.stdout.write(pprint.pformat(device_to_dict(device)) + "\n")


async def command_stream(arguments: argparse.Namespace):
    event = asyncio.Event()
    history = {}

    async with aiohttp.ClientSession() as session:
        account = Account(
            username=arguments.username, password=arguments.password, session=session
        )

        account.start(on_update=lambda: event.set())

        try:
            while True:
                await event.wait()

                # Calculate and display any updates to the devices.
                for device in account.devices:
                    current = device_to_dict(device)
                    last = history.get(device.id, {})

                    history[device.id] = current

                    updates = {
                        key: value
                        for key, value in set(current.items()) - set(last.items())
                    }

                    if updates:
                        sys.stdout.write(pprint.pformat(updates) + "\n")

                event.clear()
        finally:
            await account.stop()


async def command_trips(arguments: argparse.Namespace):
    async with aiohttp.ClientSession() as session:
        account = Account(
            username=arguments.username, password=arguments.password, session=session
        )

        await account.update_devices()

        devices = list(
            filter(lambda d: str(d.id) == arguments.device_id, account.devices)
        )

        if not devices:
            sys.stdout.write(
                f"Device with identifier {arguments.device_id} not found.\n"
            )
            return

        device = devices[0]

        await device.update_trips()

        for trip in device.trips:
            sys.stdout.write(pprint.pformat(trip_to_dict(trip)) + "\n")


def device_to_dict(device: Device) -> dict[str, any]:
    return instance_to_dict(device, ["is_deleted", "trips"])


def trip_to_dict(trip: Trip) -> dict[str, any]:
    return instance_to_dict(trip, ["is_deleted", "key"])


def instance_to_dict(instance: object, exclude: list[str]) -> dict[str, any]:
    """Lazy-man's approach to convert an `object` to a `dict`."""

    result = {}

    for key in dir(instance):
        if key.startswith("_"):
            continue

        if key in exclude:
            continue

        attr = getattr(instance, key)

        if callable(attr):
            continue

        if attr is None:
            continue

        result[key] = attr

    return result


async def main(argv: list[str]) -> int:
    """Application entry point."""

    arguments = parse_arguments(argv)

    if arguments.verbose:
        setup_logging()

    if arguments.command == "devices":
        await command_devices(arguments)
    elif arguments.command == "stream":
        await command_stream(arguments)
    elif arguments.command == "trips":
        await command_trips(arguments)

    return 0


def run():
    """Script entry point"""
    sys.exit(asyncio.run(main(sys.argv)))


if __name__ == "__main__":
    run()
