from .infrastructure import Logger, Config,  MqttListener
from .profiles import DetectaEnvento

if __name__ == "main":
    config = Config()
    logger = Logger(config.errorLevel)
    
    mqttListener = MqttListener(logger,
        config.broker['host'],
        config.broker['port'],
        config.broker['user'],
        config.broker['password'],
        config.broker['client_id'],
        config.mainTopic,
        config.broker['keepAlive'])

    #profileGeladeira = profiles.Geladeira(logger, database, "tele/SmartEng_Geladeira_008506/SENSOR")
    profileDetectaEvento = DetectaEnvento(logger,"/inovfablab/filamento",mqttListener)
    #mqttListener.registerProfile(profileGeladeira)
    mqttListener.registerProfile(profileDetectaEvento)
    mqttListener.start()