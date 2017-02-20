from twisted.internet import reactor,task
from twisted.python.util import println
from pysnmp.hlapi.varbinds import CommandGeneratorVarBinds
from pysnmp.hlapi.twisted import UdpTransportTarget
from pysnmp.hlapi.twisted import SnmpEngine
from pysnmp.hlapi.twisted import CommunityData
from pysnmp.hlapi.twisted import ContextData
from pysnmp.hlapi.lcd import CommandGeneratorLcdConfigurator
from pysnmp.smi.rfc1902 import ObjectIdentity
from pysnmp.smi.rfc1902 import ObjectType
from pysnmp.smi.rfc1902 import ObjectType
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.proto.rfc1905 import endOfMibView
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure

vbProcessor = CommandGeneratorVarBinds()
lcd = CommandGeneratorLcdConfigurator()

class SnmpQueryError(Exception):
    pass


def printList(lst):
    print('\n'.join(map(str, lst)))


class OidVarbindCache(object):
    '''
    This will add an extra property to the oid
    '''

    
    def get(engine, oid):
        assert isinstance(oid, ObjectType)
        cache = getattr(engine, 'oidVarbindCache', None)
        if cache is None:
            cache = {}
            setattr(oid, 'oidVarbindCache', cache)

        varbinds = None
        oidTuple = getattr(oid, 'oidTupleCache', None)
        if oidTuple is None:
            if not oid.isFullyResolved():
                varbinds = vbProcessor.makeVarBinds(engine, (oid,))
            oidTuple = oid[0][:]._value


        if oidTuple in cache:
            varbinds = cache[oidTuple]
        else:
            varbinds = varbinds or vbProcessor.makeVarBinds(engine, (oid,))
            cache[oidTuple] = varbinds

        return varbinds, oidTuple


def testErrInTable(errorIndication, errorStatus, errorIndex, varBindTable):
    if errorIndication:
        raise SnmpQueryError('%s' % errorIndication)
    elif errorStatus:
        raise SnmpQueryError(
            '%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[int(errorIndex) - 1] or '?'
            )
        )

def __bulkSubTreeCmdcbFun(
        snmpEngine,
        sendRequestHandle,
        errorIndication,
        errorStatus,
        errorIndex,
        varBindTable,
        cbCtx):
    lookupMib, deferred, result, oidTuple, oidTupleLen, logValues = cbCtx

    try:
        testErrInTable(errorIndication, errorStatus, errorIndex, varBindTable)
    except Exception as ex:
        deferred.errback(Failure(ex))
    else:
        if varBindTable:
            moreLeft = True
            while varBindTable and (oidTuple != varBindTable[-1][0][0]._value[:oidTupleLen] or varBindTable[-1][0][0].isSameTypeWith(endOfMibView)):
                moreLeft = False
                varBindTable.pop()

            if logValues:
                for item in varBindTable:
                    print('{} = {}'.format(item[0][0].prettyPrint(), item[0][1].prettyPrint()))

            result.extend(varBindTable)
        else:
            moreLeft = False
        if not moreLeft:
            deferred.callback(result)
        return moreLeft


def bulkSubTreeCmd(
        snmpEngine,
        authData,
        transportTarget,
        contextData,
        nonRepeaters,
        maxRepetitions,
        oid,
        logValues=False,
        lookupMib=False):

    deferred = Deferred()

    varbinds, oidTuple = OidVarbindCache.get(snmpEngine, oid)
    oidTupleLen = len(oidTuple)
    addrName, paramsName = lcd.configure(snmpEngine, authData, transportTarget)

    cmdgen.BulkCommandGenerator().sendVarBinds(
        snmpEngine,
        addrName,
        contextData.contextEngineId,
        contextData.contextName,
        nonRepeaters,
        maxRepetitions,
        varbinds,
        __bulkSubTreeCmdcbFun,
        (lookupMib, deferred, [], oidTuple, oidTupleLen, logValues)
    )
    return deferred

engine = SnmpEngine()
transportTarget = UdpTransportTarget(transportAddr=('1.2.3.4', 161))
blankContextData = ContextData()

dfd = bulkSubTreeCmd(
    engine,
    CommunityData('public'),
    transportTarget,
    blankContextData,
    0, 15,
    ObjectType(ObjectIdentity('1.3.6.1.2.1'))
)
dfd.addCallback(printList)
dfd.addErrback(println)
dfd.addCallback(lambda _: reactor.stop())

reactor.run()
