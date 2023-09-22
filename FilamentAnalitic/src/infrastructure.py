from paho.mqtt import client as clientMQTT
import time
import json
import socket


class Config:
    def __init__(self):
        self.broker = {
            'host': '20.226.11.46',
            'port': 1883,
            'client_id': "",
            'user': "",                 
            'password': "",

            'keepAlive': 30,
        }
    
        self.errorLevel = 3
        self.mainTopic = "inovfablab/filamento"


class Logger:
    def __init__(self, errorLevel=3):
        self.errorLevel = errorLevel

    def error(self, message):
        print(f"[ERROR] {message}")

    def warning(self, message):
        if self.errorLevel >= 1:
            print(f"[WARNING] {message}")

    def info(self, message):
        if self.errorLevel >= 2:
            print(f"[INFO] {message}")

    def debug(self, message):
        if self.errorLevel >= 3:
            print(f"[DEBUG] {message}")


class MqttListener:
    def __init__(self, logger=None, host=None, port=None, username=None, password=None, client_id=None, topic=None, keepAlive=30):
        if not logger:
            logger = Logger()
        self.logger = logger

        if not host:
            raise Exception('Valor de host ta vazio!')
        
        self.topic = topic
        self.keepAlive = keepAlive
        self.host = host
        self.port = port
        self.profiles = []
        
        client_id = "%s_%d" % (client_id, int(time.time()))

        self.client = clientMQTT.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
       # self.client.on_publish = self.on_publish
        
        self.logger.debug(f"||PROGRAMA INICIADO COMO CLIENT_ID: {(client_id,)} ||")

    def start(self):
        self.run()

    def run(self):
        try:
            self.client.connect_async(host=self.host, port=self.port, keepalive=self.keepAlive)
            self.client.loop_forever(timeout=5.0, retry_first_connection=True)
        except socket.error:
            self.logger.debug("|| CONEXAO PERDIDA! TENTANDO SE CONECTAR NOVAMENTE ||")
            self.run()
    
    def registerProfile(self, profile=None):
        if not hasattr(profile, 'onDataReceived') or not callable(getattr(profile, 'onDataReceived')) or not hasattr(profile, 'canHandle') or not callable(getattr(profile, 'canHandle')):
            raise 'Invalid profile. Expected methods onDataReceived / canHandle'
        
        self.profiles.append(profile)

    def on_connect(self, client, userdata, flags, rc):
        self.logger.debug(f"|| CONECTADO EM {self.host}:{self.port} AS {self.client._client_id} ||")
        client.subscribe(self.topic)
        self.logger.debug(f"|| SUBSCREVENDO EM {(self.topic,)} ||")
    
    def publish(self, topic, msg):
        self.logger.debug(f"|| Publicando no topico {topic} AS {msg} ||")
        self.client.publish(topic ,msg)

    def on_message(self, client, userdata, message):
        # self.logger.debug("|| MENSSAGEM RECEBIDA %s: %s ||" % (message.topic, message.payload))
        for n in range(0, len(self.profiles)):
            if self.profiles[n].canHandle(message.topic):
                return self.profiles[n].onDataReceived(message.topic, message.payload)
        
        #self.logger.warning("Nenhum profile compativel registrado com o topic %s" % (message.topic))

    def on_disconnect(self, client, userdata, rc):
        self.client.reconnect()