# hackathon
school project for hackathon

# Problem Definition 5Ws
![image](https://github.com/user-attachments/assets/8ebde35f-9cae-4aa7-9121-6ccfe0a3c9de)

# Personas
![RalfMuller](https://github.com/user-attachments/assets/615beb49-a145-4a21-8cf6-64e6fd3a1472)
![NadjaLind_(2)](https://github.com/user-attachments/assets/7d2bfc4f-3b68-44d2-9e15-566071bd475e)

# Empathy Map
![image](https://github.com/user-attachments/assets/2065a45a-f0e0-404a-a63e-ee4d77e52c0e)

# Critical Issues
![image](https://github.com/user-attachments/assets/cdcd751d-138e-42d8-90ba-7d2f5ea55388)

# Use-Case-Diagram
![image](https://github.com/user-attachments/assets/f4dadfbc-46f6-458d-8a18-8728fe1c4f24)


# Activity Diagram
![image](https://github.com/user-attachments/assets/5e4e6f5a-bca3-48b0-90da-35b30aab8ed0)


# Business Canvas Model
![image](https://github.com/user-attachments/assets/fbdecba2-55cf-4e58-bb61-12466e12aabc)


# Our Solution
There are currently solutions for health tracking and automatic notification of emergency services, alas in some cases, a fall detection can simply be triggered by dropping the device.

To reduce the strain on medical services our solution tries to reduce false alarms regarding emergencies. 

Our device works by first notifying the family / neighbors / people in close proximity, after a fall is detected. The notification can be canceled by the user, if it was not an emergency that required assistance. If a trusted person does not respond to the notification either, the emergency services get notified.

With our solution we are trying to reduce the strain on emergency response services, while improving the health outcomes for our users, since for medical emergencies, the sooner the response, the better the outcome. 

# Code
import RPi.GPIO as GPIO
import time
from datetime import datetime
import paho.mqtt.client as mqtt

# Definieren der verwendeten GPIO Pins
tapPin = 11
buttonPin = 24
ledPin = 31

# Variablen für den Schocksensor
tapIntensity = 0
tapThreshold = 50
tapStatus = False
tapTimer = 0
tapTimerTimeout = 0.5
tapTimerStatus = False

# Variablen für den Knopf
buttonStatus = False

# Variablen für den Alarm
alarmTimer = 0
alarmTimerTimeout = 10
alarmTimerStatus = False
messageSent = False

# GPIO pins konfigurieren
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(tapPin, GPIO.IN)
GPIO.setup(buttonPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW)
print("Konfig fertig")

# Variablen zum Versenden der Message per MQTT
username = "Herbert"
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
MQTT_HOST = "192.168.202.195"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "Sturzalarm"
MQTT_MSG = dt_string + " " + username + " ist gerade gestuerzt"

# Schickt eine Meldung, dass Person gestuerzt ist an andere Geraete
def sturzmeldungVersenden():
	mqttc = mqtt.Client()
	mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL) 
	mqttc.publish(MQTT_TOPIC,MQTT_MSG)
	mqttc.disconnect()

# Die Loop
while True:
	# Messung der Schockintensität
	tapStatus = GPIO.input(tapPin)
	if tapStatus == False:
		if (tapTimerStatus == False):
			tapTimerStatus = True
			tapTimer = time.time()
			print("timer gestartet")
			
		tapIntensity += 1
		print(tapIntensity)
	# Schockintesitätsmessung zurücksetzen
	if time.time() > tapTimer + tapTimerTimeout and tapTimerStatus == True:
		tapIntensity = 0
		tapTimerStatus = False
	# Alarm starten, wenn der Schock stark genug ist
	if tapIntensity > tapThreshold:
		if alarmTimerStatus == False:
			alarmTimerStatus = True
			alarmTimer = time.time()
	# Abbruchbedingung für den Alarmtimer
	buttonStatus = GPIO.input(buttonPin)
	if buttonStatus == False and alarmTimerStatus == True:
		alarmTimerStatus = False
		GPIO.output(ledPin, GPIO.LOW)
		messageSent = False
	# Wenn Alarm nicht abgebrochen wird
	if alarmTimerStatus == True:
		if time.time() > alarmTimer + alarmTimerTimeout:
			GPIO.output(ledPin, GPIO.HIGH)
			if messageSent == False:
				sturzmeldungVersenden()
				messageSent = True
		elif time.time() % 1 > 0.5:
			GPIO.output(ledPin, GPIO.HIGH)
		else:
			GPIO.output(ledPin, GPIO.LOW)

# Idea of product
![image](https://github.com/user-attachments/assets/9a694787-2d66-411c-a87c-0f0dfb595dc6)

