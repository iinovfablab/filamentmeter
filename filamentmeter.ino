#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

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

const char *ssid     = "FABLAB";
const char *password = "IsEsc2018";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");


String semanas[7]={"Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sabado"};


String meses[12]={"Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"};


void setup() { 
  
  Serial.begin(9600);
  pinMode (pin1 ,INPUT_PULLUP);
  pinMode (pin2 ,INPUT_PULLUP);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  LastState = digitalRead(pin1); 
  timeClient.begin();

  timeClient.setTimeOffset(-10800);   
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

  float lastDistance = distance;
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
  

  if((lastDistance == distance) && (minutes - delta) > 1){
    lastDistance = distance;
    Pos = 0;
    endTime = timeClient.getFormattedTime();

    if(oneTime){
      Serial.println("======================");
      Serial.print("end time: ");
      Serial.println(endTime);
      Serial.print("distance: ");
      Serial.println(distance);
      
    }
    
    

  }
  else{

    distance = startMeasure();
    oneTime = 0;
  }
  
 }
