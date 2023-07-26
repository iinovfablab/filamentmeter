#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

bool _timeout = false;
os_timer_t mTimer;
int state1 = 0;

void tCallback(void *tCall){
    _timeout = true;
    state1 = state1^1;
}

void usrInit(void){
    os_timer_setfn(&mTimer, tCallback, NULL);
    os_timer_arm(&mTimer, 500, true);
}

int pin1 = 16;
int pin2 = 5;


int Pos = 0; 
int State;
int LastState;  

const float pi = 3.14;
const float R = 5.5;
const int N = 40;

float lastDistance = 0;
float distance = 0;
int minutes, delta, oneTime = 0;
String startTime, endTime;

const char *ssid     = "gatoalado";
const char *password = "sergiojuliana";



WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

String semanas[7]={"Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sabado"};
String meses[12]={"Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"};

void setup() { 
  
  Serial.begin(9600);
  pinMode (pin1 ,INPUT_PULLUP);
  pinMode (pin2 ,INPUT_PULLUP);
  pinMode (4,OUTPUT);
  pinMode (0,OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  LastState = digitalRead(pin1); 
  timeClient.begin();
  timeClient.setTimeOffset(-10800);   
  usrInit();
} 



static float startMeasure(){
    lastDistance = distance;
      State = digitalRead(pin1);
       if (State != LastState){     
         if (digitalRead(pin2) != State) { 
           Pos ++;
         } 
         else {
           Pos --;
         }
      }
      distance = ((2*pi*R)/N) * Pos ;
      if (distance > 0){
        Pos = 0;
      }
      LastState = State;
    return distance;
  }


void loop() {
  timeClient.update();
  minutes = timeClient.getMinutes();
  lastDistance = distance;

  if(delta == 0){
    startTime = timeClient.getFormattedTime();
    Serial.print("started time: ");
    Serial.println(startTime);
    Serial.print("distance: ");
    Serial.println(distance);
    delta = timeClient.getMinutes();
    distance = startMeasure();
    oneTime = 1;
  }
  
  int delta2= minutes - delta;
  if(lastDistance == distance) {
    if (delta2 > 1){
    lastDistance = distance;
    Pos = 0;
    endTime = timeClient.getFormattedTime();
    oneTime = 1;

    if(oneTime){
      Serial.println("======================");
      Serial.print("end time: ");
      Serial.println(endTime);
      Serial.print("distance: ");
      Serial.println(distance);
      oneTime = 0;
      delta = timeClient.getMinutes();
      }
    }
  }
  else{
    distance = startMeasure();
    oneTime = 0;
  }
  
  if (_timeout){
        //Serial.println("cuco!");
        _timeout = false;
        digitalWrite(4, state1);
        digitalWrite(0, !state1);
        //Serial.println(state);
        //Serial.println(!state);
        /*      
        Serial.print("distance: ");
        Serial.println(distance);
        Serial.print("delta: ");
        Serial.println(delta);
        Serial.print("oneTime: ");
        Serial.println(oneTime);
        Serial.print("lastDistance: ");
        Serial.println(lastDistance);
        Serial.print("minutes: ");
        Serial.println(minutes);
        Serial.print("delta2: ");
        Serial.println(delta2);
        */
    }
}
