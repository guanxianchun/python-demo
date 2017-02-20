from pysnmp.hlapi.asyncore import *


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBinds, cbCtx):
    if errorIndication:
        print(errorIndication)
        return
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBindTable[-1][int(errorIndex) - 1][0] or '?'))
        return
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


snmpEngine = SnmpEngine()

getCmd(snmpEngine,
       CommunityData('eisoo.com123'),
       UdpTransportTarget(('172.17.112.107', 161)),
       ContextData(),
       ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
       cbFun=cbFun)

snmpEngine.transportDispatcher.runDispatcher()

import threading
class TwistedThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
from twisted.internet.task import react
from pysnmp.hlapi.twisted import *


def success((errorStatus, errorIndex, varBinds), hostname,ret_result):
    print errorStatus
    if errorStatus:
        print('%s: %s at %s' % (hostname,
                                errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for name,val in varBinds:
            ret_result.append(val.prettyPrint())
        print ret_result

def failure(errorIndication, hostname):
    print('%s failure: %s' % (hostname, errorIndication))

from twisted.internet import protocol, reactor
# noinspection PyUnusedLocal
def getSysDescr(reactor, hostname):
    d = getCmd(SnmpEngine(),
               CommunityData('eisoo.com123'),
               UdpTransportTarget((hostname, 161)),
               ContextData(),
               ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.2.0')))
    ret_result = []
    d.addCallback(success, hostname,ret_result).addErrback(failure, hostname)
#     d.callback("sdfdsfd")
    print dir(d)
    print ret_result
    return d

# getSysDescr(reactor,'172.17.112.107')
import  time
start_time = time.time()
for i in range(1000):
    react(getSysDescr, ['172.17.112.107'])
print "******************************",time.time()-start_time