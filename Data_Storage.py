import csv
from datetime import datetime
import time

class SensorDataLogger:
    def __init__(self):
        self.data = {}

    def log_measurement(self, measurements):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stream_key = 'DataLogKey'

        if stream_key not in self.data:
            self.data[stream_key] = {
                'start_time': timestamp,
                'measurements': []
            }

        self.data[stream_key]['measurements'].extend(measurements)

    def save_to_file(self, file_name="Data_Log.csv"):
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(['Timestamp', 'Measurement', 'Start_Time'])

            for stream_key, stream_data in self.data.items():
                start_time = stream_data['start_time']

                for measurement in stream_data['measurements']:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([timestamp, measurement, start_time])

        self.data = {}
