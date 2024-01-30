import datetime
from typing import Any, Iterable
import pandas as pd
import os
from connections.connection_mongo import ConnectionMongo
import re

def convert_dt(dt) -> list():
    fdate = str(dt.datetime.now()).split()[0]
    fdate = list(map(lambda x: int(x), fdate.split('-')))
    return fdate

def reverse_key_to_value(d: list) -> dict:
    return dict(map(lambda x: x[::-1], d))



def insert_row_distinct(df):
    
    fuso = datetime.timedelta(hours=3)
    df[['data_inicio','data_fim']] = df[['data_inicio','data_fim']].apply(lambda x: x-fuso)
    df['consumo(minutos)'] = df['consumo(minutos)'].apply(lambda x: x.seconds/60)
    cv_int = lambda x: int(x.split(':')[1])
    #df['consumo(minutos)'] = df['consumo(minutos)'].apply(cv_int)
    df[['data_inicio','data_fim']] = df[['data_inicio','data_fim']].apply(pd.to_datetime)
    

    dfs = []
    #separa os id e username para empacotamento
    df_x = df[['id','username']].stack()
    
    #empacota (id,username)
    tl = len(df_x.unique())
    lt = []
    for c in range(0,tl,2):
        lt.append(tuple(df_x.unique()[c:c+2]))

    #filtra respectivos

    for id,name in lt:
        df_username = df.loc[df['username']==name]
        
        minn = df_username['data_inicio'].min()
        maxx = df_username['data_fim'].max()
        
        new_row = {"reserva(minutos)":df_username['consumo(minutos)'].sum(),
                   "tempo_de_maquina_usado(minutos)":0,
                   "id":id,
                   "username":name,
                   "data_inicio":[minn],
                   "data_fim":[maxx],
                   "curso":[df_username["curso"].unique()[0]],
                   "email":[df_username['email'].unique()[0]],
                   "consumo_material(cm)":[0]
                  }
        
        dfs.append(pd.DataFrame.from_dict(new_row))
    
    dfT = pd.concat(dfs, ignore_index=True)
    dfT.to_excel("oi.xlsx")
    return dfT



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
    
    
    for row in range(df.shape[0]):
        manga.mongo['collection1'].insert_one(df.iloc[row,:].to_dict())
    
    manga.disconnect()


def convert_dict_datetime(data):
    keys_ = ['start_time', 'end_time']
    for k in keys_:
        data[k] = datetime.datetime.strptime(data[k], "%Y-%m-%d %H:%M:%S")
    
    return data

def replace_date_to_datetime(d):
    dt = list(map(lambda x: int(x),re.split("-| |:", d)))
    return datetime.datetime(*dt)

def check_alter(date):
    
    mongo = ConnectionMongo()
    all_distances = mongo.mongo['collection2'].find({"distance":{"$gte":1}})
    all_users = mongo.mongo['collection1'].find({"start_time"})
    all_distances = list(map(convert_dict_datetime, all_distances))

    print(mongo.mongo['collection1'].find({"$gte":1}))

    for dates in all_distances:
        
        #consumption = mongo.mongo['collection1'].find_one({"$and":[{"data_inicio":{"$gte":dates['start_time']}}, 
                                                        #{"data_fim":{"$lte":dates['end_time']}}]})["consumo_material(cm)"]

        #mongo.mongo['collection1'].find_one_and_update({"$and":[{"data_inicio":{"$gte":dates['start_time']}}, 
                                                                #{"data_fim":{"$lte":dates['end_time']}}]},
                                                                #{"$set":{"consumo_material(cm)":dates['distance']+consumption}})
        pass

    mongo.disconnect()



        
    


