'''
import ipaddress


ip = "192.168.1.m9"


try :
    x = ipaddress.ip_address(ip)
    print(x)
except Exception as a:
    print(a)
'''

from threading import *
from pythonping import ping
import time


def pingo(IP):
    check = ping(IP, count=2)
    if check.success():
        print('UP')
    else:
        print('Down')
