import logging
import datetime
import socket
from struct import unpack
from threading import Thread
from time import sleep

from evreka.db import add_new_device, get_device_list, delete_device_from_db, \
    get_location_history_from_db, get_last_location_of_device
from evreka.db_async import db_queue
from evreka.model import Location, Device

all_devices = {}


def device_connection_and_data_handler(device: Device):
    logging.info(f'device_connection_and_data_handler started for {device.name}')
    while device.device_is_active:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((device.ip_address, device.port))
                logging.info(f'connected to the device {device.name}')
            except Exception as e:
                logging.warning(f'Exception raised on {device.name} ex: {e}')
                sleep(5)
                continue

            while device.device_is_active:
                try:
                    data = s.recv(1024)
                    lat, long = unpack("@ff", data)
                    logging.info(f'received new location from {device.name}')
                    timestamp = datetime.datetime.now()
                    location = Location(lat, long, timestamp)
                    device.add_location_entity(location)
                    db_queue.put((device.id, location))
                except Exception as e:
                    logging.warning(f'Exception raised on recv {device.name} ex: {e}')
                    break
    logging.info(f'device_connection_and_data_handler finished for {device.name}')


def create_device(name, ip_address, port, uid=None):
    if uid is None:
        if len(all_devices) > 0:
            uid = max(all_devices, key=int) + 1
        else:
            uid = 1

    device = Device(name=name, id=uid, ip_address=ip_address, port=port)
    if add_new_device(uid, name, ip_address, port):
        all_devices[uid] = device
        t = Thread(target=device_connection_and_data_handler, args=(device,))
        t.start()
        return uid
    return -1


def delete_device(uid):
    if uid not in all_devices:
        raise Exception('id not found in device list')
    device = all_devices[uid]
    delete_device_from_db(uid)
    device.device_is_active = False
    del all_devices[uid]


def load_devices_from_db():
    devices = get_device_list()
    for device_tuple in devices:
        if device_tuple[0] not in all_devices:
            device = Device(name=device_tuple[1], ip_address=device_tuple[2], port=device_tuple[3], id=device_tuple[0])
            all_devices[device_tuple[0]] = device
            location = get_last_location_of_device(device.id)
            if len(location) > 0:
                device.last_location = Location(lat=location[0][1], long=location[0][2], timestamp=location[0][3])
            t = Thread(target=device_connection_and_data_handler, args=(device,))
            t.start()


def get_location_history(uid):
    locations = get_location_history_from_db(uid)
    locations_ret = []
    for location in locations:
        locations_ret.append(Location(lat=location[1], long=location[2], timestamp=location[3]))
    return locations_ret
