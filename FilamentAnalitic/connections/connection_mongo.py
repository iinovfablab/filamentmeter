from typing import Any
import pymongo



class ConnectionMongo:

    mongo = {}

    def __init__(self) -> None:
        self.mongo['client'] =  pymongo.MongoClient("mongodb://localhost:27017")
        self.mongo['db'] = self.mongo['client']['inovfablab']
        self.mongo['collection1'] = self.mongo['db']['finder1']
        self.mongo['collection2'] = self.mongo['db']['schedules_use_finder1']


    def query(self, q:dict, collection) -> Any:
        result = self.mongo[collection].find(q)
        self.disconnect()
        return result

    
    def query_update(self, q:dict, updated:dict, collection) -> None:
        self.mongo[collection].find_one_and_update(q, updated)
        self.disconnect()
    

    def disconnect(self) -> None:
        self.mongo['client'].close()