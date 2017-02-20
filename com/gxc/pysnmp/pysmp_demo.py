# /usr/bin/env python
#encoding=utf-8

__author__ = 'guan.xianchun'
from pysnmp.entity.rfc3413.oneliner import cmdgen
class SnmpSession(object):
    
    def __init__(self,host_ip,port,community):
        self.cmdGen = cmdgen.CommandGenerator()
        self.host_ip = host_ip
        self.port = int(port)
        self.community_data = cmdgen.CommunityData(community)
        self.udpTransportTarget= cmdgen.UdpTransportTarget((self.host_ip, self.port))
    
    def get_object_info(self,oid):
        result = []
        errorIndication, errorStatus, errorIndex, varBinds = self.cmdGen.getCmd(
             self.community_data,self.udpTransportTarget,oid,)
        if errorIndication:
            raise Exception('get snmp object error:%s'%(errorIndication))
        else:
            if errorStatus:
                raise Exception('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[-1][int(errorIndex)-1] or '? '))
            else:
                    for name,val in varBinds:
                        result.append(val.prettyPrint())
        return result
    

    def get_objects_info(self,oids):
        result = []
        errorIndication, errorStatus, errorIndex, varBinds = self.cmdGen.getCmd(
             self.community_data, self.udpTransportTarget,*oids)
        if errorIndication:
            raise Exception('get snmp object error:%s'%(errorIndication))
        else:
            if errorStatus:
                raise Exception('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[-1][int(errorIndex)-1] or '? '))
            else:
                    for name,val in varBinds:
                        result.append(val.prettyPrint())
        return result

    def walk_object_info(self,oid):
        result = []
        errorIndication, errorStatus, errorIndex, varBindTable = self.cmdGen.bulkCmd(
             self.community_data, self.udpTransportTarget,0, 25,oid)
        if errorIndication:
            raise Exception('walk snmp object error %s'%(errorIndication))
        else:
            if errorStatus:
                raise Exception('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBindTable[-1][int(errorIndex)-1] or '? '))
            else:
                    for varBinds in varBindTable:
                        for name,val in varBinds:
                            result.append(val.prettyPrint())
        return result
import threading,time
class SnmpThread(threading.Thread):
    def __init__(self,host_ip,port,community):
        threading.Thread.__init__(self)
        self.snmp_session = SnmpSession(host_ip,port,community)
        
    def run(self):
        while True:
            count = 5
            while count >=0:
                print self.snmp_session.walk_object_info('.1.3.6.1.2.1.2.2.1.2')
                count = count-1
                time.sleep(1)
            time.sleep(5)
if __name__=="__main__":
    host_ips = ['172.17.112.107','172.17.111.184','172.17.112.18','172.17.112.12','172.17.112.7','192.168.245.19']
#     for i in range(5):
#         for j in range(len(host_ips)):
#             snmpThread = SnmpThread(host_ips[j],161,'eisoo.com123')
#             snmpThread.setDaemon(True)
#             snmpThread.start()
#     start = time.time()
#     while time.time()-start<600:
#         time.sleep(10)
    print SnmpSession(host_ips[len(host_ips)-1], 161, 'eisoo.com123').walk_object_info('.1.3.6.1.2.1.2.2.1.2')