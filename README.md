# aiobiketrax
Python library for interacting with the PowUnity BikeTrax GPS tracker.

[![Linting](https://github.com/basilfx/aiobiketrax/actions/workflows/lint.yml/badge.svg)](https://github.com/basilfx/aiobiketrax/actions/workflows/lint.yml)
[![PyPI version](https://badge.fury.io/py/aiobiketrax.svg)](https://badge.fury.io/py/aiobiketrax)

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

### Known issues
The [schemas](contrib/generator/schema.json) of the models haven been
reversed-engineerd by observing responses for a small number of devices. It is
likely that responses of other devices do not map onto the current models. For
example, some properties are not set if they have never been configured from
the app.

Please open an issue, and provide some responses so that the schemas can be
improved. Be sure to redact sensitive information, such as locations, unique
identifiers and personal details.

### Debugging
In case of issues, it is possible to enable logging in your application for the
following loggers:

* `aiobiketrax.api` - API logging.
* `aiobiketrax.api.responses` - Additional API response logging.
* `aiobiketrax.api.client` - Client interaction logging.

## Usage

### In code
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

### CLI
For demonstration and testing purposes, one can use the CLI as well. If you
have the package installed, use `biketrax --help` command to get started.

### Mock server
For development, a mock server is included in `contrib/mock/`. Simply run
`server.py` and adapt `aiobiketrax/consts.py` to use other endpoints.

```python
API_TRACCAR_ENDPOINT = "http://localhost:5555/traccar/api"
API_ADMIN_ENDPOINT = "http://localhost:5555/admin/api"
```

Do note that authentication is not mocked.

## Contributing
See the [`CONTRIBUTING.md`](CONTRIBUTING.md) file.

## License
See the [`LICENSE.md`](LICENSE.md) file (MIT license).

## Disclaimer
Use this library at your own risk. I cannot be held responsible for any
damages.

This page and its content is not affiliated with PowUnity.
