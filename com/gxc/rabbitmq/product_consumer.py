#!/usr/bin/env python
#-*- encoding:utf-8 -*-
'''

时间: 2017年1月17日 下午4:04:17
@author: guan.xianchun
'''
import threading
import time
semaphore_consumer = threading.Semaphore(0)
semaphore_baozi = threading.Semaphore(0)
 
def producer():
    print u'chef:等人来买包子....'
    semaphore_consumer.acquire()
    print 'sb is coming for baozi'
    
    print 'chef is making baozi for sb...'
    time.sleep(5)
    semaphore_baozi.release()
    '''做包子中，等待。。。'''
    print u'you baozi 好了'
    
def consumer():
    
    print u'chentao:去买包子....'
    semaphore_consumer.release()
    print 'chentao:waiting for baozi to be ready...'
    semaphore_baozi.acquire()
    print u'Thanks....'
    
p1 = threading.Thread(target=producer)
c1 = threading.Thread(target=consumer)
p1.start()
c1.start()   