from infrastructure import Logger, Config,  MqttListener
import profiles

if __name__ == "__main__":
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
    profileDetectaEvento = profiles.DetectaEnvento(logger,"inovfablab/filamento",mqttListener)
   
    #mqttListener.registerProfile(profileGeladeira)
    mqttListener.registerProfile(profileDetectaEvento)

    mqttListener.start()