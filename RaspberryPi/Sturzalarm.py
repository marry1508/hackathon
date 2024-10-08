import RPi.GPIO as GPIO
import time

# Definieren der verwendeten GPIO Pins
tapPin = 11
buttonPin = 24
ledPin = 31

# Variablen für den Schocksensor
tapIntensity = 0
tapThreshold = 100
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

# GPIO pins konfigurieren
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(tapPin, GPIO.IN)
GPIO.setup(buttonPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW)
print("Konfig fertig")

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
		print("Knopf gedrückt")
	# Wenn Alarm nicht abgebrochen wird
	if alarmTimerStatus == True:
		if time.time() > alarmTimer + alarmTimerTimeout:
			GPIO.output(ledPin, GPIO.HIGH)
		elif time.time() % 1 > 0.5:
			GPIO.output(ledPin, GPIO.HIGH)
		else:
			GPIO.output(ledPin, GPIO.LOW)