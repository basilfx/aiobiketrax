# aiobiketrax
Python library for interacting with the PowUnity BikeTrax GPS tracker.

## Introduction
This library is mainly written to work with a custom component for
Home Assistant. You can find this custom component
[here](https://github.com/basilfx/homeassistant-biketrax).

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
See the ['CONTRIBUTING.md'](CONTRIBUTING.md) file.

## License
See the [`LICENSE.md`](LICENSE.md) file (MIT license).

## Disclaimer
Use this library at your own risk. I cannot be held responsible for any
damages.

This page and its content is not affiliated with PowUnity.