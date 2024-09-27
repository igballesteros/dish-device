# ENGG*4200 Project

import RPi.GPIO as GPIO
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def Data_Over_Wifi(data):
    try:
        response = requests.post(SERVER_ENDPOINT, data={'distance': data}, verify=False)
        response.raise_for_status()
        print("Data sent Succesfully!")
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

def Moving_Average(dist):
    distanceBuffer.pop(0)
    distanceBuffer.append(dist)
    return sum(distanceBuffer) / readings
                
SERVER_ENDPOINT = "https://10.0.0.118:5000/data"

#board pin numbering system
GPIO.setmode(GPIO.BCM)

delayTime = 0.2

#trigger and echo pins setup
trigPin = 23
echoPin = 24
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

#variables for reading processing
distThreshold= 63.5
currentReadings = 0
readings = 5
distanceBuffer = [0]*readings

occurrences = 0
actualReadings = 0
maxReadings = 100
maxOccurrences = 2

#sensor code
try:
    while actualReadings < maxReadings and occurrences < maxOccurrences:
        #start the pulse to send a ping
        #set trigger to low for 2 micro seconds
        GPIO.output(trigPin, 0)
        time.sleep(2E-6)
        
        #set triger pin to high for 10 micro seconds
        GPIO.output(trigPin, 1)
        time.sleep(10E-6)
        
        #go back to zero to complete ping communication
        GPIO.output(trigPin, 0)
        
        #wait until echo pin goes to highto start timer
        while GPIO.input(echoPin) == 0:
            pass
        
        #start timer
        echoStartTime = time.time()
        
        #wait for echo pin to go down to zero
        while GPIO.input(echoPin) == 1:
            pass
        
        #calculate travel time
        echoStopTime = time.time()
        pingTravelTime = echoStopTime - echoStartTime
        currentDist = (pingTravelTime * 34444) / 2
        currentReadings += 1
        actualReadings += 1
        print('Current Distance', currentReadings, '=',  round(currentDist, 1), 'cm')


        filteredDist = Moving_Average(currentDist)
        
        #compare distance to threshold
        #send email if distance is smaller than threshold
        if (currentReadings >= readings):
            print('Filtered Distance =',  round(filteredDist, 1), 'cm\n')
            Data_Over_Wifi(filteredDist)
            
            if (filteredDist < distThreshold):
                currentReadings = 0
                occurrences += 1


        time.sleep(delayTime)
        time.sleep(0)
        
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
