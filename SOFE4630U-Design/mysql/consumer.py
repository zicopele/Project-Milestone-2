
from google.cloud import pubsub_v1
import mysql
import json
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\hamzi\Desktop\SOFE4630U-MS2-main\SOFE4630U-Design\mysql\amazing-sunset-448818-i6-cf45924c8946.json"
project_id = "amazing-sunset-448818-i6"
subscription_id = "csvRecords-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

db = mysql.connector.connect(
    host="34.152.49.145",
    user="usr",
    password="sofe4630u",
    database="csvReadings"
)

def callback(message):
    row_data = json.loads(message.data.decode("utf-8"))
    cursor = db.cursor()
    insert_query = ("INSERT INTO your_table "
                    "(Timestamp, Car1_Location_X, Car1_Location_Y, Car1_Location_Z, "
                    " Car2_Location_X, Car2_Location_Y, Car2_Location_Z, Occluded_Image_view, "
                    " Occluding_Car_view, Ground_Truth_View, pedestrianLocationX_TopLeft, "
                    " pedestrianLocationY_TopLeft, pedestrianLocationX_BottomRight, "
                    " pedestrianLocationY_BottomRight) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data_tuple = (
        row_data["Timestamp"],
        row_data["Car1_Location_X"],
        row_data["Car1_Location_Y"],
        row_data["Car1_Location_Z"],
        row_data["Car2_Location_X"],
        row_data["Car2_Location_Y"],
        row_data["Car2_Location_Z"],
        row_data["Occluded_Image_view"],
        row_data["Occluding_Car_view"],
        row_data["Ground_Truth_View"],
        row_data["pedestrianLocationX_TopLeft"],
        row_data["pedestrianLocationY_TopLeft"],
        row_data["pedestrianLocationX_BottomRight"],
        row_data["pedestrianLocationY_BottomRight"]
    )
    cursor.execute(insert_query, data_tuple)
    db.commit()
    cursor.close()
    message.ack()

future = subscriber.subscribe(subscription_path, callback=callback)
print("Listening for CSV record messages...")
future.result()