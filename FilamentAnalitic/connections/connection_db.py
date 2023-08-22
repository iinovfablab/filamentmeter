import psycopg2
from connections.connection_tunel import Connection


class ConnectionDB(Connection):
    __params = None
    __conn_db = None

    def params_db(self, file_params):
        self.__params = file_params

    def connection_db(self):
        
        conn_ssh = Connection() #alteração futura
        conn_ssh.connection(self.__params)
        conn_ssh.start()
        self.__params['db']['port'] = conn_ssh.params
        self.__conn_db = psycopg2.connect(**self.__params['db'])
        return self.__conn_db

    
