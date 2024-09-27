from flask import Flask, request
import Data_Processing
import Data_Storage

app = Flask(__name__)

threshold = 63.5

sensorLogger = Data_Storage.SensorDataLogger()

@app.route('/data', methods=['POST'])

def receive_data():
    data = request.form.get('distance')
    roundedData = round(float(data), 1)
    print(f"Recieved Data: {roundedData} cm\n")

    sensorLogger.log_measurement([roundedData])
    sensorLogger.save_to_file()

    check = Data_Processing.ProcessData(data, threshold)

    if check == True:
        print('There are dirty dishes in the sink')
        for emails in Data_Processing.RECIPIENT_EMAIL:
            print('Email was sent to ', emails)
            
        print('\n')
        
    return 'Data received succesfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
