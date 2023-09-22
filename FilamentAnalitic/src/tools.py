import datetime
from typing import Any, Iterable
import pandas as pd
import os
from connections.connection_mongo import ConnectionMongo

def convert_dt(dt) -> list():
    fdate = str(dt.datetime.now()).split()[0]
    fdate = list(map(lambda x: int(x), fdate.split('-')))
    return fdate

def reverse_key_to_value(d: list) -> dict:
    return dict(map(lambda x: x[::-1], d))



def insert_row_distinct(df):
    fuso = datetime.timedelta(hours=3)
    df[['data_inicio','data_fim']] = df[['data_inicio','data_fim']].apply(lambda x: x-fuso)
    #cv_int = lambda x: int(x.split(':')[1])
    
    df[['data_inicio','data_fim']] = df[['data_inicio','data_fim']].apply(pd.to_datetime)
    

    dfs = []
    #separa os id e username para empacotamento
    df_x = df[['id','username']].stack()
    
    #empacota (id,username)
    tl = len(df_x.unique())
    lt = []
    for c in range(0,tl,2):
        lt.append(tuple(df_x.unique()[c:c+2]))

    #filstra respectivos

    for id,name in lt:
        df_username = df.loc[df['username']==name]
        
        minn = df_username['data_inicio'].min()
        maxx = df_username['data_fim'].max()
        
        new_row = {"consumo(minutos)":df_username['consumo(minutos)'].sum(),
                   "id":id,
                   "username":name,
                   "data_inicio":[minn],
                   "data_fim":[maxx],
                   "curso":[df_username["curso"].unique()[0]],
                   "email":[df_username['email'].unique()[0]],
                   "consumo_material(cm)":[0]
                  }
        
        dfs.append(pd.DataFrame.from_dict(new_row))
        
    return pd.concat(dfs, ignore_index=True)



def check_if_exists(df) -> Any:

    manga = ConnectionMongo()
    
    for r in df.iloc[:,0]:
        result = manga.query({"id":{"$eq":r}})
        if not r in result:
            manga.disconnect()
            return r
             
    manga.disconnect()
    return False

def first_insert(df) -> Iterable:
    manga = ConnectionMongo()
 
    for row in range(df.ndim):
        manga.mongo['collection1'].insert_one(df.iloc[row,:].to_dict())
    
    manga.disconnect()


def convert_dict_datetime(data):
    keys_ = ['start_time', 'end_time', 'date-time']
    for k in keys_:
        if k.endswith('time'):
            data[k] = datetime.datetime.strptime(data[k], "%Y-%m-%d %H:%M:%S")
    
    return data

def check_alter():
    
    mongo = ConnectionMongo()
    all_distances = mongo.mongo['collection2'].find({"distance":{"$gte":1}})

    for dates in all_distances:
        consumption = mongo.mongo['collection1'].find_one({"$and":[{"data_inicio":{"$gte":dates['start_time']}}, 
                                                          {"data_fim":{"$lte":dates['end_time']}}]})["consumo_material(cm)"]

        mongo.mongo['collection1'].find_one_and_update({"$and":[{"data_inicio":{"$gte":dates['start_time']}}, 
                                                                {"data_fim":{"$lte":dates['end_time']}}]},
                                                                {"$set":{"consumo_material(cm)":dates['distance']+consumption}})
        
    


