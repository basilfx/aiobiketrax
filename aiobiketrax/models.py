# This file is auto-generated. See the README.md for more information.

# flake8: noqa

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, cast

import dateutil.parser

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


@dataclass
class SessionAttributes:
    app_environment: Optional[str] = None
    app_package: Optional[str] = None
    app_version: Optional[str] = None
    fcm_tokens: Optional[List[str]] = None
    locale: Optional[str] = None
    send_analytics: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "SessionAttributes":
        assert isinstance(obj, dict)
        app_environment = from_union([from_str, from_none], obj.get("appEnvironment"))
        app_package = from_union([from_str, from_none], obj.get("appPackage"))
        app_version = from_union([from_str, from_none], obj.get("appVersion"))
        fcm_tokens = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("fcmTokens")
        )
        locale = from_union([from_str, from_none], obj.get("locale"))
        send_analytics = from_union([from_bool, from_none], obj.get("sendAnalytics"))
        return SessionAttributes(
            app_environment,
            app_package,
            app_version,
            fcm_tokens,
            locale,
            send_analytics,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.app_environment is not None:
            result["appEnvironment"] = from_union(
                [from_str, from_none], self.app_environment
            )
        if self.app_package is not None:
            result["appPackage"] = from_union([from_str, from_none], self.app_package)
        if self.app_version is not None:
            result["appVersion"] = from_union([from_str, from_none], self.app_version)
        if self.fcm_tokens is not None:
            result["fcmTokens"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.fcm_tokens
            )
        if self.locale is not None:
            result["locale"] = from_union([from_str, from_none], self.locale)
        if self.send_analytics is not None:
            result["sendAnalytics"] = from_union(
                [from_bool, from_none], self.send_analytics
            )
        return result


@dataclass
class Session:
    administrator: bool
    attributes: SessionAttributes
    device_limit: int
    device_readonly: bool
    disabled: bool
    email: str
    id: int
    latitude: float
    limit_commands: bool
    longitude: float
    name: str
    readonly: bool
    token: str
    twelve_hour_format: bool
    user_limit: int
    zoom: int
    coordinate_format: Optional[str] = None
    expiration_time: Optional[datetime] = None
    login: Optional[str] = None
    map: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    poi_layer: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Session":
        assert isinstance(obj, dict)
        administrator = from_bool(obj.get("administrator"))
        attributes = SessionAttributes.from_dict(obj.get("attributes"))
        device_limit = from_int(obj.get("deviceLimit"))
        device_readonly = from_bool(obj.get("deviceReadonly"))
        disabled = from_bool(obj.get("disabled"))
        email = from_str(obj.get("email"))
        id = from_int(obj.get("id"))
        latitude = from_float(obj.get("latitude"))
        limit_commands = from_bool(obj.get("limitCommands"))
        longitude = from_float(obj.get("longitude"))
        name = from_str(obj.get("name"))
        readonly = from_bool(obj.get("readonly"))
        token = from_str(obj.get("token"))
        twelve_hour_format = from_bool(obj.get("twelveHourFormat"))
        user_limit = from_int(obj.get("userLimit"))
        zoom = from_int(obj.get("zoom"))
        coordinate_format = from_union(
            [from_none, from_str], obj.get("coordinateFormat")
        )
        expiration_time = from_union(
            [from_datetime, from_none], obj.get("expirationTime")
        )
        login = from_union([from_none, from_str], obj.get("login"))
        map = from_union([from_none, from_str], obj.get("map"))
        password = from_union([from_none, from_str], obj.get("password"))
        phone = from_union([from_none, from_str], obj.get("phone"))
        poi_layer = from_union([from_none, from_str], obj.get("poiLayer"))
        return Session(
            administrator,
            attributes,
            device_limit,
            device_readonly,
            disabled,
            email,
            id,
            latitude,
            limit_commands,
            longitude,
            name,
            readonly,
            token,
            twelve_hour_format,
            user_limit,
            zoom,
            coordinate_format,
            expiration_time,
            login,
            map,
            password,
            phone,
            poi_layer,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["administrator"] = from_bool(self.administrator)
        result["attributes"] = to_class(SessionAttributes, self.attributes)
        result["deviceLimit"] = from_int(self.device_limit)
        result["deviceReadonly"] = from_bool(self.device_readonly)
        result["disabled"] = from_bool(self.disabled)
        result["email"] = from_str(self.email)
        result["id"] = from_int(self.id)
        result["latitude"] = to_float(self.latitude)
        result["limitCommands"] = from_bool(self.limit_commands)
        result["longitude"] = to_float(self.longitude)
        result["name"] = from_str(self.name)
        result["readonly"] = from_bool(self.readonly)
        result["token"] = from_str(self.token)
        result["twelveHourFormat"] = from_bool(self.twelve_hour_format)
        result["userLimit"] = from_int(self.user_limit)
        result["zoom"] = from_int(self.zoom)
        result["coordinateFormat"] = from_union(
            [from_none, from_str], self.coordinate_format
        )
        result["expirationTime"] = from_union(
            [lambda x: x.isoformat(), from_none], self.expiration_time
        )
        result["login"] = from_union([from_none, from_str], self.login)
        result["map"] = from_union([from_none, from_str], self.map)
        result["password"] = from_union([from_none, from_str], self.password)
        result["phone"] = from_union([from_none, from_str], self.phone)
        result["poiLayer"] = from_union([from_none, from_str], self.poi_layer)
        return result


@dataclass
class Subscription:
    category: str
    created_at: datetime
    id: int
    unique_id: str
    updated_at: datetime
    addon_ids: Optional[List[str]] = None
    setup_fee: Optional[bool] = None
    subscription_id: Optional[str] = None
    trial_duration: Optional[int] = None
    trial_end: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> "Subscription":
        assert isinstance(obj, dict)
        category = from_str(obj.get("category"))
        created_at = from_datetime(obj.get("createdAt"))
        id = from_int(obj.get("id"))
        unique_id = from_str(obj.get("uniqueId"))
        updated_at = from_datetime(obj.get("updatedAt"))
        addon_ids = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("addonIds")
        )
        setup_fee = from_union([from_bool, from_none], obj.get("setupFee"))
        subscription_id = from_union([from_none, from_str], obj.get("subscriptionId"))
        trial_duration = from_union([from_int, from_none], obj.get("trialDuration"))
        trial_end = from_union([from_datetime, from_none], obj.get("trialEnd"))
        return Subscription(
            category,
            created_at,
            id,
            unique_id,
            updated_at,
            addon_ids,
            setup_fee,
            subscription_id,
            trial_duration,
            trial_end,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["category"] = from_str(self.category)
        result["createdAt"] = self.created_at.isoformat()
        result["id"] = from_int(self.id)
        result["uniqueId"] = from_str(self.unique_id)
        result["updatedAt"] = self.updated_at.isoformat()
        if self.addon_ids is not None:
            result["addonIds"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.addon_ids
            )
        result["setupFee"] = from_union([from_bool, from_none], self.setup_fee)
        result["subscriptionId"] = from_union(
            [from_none, from_str], self.subscription_id
        )
        if self.trial_duration is not None:
            result["trialDuration"] = from_union(
                [from_int, from_none], self.trial_duration
            )
        result["trialEnd"] = from_union(
            [lambda x: x.isoformat(), from_none], self.trial_end
        )
        return result


@dataclass
class Trip:
    average_speed: float
    device_id: int
    device_name: str
    distance: float
    duration: int
    end_lat: float
    end_lon: float
    end_odometer: float
    end_position_id: int
    end_time: datetime
    max_speed: float
    spent_fuel: float
    start_lat: float
    start_lon: float
    start_odometer: float
    start_position_id: int
    start_time: datetime
    driver_name: Optional[str] = None
    driver_unique_id: Optional[int] = None
    end_address: Optional[str] = None
    start_address: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Trip":
        assert isinstance(obj, dict)
        average_speed = from_float(obj.get("averageSpeed"))
        device_id = from_int(obj.get("deviceId"))
        device_name = from_str(obj.get("deviceName"))
        distance = from_float(obj.get("distance"))
        duration = from_int(obj.get("duration"))
        end_lat = from_float(obj.get("endLat"))
        end_lon = from_float(obj.get("endLon"))
        end_odometer = from_float(obj.get("endOdometer"))
        end_position_id = from_int(obj.get("endPositionId"))
        end_time = from_datetime(obj.get("endTime"))
        max_speed = from_float(obj.get("maxSpeed"))
        spent_fuel = from_float(obj.get("spentFuel"))
        start_lat = from_float(obj.get("startLat"))
        start_lon = from_float(obj.get("startLon"))
        start_odometer = from_float(obj.get("startOdometer"))
        start_position_id = from_int(obj.get("startPositionId"))
        start_time = from_datetime(obj.get("startTime"))
        driver_name = from_union([from_none, from_str], obj.get("driverName"))
        driver_unique_id = from_union([from_int, from_none], obj.get("driverUniqueId"))
        end_address = from_union([from_none, from_str], obj.get("endAddress"))
        start_address = from_union([from_none, from_str], obj.get("startAddress"))
        return Trip(
            average_speed,
            device_id,
            device_name,
            distance,
            duration,
            end_lat,
            end_lon,
            end_odometer,
            end_position_id,
            end_time,
            max_speed,
            spent_fuel,
            start_lat,
            start_lon,
            start_odometer,
            start_position_id,
            start_time,
            driver_name,
            driver_unique_id,
            end_address,
            start_address,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["averageSpeed"] = to_float(self.average_speed)
        result["deviceId"] = from_int(self.device_id)
        result["deviceName"] = from_str(self.device_name)
        result["distance"] = to_float(self.distance)
        result["duration"] = from_int(self.duration)
        result["endLat"] = to_float(self.end_lat)
        result["endLon"] = to_float(self.end_lon)
        result["endOdometer"] = to_float(self.end_odometer)
        result["endPositionId"] = from_int(self.end_position_id)
        result["endTime"] = self.end_time.isoformat()
        result["maxSpeed"] = to_float(self.max_speed)
        result["spentFuel"] = to_float(self.spent_fuel)
        result["startLat"] = to_float(self.start_lat)
        result["startLon"] = to_float(self.start_lon)
        result["startOdometer"] = to_float(self.start_odometer)
        result["startPositionId"] = from_int(self.start_position_id)
        result["startTime"] = self.start_time.isoformat()
        result["driverName"] = from_union([from_none, from_str], self.driver_name)
        result["driverUniqueId"] = from_union(
            [from_int, from_none], self.driver_unique_id
        )
        result["endAddress"] = from_union([from_none, from_str], self.end_address)
        result["startAddress"] = from_union([from_none, from_str], self.start_address)
        return result


@dataclass
class Passport:
    bike_pictures: Optional[List[str]] = None
    bike_type: Optional[str] = None
    colour: Optional[str] = None
    engine: Optional[str] = None
    frame_number: Optional[str] = None
    insurance: Optional[bool] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    price: Optional[str] = None
    receipt_pictures: Optional[List[str]] = None
    registration_code: Optional[str] = None
    shifting_system_gears: Optional[str] = None
    shifting_system_manufacturer: Optional[str] = None
    shifting_system_model: Optional[str] = None
    special_features: Optional[str] = None
    used: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "Passport":
        assert isinstance(obj, dict)
        bike_pictures = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("bikePictures")
        )
        bike_type = from_union([from_str, from_none], obj.get("bikeType"))
        colour = from_union([from_str, from_none], obj.get("colour"))
        engine = from_union([from_str, from_none], obj.get("engine"))
        frame_number = from_union([from_str, from_none], obj.get("frameNumber"))
        insurance = from_union([from_bool, from_none], obj.get("insurance"))
        manufacturer = from_union([from_str, from_none], obj.get("manufacturer"))
        model = from_union([from_str, from_none], obj.get("model"))
        price = from_union([from_str, from_none], obj.get("price"))
        receipt_pictures = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("receiptPictures")
        )
        registration_code = from_union(
            [from_str, from_none], obj.get("registrationCode")
        )
        shifting_system_gears = from_union(
            [from_str, from_none], obj.get("shiftingSystemGears")
        )
        shifting_system_manufacturer = from_union(
            [from_str, from_none], obj.get("shiftingSystemManufacturer")
        )
        shifting_system_model = from_union(
            [from_str, from_none], obj.get("shiftingSystemModel")
        )
        special_features = from_union([from_str, from_none], obj.get("specialFeatures"))
        used = from_union([from_bool, from_none], obj.get("used"))
        return Passport(
            bike_pictures,
            bike_type,
            colour,
            engine,
            frame_number,
            insurance,
            manufacturer,
            model,
            price,
            receipt_pictures,
            registration_code,
            shifting_system_gears,
            shifting_system_manufacturer,
            shifting_system_model,
            special_features,
            used,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.bike_pictures is not None:
            result["bikePictures"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.bike_pictures
            )
        if self.bike_type is not None:
            result["bikeType"] = from_union([from_str, from_none], self.bike_type)
        if self.colour is not None:
            result["colour"] = from_union([from_str, from_none], self.colour)
        if self.engine is not None:
            result["engine"] = from_union([from_str, from_none], self.engine)
        if self.frame_number is not None:
            result["frameNumber"] = from_union([from_str, from_none], self.frame_number)
        if self.insurance is not None:
            result["insurance"] = from_union([from_bool, from_none], self.insurance)
        if self.manufacturer is not None:
            result["manufacturer"] = from_union(
                [from_str, from_none], self.manufacturer
            )
        if self.model is not None:
            result["model"] = from_union([from_str, from_none], self.model)
        if self.price is not None:
            result["price"] = from_union([from_str, from_none], self.price)
        if self.receipt_pictures is not None:
            result["receiptPictures"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.receipt_pictures
            )
        if self.registration_code is not None:
            result["registrationCode"] = from_union(
                [from_str, from_none], self.registration_code
            )
        if self.shifting_system_gears is not None:
            result["shiftingSystemGears"] = from_union(
                [from_str, from_none], self.shifting_system_gears
            )
        if self.shifting_system_manufacturer is not None:
            result["shiftingSystemManufacturer"] = from_union(
                [from_str, from_none], self.shifting_system_manufacturer
            )
        if self.shifting_system_model is not None:
            result["shiftingSystemModel"] = from_union(
                [from_str, from_none], self.shifting_system_model
            )
        if self.special_features is not None:
            result["specialFeatures"] = from_union(
                [from_str, from_none], self.special_features
            )
        if self.used is not None:
            result["used"] = from_union([from_bool, from_none], self.used)
        return result


@dataclass
class DeviceAttributes:
    alarm: Optional[bool] = None
    auto_guard: Optional[bool] = None
    fw_version: Optional[str] = None
    geofence_radius: Optional[int] = None
    gps_disabled: Optional[bool] = None
    guarded: Optional[bool] = None
    guard_type: Optional[str] = None
    last_alarm: Optional[int] = None
    passport: Optional[Passport] = None
    stolen: Optional[bool] = None
    trial_end: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> "DeviceAttributes":
        assert isinstance(obj, dict)
        alarm = from_union([from_bool, from_none], obj.get("alarm"))
        auto_guard = from_union([from_bool, from_none], obj.get("autoGuard"))
        fw_version = from_union([from_str, from_none], obj.get("fwVersion"))
        geofence_radius = from_union([from_int, from_none], obj.get("geofenceRadius"))
        gps_disabled = from_union([from_bool, from_none], obj.get("gpsDisabled"))
        guarded = from_union([from_bool, from_none], obj.get("guarded"))
        guard_type = from_union([from_str, from_none], obj.get("guardType"))
        last_alarm = from_union([from_int, from_none], obj.get("lastAlarm"))
        passport = from_union([Passport.from_dict, from_none], obj.get("passport"))
        stolen = from_union([from_bool, from_none], obj.get("stolen"))
        trial_end = from_union([from_datetime, from_none], obj.get("trialEnd"))
        return DeviceAttributes(
            alarm,
            auto_guard,
            fw_version,
            geofence_radius,
            gps_disabled,
            guarded,
            guard_type,
            last_alarm,
            passport,
            stolen,
            trial_end,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.alarm is not None:
            result["alarm"] = from_union([from_bool, from_none], self.alarm)
        if self.auto_guard is not None:
            result["autoGuard"] = from_union([from_bool, from_none], self.auto_guard)
        if self.fw_version is not None:
            result["fwVersion"] = from_union([from_str, from_none], self.fw_version)
        if self.geofence_radius is not None:
            result["geofenceRadius"] = from_union(
                [from_int, from_none], self.geofence_radius
            )
        if self.gps_disabled is not None:
            result["gpsDisabled"] = from_union(
                [from_bool, from_none], self.gps_disabled
            )
        if self.guarded is not None:
            result["guarded"] = from_union([from_bool, from_none], self.guarded)
        if self.guard_type is not None:
            result["guardType"] = from_union([from_str, from_none], self.guard_type)
        if self.last_alarm is not None:
            result["lastAlarm"] = from_union([from_int, from_none], self.last_alarm)
        if self.passport is not None:
            result["passport"] = from_union(
                [lambda x: to_class(Passport, x), from_none], self.passport
            )
        if self.stolen is not None:
            result["stolen"] = from_union([from_bool, from_none], self.stolen)
        if self.trial_end is not None:
            result["trialEnd"] = from_union(
                [lambda x: x.isoformat(), from_none], self.trial_end
            )
        return result


@dataclass
class Device:
    attributes: DeviceAttributes
    disabled: bool
    geofence_ids: List[Any]
    group_id: int
    id: int
    last_update: datetime
    name: str
    position_id: int
    status: str
    unique_id: str
    category: Optional[str] = None
    contact: Optional[str] = None
    model: Optional[str] = None
    phone: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Device":
        assert isinstance(obj, dict)
        attributes = DeviceAttributes.from_dict(obj.get("attributes"))
        disabled = from_bool(obj.get("disabled"))
        geofence_ids = from_list(lambda x: x, obj.get("geofenceIds"))
        group_id = from_int(obj.get("groupId"))
        id = from_int(obj.get("id"))
        last_update = from_datetime(obj.get("lastUpdate"))
        name = from_str(obj.get("name"))
        position_id = from_int(obj.get("positionId"))
        status = from_str(obj.get("status"))
        unique_id = from_str(obj.get("uniqueId"))
        category = from_union([from_none, from_str], obj.get("category"))
        contact = from_union([from_none, from_str], obj.get("contact"))
        model = from_union([from_none, from_str], obj.get("model"))
        phone = from_union([from_none, from_str], obj.get("phone"))
        return Device(
            attributes,
            disabled,
            geofence_ids,
            group_id,
            id,
            last_update,
            name,
            position_id,
            status,
            unique_id,
            category,
            contact,
            model,
            phone,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["attributes"] = to_class(DeviceAttributes, self.attributes)
        result["disabled"] = from_bool(self.disabled)
        result["geofenceIds"] = from_list(lambda x: x, self.geofence_ids)
        result["groupId"] = from_int(self.group_id)
        result["id"] = from_int(self.id)
        result["lastUpdate"] = self.last_update.isoformat()
        result["name"] = from_str(self.name)
        result["positionId"] = from_int(self.position_id)
        result["status"] = from_str(self.status)
        result["uniqueId"] = from_str(self.unique_id)
        result["category"] = from_union([from_none, from_str], self.category)
        result["contact"] = from_union([from_none, from_str], self.contact)
        result["model"] = from_union([from_none, from_str], self.model)
        result["phone"] = from_union([from_none, from_str], self.phone)
        return result


@dataclass
class PositionAttributes:
    alarm: Optional[str] = None
    armed: Optional[bool] = None
    battery_level: Optional[int] = None
    charge: Optional[bool] = None
    distance: Optional[float] = None
    hours: Optional[int] = None
    ignition: Optional[bool] = None
    index: Optional[int] = None
    motion: Optional[bool] = None
    status: Optional[int] = None
    total_distance: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> "PositionAttributes":
        assert isinstance(obj, dict)
        alarm = from_union([from_str, from_none], obj.get("alarm"))
        armed = from_union([from_bool, from_none], obj.get("armed"))
        battery_level = from_union([from_int, from_none], obj.get("batteryLevel"))
        charge = from_union([from_bool, from_none], obj.get("charge"))
        distance = from_union([from_float, from_none], obj.get("distance"))
        hours = from_union([from_int, from_none], obj.get("hours"))
        ignition = from_union([from_bool, from_none], obj.get("ignition"))
        index = from_union([from_int, from_none], obj.get("index"))
        motion = from_union([from_bool, from_none], obj.get("motion"))
        status = from_union([from_int, from_none], obj.get("status"))
        total_distance = from_union([from_float, from_none], obj.get("totalDistance"))
        return PositionAttributes(
            alarm,
            armed,
            battery_level,
            charge,
            distance,
            hours,
            ignition,
            index,
            motion,
            status,
            total_distance,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.alarm is not None:
            result["alarm"] = from_union([from_str, from_none], self.alarm)
        if self.armed is not None:
            result["armed"] = from_union([from_bool, from_none], self.armed)
        if self.battery_level is not None:
            result["batteryLevel"] = from_union(
                [from_int, from_none], self.battery_level
            )
        if self.charge is not None:
            result["charge"] = from_union([from_bool, from_none], self.charge)
        if self.distance is not None:
            result["distance"] = from_union([to_float, from_none], self.distance)
        if self.hours is not None:
            result["hours"] = from_union([from_int, from_none], self.hours)
        if self.ignition is not None:
            result["ignition"] = from_union([from_bool, from_none], self.ignition)
        if self.index is not None:
            result["index"] = from_union([from_int, from_none], self.index)
        if self.motion is not None:
            result["motion"] = from_union([from_bool, from_none], self.motion)
        if self.status is not None:
            result["status"] = from_union([from_int, from_none], self.status)
        if self.total_distance is not None:
            result["totalDistance"] = from_union(
                [to_float, from_none], self.total_distance
            )
        return result


@dataclass
class Position:
    accuracy: float
    altitude: float
    attributes: PositionAttributes
    course: float
    device_id: int
    device_time: datetime
    fix_time: datetime
    id: int
    latitude: float
    longitude: float
    outdated: bool
    protocol: str
    server_time: datetime
    speed: float
    type: None
    valid: bool
    address: Optional[str] = None
    network: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Position":
        assert isinstance(obj, dict)
        accuracy = from_float(obj.get("accuracy"))
        altitude = from_float(obj.get("altitude"))
        attributes = PositionAttributes.from_dict(obj.get("attributes"))
        course = from_float(obj.get("course"))
        device_id = from_int(obj.get("deviceId"))
        device_time = from_datetime(obj.get("deviceTime"))
        fix_time = from_datetime(obj.get("fixTime"))
        id = from_int(obj.get("id"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        outdated = from_bool(obj.get("outdated"))
        protocol = from_str(obj.get("protocol"))
        server_time = from_datetime(obj.get("serverTime"))
        speed = from_float(obj.get("speed"))
        type = from_none(obj.get("type"))
        valid = from_bool(obj.get("valid"))
        address = from_union([from_none, from_str], obj.get("address"))
        network = from_union(
            [from_none, lambda x: from_dict(lambda x: x, x)], obj.get("network")
        )
        return Position(
            accuracy,
            altitude,
            attributes,
            course,
            device_id,
            device_time,
            fix_time,
            id,
            latitude,
            longitude,
            outdated,
            protocol,
            server_time,
            speed,
            type,
            valid,
            address,
            network,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["accuracy"] = to_float(self.accuracy)
        result["altitude"] = to_float(self.altitude)
        result["attributes"] = to_class(PositionAttributes, self.attributes)
        result["course"] = to_float(self.course)
        result["deviceId"] = from_int(self.device_id)
        result["deviceTime"] = self.device_time.isoformat()
        result["fixTime"] = self.fix_time.isoformat()
        result["id"] = from_int(self.id)
        result["latitude"] = to_float(self.latitude)
        result["longitude"] = to_float(self.longitude)
        result["outdated"] = from_bool(self.outdated)
        result["protocol"] = from_str(self.protocol)
        result["serverTime"] = self.server_time.isoformat()
        result["speed"] = to_float(self.speed)
        result["type"] = from_none(self.type)
        result["valid"] = from_bool(self.valid)
        result["address"] = from_union([from_none, from_str], self.address)
        result["network"] = from_union(
            [from_none, lambda x: from_dict(lambda x: x, x)], self.network
        )
        return result


@dataclass
class WebSocketUpdate:
    devices: Optional[List[Device]] = None
    positions: Optional[List[Position]] = None

    @staticmethod
    def from_dict(obj: Any) -> "WebSocketUpdate":
        assert isinstance(obj, dict)
        devices = from_union(
            [lambda x: from_list(Device.from_dict, x), from_none], obj.get("devices")
        )
        positions = from_union(
            [lambda x: from_list(Position.from_dict, x), from_none],
            obj.get("positions"),
        )
        return WebSocketUpdate(devices, positions)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.devices is not None:
            result["devices"] = from_union(
                [lambda x: from_list(lambda x: to_class(Device, x), x), from_none],
                self.devices,
            )
        if self.positions is not None:
            result["positions"] = from_union(
                [lambda x: from_list(lambda x: to_class(Position, x), x), from_none],
                self.positions,
            )
        return result


def device_from_dict(s: Any) -> Device:
    return Device.from_dict(s)


def device_to_dict(x: Device) -> Any:
    return to_class(Device, x)


def device_attributes_from_dict(s: Any) -> DeviceAttributes:
    return DeviceAttributes.from_dict(s)


def device_attributes_to_dict(x: DeviceAttributes) -> Any:
    return to_class(DeviceAttributes, x)


def passport_from_dict(s: Any) -> Passport:
    return Passport.from_dict(s)


def passport_to_dict(x: Passport) -> Any:
    return to_class(Passport, x)


def position_from_dict(s: Any) -> Position:
    return Position.from_dict(s)


def position_to_dict(x: Position) -> Any:
    return to_class(Position, x)


def position_attributes_from_dict(s: Any) -> PositionAttributes:
    return PositionAttributes.from_dict(s)


def position_attributes_to_dict(x: PositionAttributes) -> Any:
    return to_class(PositionAttributes, x)


def session_from_dict(s: Any) -> Session:
    return Session.from_dict(s)


def session_to_dict(x: Session) -> Any:
    return to_class(Session, x)


def session_attributes_from_dict(s: Any) -> SessionAttributes:
    return SessionAttributes.from_dict(s)


def session_attributes_to_dict(x: SessionAttributes) -> Any:
    return to_class(SessionAttributes, x)


def subscription_from_dict(s: Any) -> Subscription:
    return Subscription.from_dict(s)


def subscription_to_dict(x: Subscription) -> Any:
    return to_class(Subscription, x)


def trip_from_dict(s: Any) -> Trip:
    return Trip.from_dict(s)


def trip_to_dict(x: Trip) -> Any:
    return to_class(Trip, x)


def web_socket_update_from_dict(s: Any) -> WebSocketUpdate:
    return WebSocketUpdate.from_dict(s)


def web_socket_update_to_dict(x: WebSocketUpdate) -> Any:
    return to_class(WebSocketUpdate, x)
