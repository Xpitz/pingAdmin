# -*- coding: utf-8 -*-
import requests
import json
import os
import configparser

# 使用requests请求https出现警告，做的设置
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config.read(os.path.join(BASE_DIR, 'config.ini'))
salt_url = config.get('salt', 'url')
salt_user = config.get('salt', 'user')
salt_password = config.get('salt', 'password')

__all__ = ['SaltApi']


class SaltApi:
    def __init__(self):
        self._url = salt_url
        self._username = salt_user
        self._password = salt_password
        self._token = ''
        self._headers = {"Content-type": "application/json"}
        # 默认为glob，可选（glob,pcre,list,grain,grain_pcre,pillar,pillar_pcre,range,compound)
        self.expr_form = 'glob'

    def _get_token_id(self):
        """登录 salt API 获取 token 认证"""
        params = {'eauth': 'pam', 'username': self._username, 'password': self._password}
        result = self.get_data(params, prefix="/login")
        if result:
            self._token = result['token']
            return self._token
        else:
            return None

    def get_data(self, params, prefix="/"):
        self._headers.update({'X-Auth-Token': self._token})
        url = self._url + prefix
        send_data = json.dumps(params)
        try:
            request = requests.post(url, data=send_data, headers=self._headers, verify=False)
            if request.status_code == 200:
                response = request.json()
                result = dict(response)
                return result['return'][0]
            else:
                print('命令参数: ', params)
                print("访问失败，状态码：{status_code}".format(status_code=request.status_code))
                return None
        except requests.exceptions.ConnectionError as e:  # 网络不可达
            print(e)
            exit()

    def list_all_key(self):
        self._get_token_id()
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        result = self.get_data(params)
        if result:
            minions = result['data']['return']['minions']
            minions_pre = result['data']['return']['minions_pre']
            return minions, minions_pre

    def test_ping(self, tgt):
        """
        批量服务器ping测试
        :param tgt: minion id，多个id已逗号分隔，例如："test01,test02"
        :return:
        """
        ''' test.ping '''
        self._get_token_id()
        params = {'client': 'local', 'tgt': tgt, 'expr_form': 'list', 'fun': 'test.ping'}
        result = self.get_data(params)
        if result:
            return result

    def grains_items(self, tgt):
        """ 获取主机信息 """
        self._get_token_id()
        params = {'client': 'local', 'tgt': tgt, 'expr_form': 'list', 'fun': 'grains.items'}
        result = self.get_data(params)
        if result:
            return result

    def cmd_run(self, tgt, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        self._get_token_id()
        params = {'client': 'local', 'expr_form': 'list', 'fun': 'cmd.run', 'tgt': tgt, 'arg': arg}
        result = self.get_data(params)
        if result:
            return result

    def command_run(self, tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        self._get_token_id()
        if arg:
            params = {'client': 'local',  'expr_form': 'list', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local',  'expr_form': 'list', 'fun': method, 'tgt': tgt}
        result = self.get_data(params)
        return result


if __name__ == '__main__':
    pass
