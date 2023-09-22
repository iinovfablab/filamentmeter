#from domain import 
import json
import numpy as np
import datetime
from model.slots_reservation import SlotsModel
import pandas as pd
from .tools import insert_row_distinct, convert_dict_datetime, check_alter, first_insert
from connections.connection_mongo import ConnectionMongo


class DetectaEnvento:
    def __init__(self, logger=None, device=None, MqttListener=None):
        self.logger = logger
        self.device = device
        self.MqttListener = MqttListener
        
        
        
    
    def canHandle(self, topic):
        return topic == "inovfablab/filamento" 
    
    def on_publish(self, topic, msg):
            self.logger.debug(f"|| Publicando no topico {topic} AS {msg} ||")
            self.MqttListener.publish(topic,msg)

    def onDataReceived(self, topic, payload,logger=None):
        sl = SlotsModel()
        mongo = ConnectionMongo()

        columns = ["consumo(minutos)", "id", "username", "data_inicio", "data_fim", "curso", "email"]
        
        

        if topic.endswith("filamento"):
            data = json.loads(payload)
            flag = data["finish"]
            try:
                data = convert_dict_datetime(data)
                mongo.mongo['collection2'].insert_one(data)

            except:
                pass

            finally:

                slts = sl.slots()
                dd = {}
                for key, value in zip(columns, list(zip(*slts))):
                    dd[key] = list(value)

                df = pd.DataFrame.from_dict(dd)
                
                df = insert_row_distinct(df)
                

                if flag:
                    first_insert(df)
                    check_alter()
                    self.logger.debug(f"|| BANCO DE DADOS ATUALIZADO COM SUCESSO")

                self.logger.debug(f"|| mensagem recebidas {data} ||")




        
            

     
    
