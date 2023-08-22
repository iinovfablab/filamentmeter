import datetime
import pandas as pd
import os

def convert_dt(dt) -> list():
    fdate = str(dt.datetime.now()).split()[0]
    fdate = list(map(lambda x: int(x), fdate.split('-')))
    return fdate

def reverse_key_to_value(d: list) -> dict:
    return dict(map(lambda x: x[::-1], d))


def read_file_list(level, path=False, dirname="files"):
    current_path = "\\".join(os.path.abspath(__file__).split('\\')[:-level])
    path_file = os.path.join(current_path, dirname)
    if not path:
        files = list(filter(lambda x: x.endswith(".xlsx"), os.listdir(os.path.abspath(path_file))))
        return files
    return path_file

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

def check_date_time(df) -> list:
    now = datetime.datetime.now()
    #fmt = "%Y-%m-%d %H:%M:%S"
    
    #actual_date = datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"), fmt)
    #actual_date = datetime.datetime.strptime(date_cmp,fmt)

    return df.loc[now >= df['data_inicio']].loc[now <= df['data_fim']]['id']


def alter_table(df, id, val) -> None:
    df.loc[df['id']==id, 'consumo_material(cm)'] = val