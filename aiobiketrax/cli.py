import argparse
import asyncio
import pprint
import sys

import aiohttp

from .client import Account, Device


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=argv[0])

    parser.add_argument(
        "-u", "--username", action="store", required=True, help="username for login"
    )
    parser.add_argument(
        "-p", "--password", action="store", required=True, help="password for login"
    )

    sub_parsers = parser.add_subparsers(dest="command", help="command to execute")

    sub_parsers.add_parser("devices", help="display all devices")

    sub_parsers.add_parser("stream", help="stream device updates")

    # Parse command line
    return parser.parse_args(argv[1:])


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


def device_to_dict(device: Device) -> dict[str, any]:
    """Lazy-man's approach to convert a `Device` to a `dict`."""

    result = {}

    for key in dir(device):
        if key.startswith("_"):
            continue

        attr = getattr(device, key)

        if callable(attr):
            continue

        if attr is None:
            continue

        result[key] = attr

    return result


async def main(argv: list[str]) -> int:
    """Application entry point."""

    arguments = parse_arguments(argv)

    if arguments.command == "devices":
        await command_devices(arguments)
    elif arguments.command == "stream":
        await command_stream(arguments)

    return 0


def run():
    """Script entry point"""
    sys.exit(asyncio.run(main(sys.argv)))


if __name__ == "__main__":
    run()
