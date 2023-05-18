import json
import time
from azure.servicebus import ServiceBusClient
from updater import create_new_job
from logger import insert_log

# ENDPOINT = "Endpoint=sb://tmtfirstuatservicebus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=862EjZM0jy8sW5upGvHWBmbcXJX7K2MXCYrv3559PB8="
ENDPOINT = "Endpoint=sb://tmtfirstprodqueues.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XRIaMrfogIYIWSLF+7msAZ2gW3m+8FLUuxaKNiFsZbE="
QUEUE = "rs2uqueue"

servicebus_client = ServiceBusClient.from_connection_string(conn_str=ENDPOINT, logging_enable=True)


def get_messages():
    try:
        with servicebus_client:
            receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE, max_wait_time=5)
            with receiver:
                received_count = 0
                missed_count = 0
                for msg in receiver:
                    if msg is not None:
                        if create_new_job(json.loads(str(msg))):
                            received_count += 1
                            receiver.complete_message(msg)
                        else:
                            missed_count += 1
                if received_count > 0:
                    message = str(received_count) + " jobs have been imported"
                    if missed_count > 0:
                        message += " and " + str(missed_count) + " have been skipped"
                    insert_log(message, "info")
                    print(message)

    except Exception as qex:
        print(qex)
        insert_log(qex, "error")


try:
    print("*** Mimas ver. 1.0 ***")
    print("Reading messages from the queue...\n")
    while True:
        get_messages()
        time.sleep(60)
except Exception as ex:
    print(ex)
    insert_log(ex, "error")
