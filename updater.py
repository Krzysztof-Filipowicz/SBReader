import prealert as p
from logger import insert_log
import mysql.connector

try:
    db = mysql.connector.connect(host="172.16.16.27", user="mimas", password="483JzXb#c=qx8HzZ", database="RMS")
except Exception as cx:
    insert_log(cx + " CX", "error")


# def check_job_id(imei, serial):
#     try:
#         db.reconnect()
#         cursor = db.cursor()
#         sql_search = "SELECT jobnumber FROM job WHERE (job.imei=%s OR job.serial=%s) AND job.serial<>'Unknown' AND  job.lastStatus<>'BOOKED OUT'"
#         val = (imei, serial)
#         cursor.execute(sql_search, val)
#         result = cursor.fetchone()
#
#         if result is not None:
#             return True
#         else:
#             return False
#
#     except (db.Error, db.Warning) as dx:
#         insert_log(dx + " DX", "error")
#     finally:
#         db.close()


def create_new_job(msg):
    try:
        message_type = msg['MessageType']
        complaint = msg['Message']['Complaint']
        notes = msg['Message']['Notes']
        job_id = msg['Message']['JobId']
        reference = msg['Message']['ReferenceNumber']
        manufacturer = msg['Message']['Equipment']['Manufacturer']['Name']
        model = msg['Message']['Equipment']['PhoneModel']['Name']
        colour = msg['Message']['Equipment']['Color']['Name']
        imei = msg['Message']['Equipment']['Imei']
        serial = msg['Message']['Equipment']['SerialNumber']
        model_code = msg['Message']['Equipment']['PhoneModel']['Number']
        customer = msg['Message']['Organisation']['Name']
        # tracking_number = msg['Message']['Organisation']['Name']

        if message_type == 'NewRepair':

            # if not check_job_id(imei, serial):

            db.reconnect()
            cursor = db.cursor()
            print(job_id)
            sql_job = "INSERT INTO job (jobnumber, source, batch, customerRef, imei, serial, manufacturer, model, colour, lastStatus, modelCode) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val1 = (job_id, 2, "CONNECT", reference, imei, serial, manufacturer, model, colour, "PRE-ALERT", model_code)
            cursor.execute(sql_job, val1)

            sql_tracking = "INSERT INTO tracking (jobnumber, batch, imei, serial, status, customer, user) \
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val2 = (job_id, "CONNECT", imei, serial, "PRE-ALERT", customer, "System")
            cursor.execute(sql_tracking, val2)

            sql_repair = "INSERT INTO repair (jobnumber, complaint, notes) \
                                               VALUES (%s, %s, %s)"
            val3 = (job_id, complaint, notes)
            cursor.execute(sql_repair, val3)

            db.commit()

            if cursor.rowcount > 0:
                p.pre_alert(job_id)
                return True
        # else:
        #     message = "IMEI: {}, Serial: {} is already in the business!".format(imei, serial)
        #     insert_log(message, "error")
        #     return False

    except Exception as ex:
        insert_log(ex + " EX", "error")
    finally:
        db.close()
