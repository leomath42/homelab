'''
    Arquivo de configurações v 0.1 via dicionário Python
    Arquivo de configurações v 0.2 será via xml
'''
import os
dir = os.getcwd()

config = \
{
    'engine_name' : "sqlite:////"+ dir +"/bancos/homelab.db?check_same_thread=False",
    'engine_echo' : True,
    'data_path': os.path.join(dir, "data")
}