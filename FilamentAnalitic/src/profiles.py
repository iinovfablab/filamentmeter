#from domain import 
import json
import numpy as np
import datetime
from model.slots_reservation import SlotsModel
import pandas as pd
from .tools import reverse_key_to_value, check_date_time, alter_table, insert_row_distinct


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
        columns = ["consumo(minutos)", "id", "username", "data_inicio", "data_fim", "curso", "email"]
        sl = SlotsModel()
        

        


        if topic.endswith("filamento"):
            
            data = json.loads(payload)
        
            slts = sl.slots()
            dd = {}
            for key, value in zip(columns, list(zip(*slts))):
                dd[key] = list(value)

            df = pd.DataFrame.from_dict(dd)

            df = insert_row_distinct(df)
            df['consumo(minutos)'] = df['consumo(minutos)'].apply(lambda x: x.seconds/60)
            

            check = check_date_time(df)
        
            
            if not check.empty:
                
                alter_table(df, int(check.iloc[0]), data["distance"])

                self.logger.debug(f"|| TABELA ATUALIZADA COM SUCESSO- NO ID {int(check.iloc[0])}")
                df.to_csv("slots.csv", index=False)


            self.logger.debug(f"|| mensagem recebidas {data} ||")



        
            

     
    
