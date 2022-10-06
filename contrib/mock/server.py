import asyncio

from aiohttp import web

DEVICES = [
    {
        "id": 1,
        "attributes": {
            "trialEnd": "2023-06-01T00:00:00.000Z",
            "guarded": False,
            "alarm": False,
            "guardType": "movement",
            "lastAlarm": 1654187403028,
            "passport": {
                "manufacturer": "Gazelle",
                "model": "Ultimate C8",
                "colour": "black",
                "bikeType": "ebike",
                "engine": "bosch",
                "insurance": False,
                "bikePictures": [],
                "receiptPictures": [],
                "frameNumber": "123456789ABC",
                "price": "4000",
            },
            "autoGuard": False,
            "geofenceRadius": 50,
            "stolen": False,
        },
        "groupId": 0,
        "name": "My first e-bike",
        "uniqueId": "123456789ABC",
        "status": "offline",
        "lastUpdate": "2022-06-01T00:00:00.000+00:00",
        "positionId": 1000,
        "geofenceIds": [],
        "phone": None,
        "model": None,
        "contact": None,
        "category": None,
        "disabled": False,
    },
    {
        "id": 2,
        "attributes": {
            "trialEnd": "2023-06-01T00:00:00.000Z",
            "guarded": True,
            "alarm": False,
            "guardType": "movement",
            "lastAlarm": 1654187403028,
            "passport": {
                "manufacturer": "Gazelle",
                "model": "Ultimate C8",
                "colour": "black",
                "bikeType": "ebike",
                "engine": "bosch",
                "insurance": False,
                "bikePictures": [],
                "receiptPictures": [],
                "frameNumber": "123456789ABC",
                "price": "4000",
            },
            "autoGuard": False,
            "geofenceRadius": 50,
            "stolen": False,
        },
        "groupId": 0,
        "name": "My second e-bike",
        "uniqueId": "ABCDEFGHI123",
        "status": "offline",
        "lastUpdate": "2022-06-01T00:00:00.000+00:00",
        "positionId": 2000,
        "geofenceIds": [],
        "phone": None,
        "model": None,
        "contact": None,
        "category": None,
        "disabled": False,
    },
]

POSITIONS = [
    {
        "id": 1000,
        "attributes": {
            "batteryLevel": 100,
            "armed": True,
            "charge": False,
            "ignition": False,
            "status": 1,
            "index": 1,
            "distance": 0.0,
            "totalDistance": 100.0,
            "motion": False,
            "hours": 11034000,
        },
        "deviceId": 1,
        "type": None,
        "protocol": "h02",
        "serverTime": "2022-06-01T00:00:00.000+00:00",
        "deviceTime": "2022-06-01T00:00:00.000+00:00",
        "fixTime": "2022-06-01T00:00:00.000+00:00",
        "outdated": False,
        "valid": True,
        "latitude": 50.00,
        "longitude": 5.0,
        "altitude": 0.0,
        "speed": 0.0,
        "course": 0.0,
        "address": None,
        "accuracy": 0.0,
        "network": None,
    },
    {
        "id": 2000,
        "attributes": {
            "batteryLevel": 100,
            "armed": True,
            "charge": False,
            "ignition": False,
            "status": 1,
            "index": 1,
            "distance": 0.0,
            "totalDistance": 100.0,
            "motion": False,
            "hours": 11034000,
        },
        "deviceId": 2,
        "type": None,
        "protocol": "h02",
        "serverTime": "2022-06-01T00:00:00.000+00:00",
        "deviceTime": "2022-06-01T00:00:00.000+00:00",
        "fixTime": "2022-06-01T00:00:00.000+00:00",
        "outdated": False,
        "valid": True,
        "latitude": 50.00,
        "longitude": 5.0,
        "altitude": 0.0,
        "speed": 0.0,
        "course": 0.0,
        "address": None,
        "accuracy": 0.0,
        "network": None,
    },
]

SESSION = {
    "id": 1,
    "attributes": {
        "sendAnalytics": True,
        "appEnvironment": "cordova-desktop-hybrid",
        "appPackage": "com.powunity.app",
        "appVersion": "web-3.7.0504",
        "fcmTokens": ["token1", "token2", "token3"],
        "locale": "nl",
    },
    "name": "email@example.org",
    "login": None,
    "email": "email@example.org",
    "phone": None,
    "readonly": False,
    "administrator": False,
    "map": None,
    "latitude": 0.0,
    "longitude": 0.0,
    "zoom": 0,
    "twelveHourFormat": False,
    "coordinateFormat": None,
    "disabled": False,
    "expirationTime": None,
    "deviceLimit": -1,
    "userLimit": 0,
    "deviceReadonly": False,
    "token": "token",
    "limitCommands": False,
    "poiLayer": None,
    "password": None,
}

SUBSCRIPTIONS = [
    {
        "trialEnd": "2023-06-01T00:00:00.000Z",
        "subscriptionId": None,
        "category": "B2C",
        "trialDuration": 365,
        "setupFee": None,
        "id": 1,
        "createdAt": "2023-06-01T00:00:00.000Z",
        "updatedAt": "2023-06-01T00:00:00.000Z",
        "uniqueId": "123456789ABC",
    },
    {
        "trialEnd": "2023-06-01T00:00:00.000Z",
        "subscriptionId": None,
        "category": "B2C",
        "trialDuration": 365,
        "setupFee": None,
        "id": 2,
        "createdAt": "2023-06-01T00:00:00.000Z",
        "updatedAt": "2023-06-01T00:00:00.000Z",
        "uniqueId": "ABCDEFGHI123",
    },
]

TRIPS = [
    {
        "deviceId": 1,
        "deviceName": "My first e-bike",
        "distance": 100.0,
        "averageSpeed": 10.0,
        "maxSpeed": 20.0,
        "spentFuel": 0.0,
        "startOdometer": 100.0,
        "endOdometer": 200.0,
        "startTime": "2022-06-01T00:00:00.000+00:00",
        "endTime": "2022-06-01T01:00:00.000+00:00",
        "startPositionId": 1000,
        "endPositionId": 1000,
        "startLat": 50.0,
        "startLon": 5.0,
        "endLat": 50.0,
        "endLon": 5.0,
        "startAddress": None,
        "endAddress": None,
        "duration": 3600000,
        "driverUniqueId": None,
        "driverName": None,
    },
    {
        "deviceId": 2,
        "deviceName": "My second e-bike",
        "distance": 100.0,
        "averageSpeed": 10.0,
        "maxSpeed": 20.0,
        "spentFuel": 0.0,
        "startOdometer": 200.0,
        "endOdometer": 300.0,
        "startTime": "2022-06-01T00:00:00.000+00:00",
        "endTime": "2022-06-01T01:00:00.000+00:00",
        "startPositionId": 2000,
        "endPositionId": 2000,
        "startLat": 50.0,
        "startLon": 5.0,
        "endLat": 50.0,
        "endLon": 5.0,
        "startAddress": None,
        "endAddress": None,
        "duration": 3600000,
        "driverUniqueId": None,
        "driverName": None,
    },
]


def get_subscription(request: web.Request):
    unique_id = request.match_info.get("unique_id")
    subscriptions = [
        subscription
        for subscription in SUBSCRIPTIONS
        if subscription["uniqueId"] == unique_id
    ]

    if not subscriptions:
        return web.Response(status=404)

    return web.json_response(subscriptions[0])


def post_arm(request: web.Request):
    unique_id = request.match_info.get("unique_id")
    devices = [device for device in DEVICES if device["uniqueId"] == unique_id]

    if not devices:
        return web.Response(status=404)

    devices[0]["attributes"]["guarded"] = True

    return web.json_response({})


def post_disarm(request: web.Request):
    unique_id = request.match_info.get("unique_id")
    devices = [device for device in DEVICES if device["uniqueId"] == unique_id]

    if not devices:
        return web.Response(status=404)

    devices[0]["attributes"]["guarded"] = False

    return web.json_response({})


def get_devices(request: web.Request):
    return web.json_response(DEVICES)


def get_device(request: web.Request):
    id = request.match_info.get("id")
    devices = [device for device in DEVICES if device["id"] == int(id)]

    if not devices:
        return web.Response(status=404)

    return web.json_response(devices[0])


async def put_device(request: web.Request):
    id = request.match_info.get("id")
    devices = [device for device in DEVICES if device["id"] == int(id)]

    if not devices:
        return web.Response(status=404)

    data = await request.json()

    devices[0].update(data)

    return web.json_response(devices[0])


def get_positions(request: web.Request):
    device_id = request.query.get("device_id")
    id = request.query.get("id")

    if id:
        positions = [
            position
            for position in POSITIONS
            if position["deviceId"] == int(device_id) and position["id"] == int(id)
        ]

        return web.json_response(positions)

    return web.json_response([])


def post_session(request: web.Request):
    return web.json_response(SESSION)


async def socket(request: web.Request):
    ws = web.WebSocketResponse()

    await ws.prepare(request)

    while not ws.closed:
        await ws.send_json({"devices": DEVICES})

        await asyncio.sleep(60)


def get_trips(request: web.Request):
    device_id = request.query.get("device_id")
    from_date = request.query.get("from")
    to_date = request.query.get("to")

    trips = [trip for trip in TRIPS if trip["deviceId"] == int(device_id)]

    return web.json_response(trips)


if __name__ == "__main__":
    aio_app = web.Application()

    # Admin routes.
    aio_app.router.add_route(
        "GET", "/admin/api/subscriptions/{unique_id}", get_subscription
    )
    aio_app.router.add_route("POST", "/admin/api/devices/{unique_id}/arm", post_arm)
    aio_app.router.add_route(
        "POST", "/admin/api/devices/{unique_id}/disarm", post_disarm
    )

    # Traccar routes.
    aio_app.router.add_route("GET", "/traccar/api/devices", get_devices)
    aio_app.router.add_route("GET", "/traccar/api/devices/{id}", get_device)
    aio_app.router.add_route("PUT", "/traccar/api/devices/{id}", put_device)
    aio_app.router.add_route("GET", "/traccar/api/positions", get_positions)
    aio_app.router.add_route("POST", "/traccar/api/session", post_session)
    aio_app.router.add_route("GET", "/traccar/api/socket", socket)
    aio_app.router.add_route("GET", "/traccar/api/trips", get_trips)

    web.run_app(aio_app, port=5555)
