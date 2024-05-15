import datetime


class Location:
    def __init__(self, lat: float, long: float, timestamp: datetime):
        self.lat = lat
        self.long = long
        self.timestamp = timestamp


class Device:
    def __init__(self, id, name, ip_address, port):
        self.id = id
        self.name = name
        self.ip_address = ip_address
        self.port = port
        self.last_location = None
        self.device_is_active = True

    def add_location_entity(self, location: Location):
        self.last_location = location
