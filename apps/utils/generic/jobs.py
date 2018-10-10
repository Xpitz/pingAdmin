import os
import configparser

from utils.remote.para import *

config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config.read(os.path.join(BASE_DIR, 'config.ini'))
file_src = config.get('file', 'src')
file_dst = config.get('file', 'dst')


def generate_job_file(data):
    with open(file_src + data.get('name'), 'w', newline="\n", encoding='utf-8') as f:
        content = data.get('content').replace('\r\n', '\n')
        f.write(content)


def push_job_file(job_name_list):
    para = ParaApi()
    for job_name in job_name_list:
        para.upload(jobname=job_name)

    para.close()
