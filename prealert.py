import json
from datetime import datetime

from azure.servicebus import ServiceBusMessage, ServiceBusClient
from logger import insert_log

### ENDPOINT = "Endpoint=sb://tmtfirstuatservicebus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=862EjZM0jy8sW5upGvHWBmbcXJX7K2MXCYrv3559PB8="
ENDPOINT = "Endpoint=sb://tmtfirstprodqueues.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XRIaMrfogIYIWSLF+7msAZ2gW3m+8FLUuxaKNiFsZbE="
QUEUE = "u2rsqueue"
utc_dt = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f0Z')

try:
    def pre_alert(jobnumber):
        with ServiceBusClient.from_connection_string(
                conn_str=ENDPOINT,
                logging_enable=True) as servicebus_client:
            sender = servicebus_client.get_queue_sender(queue_name=QUEUE)
            with sender:
                send_message(sender, jobnumber)

except Exception as ex:
    print(ex)
    insert_log(ex, "error")


def send_message(sender, jobnumber):
    msg = json.dumps({
        "MessageType": "RepairStatusUpdate",
        "Message": {
            "OrganisationName": None,
            "JobId": jobnumber,
            "UpdatedDate": utc_dt,
            "LastStatus": None,
            "NewStatus": "51"
        }
    })
    message = ServiceBusMessage(msg)
    sender.send_messages(message)
