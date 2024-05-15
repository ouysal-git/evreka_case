import mysql.connector
import logging

mydb = mysql.connector.connect(host='testdb', user='root', password='root', port=3306, database='evreka')


def add_new_device(id, name, ip, port):
    try:
        cursor = mydb.cursor()
        sql = "INSERT INTO devices (id, name, ip_address, port) VALUES (%s, %s, %s, %s)"
        val = (id, name, ip, port)
        cursor.execute(sql, val)
        mydb.commit()
        logging.info("record inserted.")
        return True
    except Exception as e:
        logging.info(f'exception on insert: {e}')
        return False


def delete_device_from_db(id):
    try:
        cursor = mydb.cursor()
        sql = "DELETE FROM `devices` WHERE id = %s"
        adr = (id,)

        cursor.execute(sql, adr)
        mydb.commit()
        logging.info("record deleted.")
        return True
    except Exception as e:
        logging.info(f'exception on delete: {e}')
        return False


def get_device_list():
    cursor = mydb.cursor()
    cursor.execute("SELECT * from devices")
    return cursor.fetchall()


def add_location_to_device(device_id, latitude, longitude, timestamp):
    try:
        cursor = mydb.cursor()
        sql = "INSERT INTO location_history (id, latitude, longitude, time_stamp_) VALUES (%s, %s, %s, %s)"
        val = (device_id, latitude, longitude, timestamp.strftime('%Y-%m-%d %H:%M:%S'), )
        cursor.execute(sql, val)
        mydb.commit()
        logging.info("record inserted.")
        return True
    except Exception as e:
        logging.info(f'exception on insert: {e}')
        return False


def get_location_history_from_db(uid):
    cursor = mydb.cursor()
    query = "SELECT * from location_history where id = '%d' order by time_stamp_" % uid
    cursor.execute(query)
    return cursor.fetchall()

def get_last_location_of_device(uid):
    cursor = mydb.cursor()
    query = "SELECT * FROM location_history lh " \
            "WHERE id = '%d' and time_stamp_ IN(SELECT max(time_stamp_) FROM location_history)" % uid
    cursor.execute(query)
    return cursor.fetchall()