#!/usr/bin/env python
#--*-- encoding:utf-8 --*--
# import netsnmp

if __name__=="__main__":
    print "snmp lib"
#     object_oid=".1.3.6.1.4.1.2021.11.9"
#     session = netsnmp.Session(DestHost="172.17.111.167",Version=2
#                         ,RemotePort=161,Timeout=60,Community="public")
#     result = session.walk(netsnmp.VarList(netsnmp.Varbind(object_oid)))
#     print result
    mac_item = ["\xA5\xF7\x02"]
    for item_mac in mac_item:
        print item_mac
        mac = ":".join(['%x'%ord(c) for c in item_mac])
        mac_result = ":".join(['%s' %_c if len(_c)>1 else '0'+_c for _c in mac.split(":")])
    print  mac_result
