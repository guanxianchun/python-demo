#--*-- encoding:utf-8 --*--
'''
Created on 2016��7��4��

@author: admin

'''
import logging

class Writer(object):
    def __init__(self, store_type, store):
        self._store_type = store_type
        self._store = store

    def write(self, content):
        pass


class STDLogWriter(Writer):
    def __init__(self, store_type, store):
        logging.root.handlers=[]
        Writer.__init__(self, store_type, store)
        print 'self._store:',self._store
        logging.basicConfig(level=logging.INFO,
                            format = '%(asctime)s %(message)s',
                            datefmt  = '%m-%d %H:%M:%S',
                            filename = self._store)
        self._logger = logging.getLogger(self._store)
        
        print 'self._logger.name',self._logger.name

    def write(self, content):
        print "self._logger",self._logger,self._logger.name,content
        self._logger.info(content)
if __name__=="__main__":
    writer = STDLogWriter("log","111.log")
    writer.write("ddddddddddddddddddddddddd")
    writer = STDLogWriter("log","222.log")
    writer.write("ffffffffffffffffffffffffffffff")
    logging.getLogger("22222222222").info("aaaaaaaaaaaaaaaaaaa")
    logging.getLogger("3333333333333").info("ssssssssssssssssssss")