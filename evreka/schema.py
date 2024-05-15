import datetime
import graphene
from evreka.controller import all_devices, create_device, delete_device, get_location_history


class Device(graphene.ObjectType):
    name = graphene.String()
    ip_address = graphene.String()
    port = graphene.Int()
    id = graphene.Int()


class DeviceLocation(graphene.ObjectType):
    name = graphene.String()
    latitude = graphene.Float()
    longitude = graphene.Float()
    timestamp = graphene.DateTime()


class LocationData(graphene.ObjectType):
    latitude = graphene.Float()
    longitude = graphene.Float()
    timestamp = graphene.DateTime()


class DeviceLocationHistory(graphene.ObjectType):
    name = graphene.String()
    locations = graphene.List(LocationData)


class CreateDevice(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        ip_address = graphene.String()
        port = graphene.Int()

    ok = graphene.Boolean()
    device = graphene.Field(lambda: Device)

    def mutate(root, info, name, ip_address, port):
        ok = True
        device_id = create_device(name, ip_address, port)
        if device_id == -1:
            return CreateDevice(ok=False)
        device = Device(name=name, ip_address=ip_address, port=port, id=device_id)
        return CreateDevice(device=device, ok=ok)


class DeleteDevice(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(root, info, id):
        try:
            delete_device(id)
            message = 'device deleted'
            ok = True
        except Exception as e:
            message = e
            ok = False
        return DeleteDevice(ok=ok, message=message)


class MyMutations(graphene.ObjectType):
    create_device = CreateDevice.Field()
    delete_device = DeleteDevice.Field()


class Query(graphene.ObjectType):
    device_list = graphene.List(Device)
    device_locations = graphene.List(DeviceLocation)
    location_history = graphene.Field(DeviceLocationHistory, id=graphene.Int())

    def resolve_device_list(self, info):
        device_list = []
        for uid, device in all_devices.items():
            device = Device(name=device.name, ip_address=device.ip_address, port=device.port, id=uid)
            device_list.append(device)
        return device_list

    def resolve_device_locations(self, info):
        last_location_list = []
        for device in all_devices.values():
            loc = device.last_location
            if loc is not None:
                device_loc = DeviceLocation(name=device.name, latitude=loc.lat, longitude=loc.long,
                                            timestamp=loc.timestamp)
            else:
                device_loc = DeviceLocation(name=device.name, latitude=None, longitude=None, timestamp=None)

            last_location_list.append(device_loc)
        return last_location_list

    def resolve_location_history(self, info, id):
        locations_data = get_location_history(id)
        name = all_devices[id].name
        locations = []
        for location in locations_data:
            location = LocationData(latitude=location.lat, longitude=location.long, timestamp=location.timestamp)
            locations.append(location)
        return DeviceLocationHistory(name=name, locations=locations)


schema = graphene.Schema(query=Query, mutation=MyMutations)
