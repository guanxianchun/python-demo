#-*- encoding:utf-8 -*-
'''
Created on 2016年7月12日

@author: admin
'''
from pyhs import Manager,__version__
import memcache
if __name__ == '__main__':
    print 'ssss'
    read_servers = [('inet', '172.17.111.167', 9998), ('inet', '172.17.111.167', 9998)]
    #Manager(['172.17.111.167',])
    print __version__