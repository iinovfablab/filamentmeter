from sshtunnel import SSHTunnelForwarder


class Connection:
    __server = None

    @property
    def params(self):
        return self.__server.local_bind_port
   
    def connection(self, parameter):
        
        #print(port(parameter['ssh']["ip/port"] ,parameter['ssh']['root'], parameter['ssh']['password'], command))
        self.__server = SSHTunnelForwarder(
            tuple(parameter['ssh']["ip/port"]),
            ssh_username=parameter['ssh']['root'],
            ssh_password=parameter['ssh']['password'],
            remote_bind_address=(parameter['ssh']['remote_addres'][0],
                                    parameter['ssh']['remote_addres'][1]))

    def commands(self, command:str) -> str:

        return self.__server.exec_command(command)
        
    def start(self):
        self.__server.start()
        
