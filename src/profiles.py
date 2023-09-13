#from domain import 
import json
import numpy as np
import datetime
from model.slots_reservation import SlotsModel
import pandas as pd
from .tools import reverse_key_to_value, check_date_time, alter_table, insert_row_distinct
import os
from datetime import datetime as dt

class DetectaEnvento:
    def __init__(self, logger=None, device=None, MqttListener=None):
        self.logger = logger
        self.device = device
        self.MqttListener = MqttListener
        self.sl = SlotsModel()

     
    
    def canHandle(self, topic):
        return topic == "inovfablab/filamento" 
    
    def on_publish(self, topic, msg):
            self.logger.debug(f"|| Publicando no topico {topic} AS {msg} ||")
            self.MqttListener.publish(topic,msg)

    def onDataReceived(self, topic, payload,logger=None):
        columns = ["consumo(minutos)", "id", "username", "data_inicio", "data_fim", "curso", "email"]
       

    

        if topic.endswith("filamento"):

            data = json.loads(payload)
            print(data)
            if not os.path.isfile("files/data_capture.txt"):
                with open("files/data_capture.txt", "w") as c:
                    c.write(f"{data['start_time']}, {data['end_time']}, {data['distance']}\n")
            else:
                with open("files/data_capture.txt", "a") as a:
                    a.write(f"{data['start_time']}, {data['end_time']}, {data['distance']}\n")
                
                
            """
            now_date = datetime.datetime.now()
            ffmt = "%H:%M:%S"
            str_now_date = now_date.strftime("%Y_%m_%d")
            
        
            slts = self.sl.slots()
            dd = {}
            for key, value in zip(columns, list(zip(*slts))):
                dd[key] = list(value)

            df = pd.DataFrame.from_dict(dd)

            #if file does not exist write header
            
            df = insert_row_distinct(df)
            

            df['consumo(minutos)'] = df['consumo(minutos)'].apply(lambda x: x.seconds/60)
            check = check_date_time(df)
            print(check)
            try:
                start = datetime.datetime.strptime(data['start_time'], ffmt)
                end = datetime.datetime.strptime(data['end_time'], ffmt)
                print(end-start)
            except:
                pass
            else:
                if not check.empty:
                    
                    print(alter_table(df, int(check.iloc[0]), data["distance"]))
                    
                    self.logger.debug(f"|| TABELA ATUALIZADA COM SUCESSO- NO ID {int(check.iloc[0])}")
                    
            self.logger.debug(f"|| mensagem recebidas {data} ||")
            if now_date.hour == 12:
                df.to_csv(f"files/{str_now_date}.csv", index=False)
            """



                
    



        
            

     
    
