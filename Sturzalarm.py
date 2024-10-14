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
