import mysql.connector

ENDPOINT = "Endpoint=sb://tmtfirstuatservicebus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=862EjZM0jy8sW5upGvHWBmbcXJX7K2MXCYrv3559PB8="
U2RS_QUEUE = "u2rsqueue"
RS2U_QUEUE = "rs2uqueue"
DATABASE = mysql.connector.connect(host="172.16.16.28", user="engineer", password="q47Ev!cbt*CJk36E", database="RMS")