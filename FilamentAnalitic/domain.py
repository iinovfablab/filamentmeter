#from domain import 
import json
import numpy as np
import datetime


class DetectaEnvento:
    def __init__(self, logger=None, device=None, MqttListener=None):
     
    
    def canHandle(self, topic):
        return topic == "inovfablab/filamento" 
    
    def on_publish(self, topic, msg):
            self.logger.debug("|| Publicando no topico %s AS %s ||" % (topic, msg))
            self.MqttListener.publish(topic,msg)

    def onDataReceived(self, topic, payload,logger=None,):
        data = json.loads(payload)
                
        if topic.endswith("filamento"):

            self.logger.debug("|| mensagem recebidas %s ||" % (data))
                