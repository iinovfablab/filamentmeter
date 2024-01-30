extern "C"{
#include "user_interface.h"
}
#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <string.h>
#include <Ticker.h>
#include <ArduinoJson.h>


#include <AsyncMqttClient.h>

#define pi 3.14
#define R 5.5
#define N 40

#define MQTT_HOST "20.226.11.46"
#define MQTT_PORT 1883

#define MQTT_PUB_TIME "inovfablab/filamento"


os_timer_t mTimer;


static bool _timeout = false;
static long distanceNow, distanceLast;
static int second=0;
int Pos = 0; 
int State;
int LastState;
char buffer[1024];

static bool first_send = false;
static bool end_send = false;

const char *ssid     = "FABLAB";
const char *password = "IsEsc2018";

String semanas[7]={"Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sabado"};
String meses[12]={"Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"};

AsyncMqttClient mqttClient;
Ticker mqttReconnectTimer;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

DynamicJsonDocument data(200);


void connectToMqtt();
void onMqttConnect(bool sessionPresent);
void onMqttDisconnect(AsyncMqttClientDisconnectReason reason);
void onMqttPublish(uint16_t packetId);

static float startMeasure();
void incrementSecond();


//Nunca execute nada na interrupcao, apenas setar flags!
void tCallback(void *tCall);
void usrInit(void);
//=====================================================

void zCallback(void *);
void measrInit(void);

void setup() {
  Serial.begin(115200);

  mqttClient.onConnect(onMqttConnect);
  mqttClient.onDisconnect(onMqttDisconnect);
  mqttClient.onPublish(onMqttPublish);
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  //LastState = digitalRead(pin1); 
  timeClient.begin();
  timeClient.setTimeOffset(-10800);
  connectToMqtt();
  //iniciar a interrupcao
  usrInit();
}


void loop() {
  
  
  timeClient.update();
  time_t epochTime = timeClient.getEpochTime();
  struct tm *ptm = gmtime ((time_t *)&epochTime);

  data["start_time"];
  data["end_time"];
  data["distance"];
  data["date-time"];


  int monthDay = ptm->tm_mday;
  int currentMonth = ptm->tm_mon+1;
  String currentMonthName = meses[currentMonth-1];
  int currentYear = ptm->tm_year+1900;


  String currentDate = String(currentYear) + "-" + String(currentMonth) + "-" + String(monthDay) + " " + String(timeClient.getFormattedTime());


  distanceNow = startMeasure();

  if((distanceNow == distanceLast) && (second%20==0)){
      
      if(end_send && (second >= 20) ){
        Serial.print("Data final: ");
        Serial.print(currentDate);
        Serial.print(" time: ");
        Serial.println(timeClient.getFormattedTime());
        data["end_time"] = currentDate;
        data["distance"] = distanceNow*-1;
        data["date-time"] = currentDate;
        serializeJson(data, buffer);
        end_send = false;
        first_send = false;
        _timeout = true;
        distanceNow = startMeasure();
        distanceLast = 0;
        mqttClient.publish(MQTT_PUB_TIME, 0, true, buffer);
        
      }
    }
  
  if(!first_send && (distanceNow != distanceLast)){
    Serial.print("Data inicial: ");
    Serial.print(currentDate);
    Serial.print(" time: ");
    Serial.println(timeClient.getFormattedTime());
    data["start_time"] = currentDate;
    first_send = true;
    end_send = true;
    second = 0;

  }

  
  

  else{
    _timeout = false;
    
  }

}


void tCallback(void *tCall){
  incrementSecond();
}
void usrInit(void){
    os_timer_setfn(&mTimer, tCallback, NULL);
    os_timer_arm(&mTimer, 1000, true);
}
void incrementSecond(){
  if(second%5==0){
    distanceLast = startMeasure();
  }
  //Serial.println(second);
  if(second>60){
    second=0;
  }
  else{
    second ++;
  }
}
static float startMeasure(){
      State = digitalRead(16);
       if (State != LastState){     
         if (digitalRead(5) != State) { 
           Pos ++;
         } 
         else {
           Pos --;
         }
      }
      if(_timeout){
        Pos = 0;
      }
      distanceNow = ((2*pi*R)/N) * Pos ;
      if (distanceNow > 0){
        Pos = 0;
      }
      LastState = State;
    return distanceNow;
}
void connectToMqtt() {
  Serial.println("Connecting to MQTT...");
  mqttClient.connect();
}
void onMqttConnect(bool sessionPresent) {
  Serial.println("Connected to MQTT.");
  Serial.print("Session present: ");
  Serial.println(sessionPresent);
}
void onMqttDisconnect(AsyncMqttClientDisconnectReason reason) {
  Serial.println("Disconnected from MQTT.");

  if (WiFi.isConnected()) {
    mqttReconnectTimer.once(2, connectToMqtt);
  }
}
void onMqttPublish(uint16_t packetId) {
  Serial.print("Publish acknowledged.");
  Serial.print("  packetId: ");
  Serial.println(packetId);
}
