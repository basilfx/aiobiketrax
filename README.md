# aiobiketrax
Python library for interacting with the PowUnity BikeTrax GPS tracker.

## Introduction
This library is mainly written to work with a custom component for
Home Assistant.

The [PowUnity BikeTrax](https://powunity.com/) is a GPS tracker for electric
bicycles. It provides real-time updates every when the bike is in motion, using
a 2G modem. It works in Europe, and requires a subscription after a trial
period of one year.

### Features
* Multi-device support.
* Traccar and admin API support.
* Live updates using websocket.

Not implemented:

* Geofencing.
* Global configuration, such as webhooks.

## Usage
```python
from aiobiketrax import Account

import aiohttp

async with aiohttp.ClientSession() as session:
    account = Account(
        username="someone@example.org",
        password="secret",
        session=session)

    await account.update_devices()

    for device in account.devices:
        print(device.name)
```

## Contributing
To contribute to this repository, use GitHub pull-requests.

- Dependencies are managed using [poetry](https://python-poetry.org/).
- Code is formatted using [black](https://github.com/psf/black).
- Your branch is linear (rebase) and logical.

The models have been generated using [quicktype](https://quicktype.io/). See
the `contrib/generator/` folder for more information.

## License
See the `[LICENSE](LICENSE.md)` file (MIT license).

## Disclaimer
Use this library at your own risk. I cannot be held responsible for any
damages.

This page and its content is not affiliated with PowUnity.