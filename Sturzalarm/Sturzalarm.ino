int tapPin = 7;
int tapStatus;
int x;
int buttonPin = 8;
int buttonStatus;
int ledPin = 6;
long tapTimer;
long tapTimerTimeout = 500;        //0,5s
bool tapTimerStatus = false;
long alarmTimer;
long alarmTimerTimeout = 10000; //30s
bool alarmTimerStatus = false;
int shockTreshold = 15;

void setup() {
  pinMode(tapPin, INPUT); 
  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Schocksensor quasi oder so idk
  tapStatus = digitalRead(tapPin);
  if(!tapStatus) {
    if(tapTimerStatus == false) {
      tapTimerStatus = true;
      tapTimer = millis();
      Serial.println("Start");
    }
    Serial.println(x);
    x+=1;
  }
  
  // Schockintensität zurücksetzen
  if(millis() > tapTimer + tapTimerTimeout && tapTimerStatus == true){
    x = 1;
    tapTimerStatus = false;
    Serial.println("stop");
  }

  // Alarm starten, wenn starker schock gemessen wurde
  if (x > shockTreshold) {
    if (alarmTimerStatus == false) {
      alarmTimerStatus = true;
      alarmTimer = millis();
      Serial.println("Alarm gestartet");
    }
  }

  // Möglichkeit, Alarm abzubrechen
  buttonStatus = digitalRead(buttonPin);
  if (buttonStatus == LOW && alarmTimerStatus == true) {
    alarmTimerStatus = false;
    Serial.println("Alarm gestoppt");
    digitalWrite(ledPin, LOW);
  }
  
  // Alarm, wenn nicht abgebrochen wurde
  if(alarmTimerStatus == true) {
    if (millis() > alarmTimer + alarmTimerTimeout){
      digitalWrite(ledPin, HIGH);
    }
    else if (millis() % 1000 > 500) {
      digitalWrite(ledPin, HIGH);
    }
    else {
      digitalWrite(ledPin, LOW);
    }
  }

}