# Changelog

## v1.3.1
Released 5 August 2024

Highlights:
* Fixed: do not pin aiohttp version.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v1.3.0...v1.3.1).

## v1.3.0
Released 14 May 2024

Highlights:
* Addded: expose unique identifier of device.
* Added: support the double battery option.
* Fixed: tracking state could not be updated.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v1.2.0...v1.3.0).

## v1.2.0
Released 13 May 2024

Highlights:
* Fixed: API incompatibility on geofenceIds.
* Upgraded: Python 3.12 compatibility.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v1.1.2...v1.2.0).

## v1.1.2
Released 1 January 2024

Highlights:
* Fixed: addonIds is a string

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v1.1.1...v1.1.2).

This release supersedes v1.1.2a1.

## v1.1.1
Released 28 August 2023

Hightlights:
* Fixed: include 'Accept' header in JSON request (fixes trips endpoint).
* Fixed: allow 'setupFee' property to be an integer as well.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v1.1.0...v1.1.1).

## v1.1.0
Released 28 June 2023

Hightlights:
* Fixed: subscription end date for B2B subscriptions.
* Added: addon identifiers.
* Upgraded: model generator.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v1.0.0...v1.1.0).

## v1.0.0
Released 12 June 2023

Highlights:
* Added: estimated battery level (similar to the app).
* Added: missing properties (fwVersion and gpsDisabled).
* Improved: upgraded dependencies.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v0.5.0...v1.0.0).

## v0.5.0
Released 09 December 2022

Highlights:
* Fixed: WebSocket not reconnecting on ClientResponseError.
* Improved: upgraded dependencies.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v0.4.0...v0.5.0).

## v0.4.0
Released 23 October 2022

Highlights:
* Added: expose 'geofence_radius' and 'guard_type'.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v0.3.0...v0.4.0).

## v0.3.0
Released 16 October 2022

Highlights:
* Fixed: setup fee is a boolean.
* Fixed: trial end is optional.
* Added: add support for exceptions (see `exceptions.py`).
* Added: configure heartbeat for WebSocket.
* Improved: WebSocket message handling.
* Improved: additional debug logging.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v0.2.1...v0.3.0).

This release supersedes v0.2.2a1.

## v0.2.1
Released 25 August 2022

Highlights:
* Fixed: exponential backoff for websocket disconnects.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v0.2.0...v0.2.1).

## v0.2.0
Released 10 August 2022

Highlights:
* Added: support for retrieving trips.
* Improvement: null-value handing to address deserialization issues (see #16).
* Fixed: speed not in km/h but knots.
* Fixed: guarded state not updating after disarming.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/v0.1.0...v0.2.0).

## v0.1.0
Released 8 July 2022

Highlights:
* Initial release.

The full list of commits can be found [here](https://github.com/basilfx/aiobiketrax/compare/e5e9f92e9c91672fa875c00ae4021edcfd61a892...v0.1.0).
