# -*- coding: utf-8 -*-
import paramiko
import os
import configparser

config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config.read(os.path.join(BASE_DIR, 'config.ini'))
para_hostname = config.get('para', 'hostname')
para_port = config.get('para', 'port')
para_user = config.get('para', 'user')
para_password = config.get('para', 'password')
file_src = config.get('file', 'src')
file_dst = config.get('file', 'dst')

__all__ = ['ParaApi']


class ParaApi:
    def __init__(self):
        self.hostname = para_hostname
        self.port = int(para_port)
        self.username = para_user
        self.password = para_password
        self.__transport = self.connect()

    def connect(self):
        transport = paramiko.Transport((self.hostname, self.port))
        transport.connect(username=self.username, password=self.password)
        return transport

    def upload(self, jobname):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        print(os.path.join(file_src, jobname), os.path.join(file_dst, jobname))
        sftp.put(os.path.join(file_src, jobname), os.path.join(file_dst, jobname))

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode('utf-8').strip('\n')
        err = stderr.read().decode('utf-8').strip('\n')
        return result, err

    def close(self):
        self.__transport.close()


if __name__ == '__main__':
    pass
