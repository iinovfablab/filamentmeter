#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define pi 3.14
#define R 11
#define N 40
#define MINUTES_LIMIT 2

int pin1 = 16;
int pin2 = 5;

int Pos = 0; 
int State;
int LastState;  

float lastDistance = 0;
float distance = 0;
int minutes = 0;
int flag = 0;

const char *ssid     = "FABLAB";
const char *password = "IsEsc2018";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

String semanas[7]={"Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sabado"};
String meses[12]={"Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"};

// buffer de tempo
char buffer_s[80];
struct tm* timeinfo;
//================

void setup() { 
  lastDistance = distance;
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


//funcação responsável por iniciar a leitura do encoder
static float startMeasure(int flag=0){
  if(!flag){
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
  else{
    Pos = 0;
    return distance;
  
  }
}
//===================================================


// função responsavél por contar tempo de inatividade 
static int countTime(float &lastDistance, int print, int reset_min){
  time_t now = time(nullptr);
  timeinfo = localtime(&now);
  strftime(buffer_s, 80, "%S", timeinfo);
  if(reset_min) minutes = 0;
  if((minutes > MINUTES_LIMIT)){
    minutes = 0;
    return 1;
  }
  if(atoi(buffer_s)>=59){
    minutes++;
  }
  if(atoi(buffer_s)%10==0){
    memset(buffer_s, 0, sizeof(char*));
    lastDistance = startMeasure(0);
    return 0;
    }
  
  if(print){
    Serial.print("tempo de inatividade: ");
    Serial.print(minutes);
    Serial.print(":");
    Serial.println(atoi(buffer_s));
  }

  return 0;
}

//=====================================================

void loop() {

  timeClient.update();

  if(lastDistance == startMeasure(flag)){
    countTime(lastDistance, 1, 0);
  }
  else{
    distance = startMeasure(countTime(lastDistance, 0, 1));
    Serial.print("passos encoder: ");
    Serial.println(distance*-1);
  }
}
