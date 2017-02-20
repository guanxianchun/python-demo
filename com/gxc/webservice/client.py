# --*-- encoding:utf-8 --*--
'''
Created on 2016年7月7日

@author: admin
'''
from suds import WebFault
from suds.client import Client
import json,urllib2
if __name__ == "__main__":
    wsdl_uri = "http://127.0.0.1:8085/xfire/service/bookservice?wsdl"
    wsdl_uri = "http://210.75.217.80:8080/S01A/ws/assetService?wsdl"
    wsdl_uri ="http://210.75.217.80:8080/S01A/ws/alarmService?wsdl"
    ws_client = Client(wsdl_uri)
    print ws_client
#     result =  ws_client.service.sayHello("")
    
#     send_data = [{ "id" :"55552", "name" :"MEM", "content":"告警内容详情","type":3,"typeName":"安全","level":"5","levelName" :"五级严重","time":"2015-01-01 01:01:01","ip":"192.168.123.110","deviceId" :"11111","mac" : "11-22-33-44-55-66","sourceCode" : "EISABC"}]
    send_data={"appCode": "EISABC", "type": "1", "appPassword": "EISABC", "data": [{"guaranteeDate": "", "nodeType": "\u5907\u4efd\u8282\u70b9", "nodeName": "221localhost.localdomain", "models": "\u7231\u6570\u5907\u4efd\u4e00\u4f53\u673a\u8282\u70b9\u670d\u52a1\u5668", "ip": "172.17.112.221", "brand": "\u7231\u6570", "state": "server.status.normal", "nodeId": "1", "alarmdays": "", "keeper": "", "mac": "ZDQ3DD51WRWPMRI1", "location": "", "sourceCode": "EISABC", "descrip": "\u5907\u4efd\u8282\u70b9:221localhost.localdomain", "department": "site01", "uniqueFlag": "20160905165246177000", "buyDate": "2016-09-05 16:52:46", "supplierName": "\u7231\u6570", "keepNumber": "", "usemonth": ""}, {"guaranteeDate": "", "nodeType": "\u4ecb\u8d28\u670d\u52a1\u5668", "nodeName": "221localhost.localdomain", "models": "\u7231\u6570\u5907\u4efd\u4e00\u4f53\u673a\u4ecb\u8d28\u670d\u52a1\u5668", "ip": "172.17.112.221", "brand": "\u7231\u6570", "state": "server.status.normal", "nodeId": "2", "alarmdays": "", "keeper": "", "mac": "ZDQ3DD51WRWPMRI1", "location": "", "sourceCode": "EISABC", "descrip": "\u4ecb\u8d28\u670d\u52a1\u5668:221localhost.localdomain", "department": "site01", "uniqueFlag": "20160905165246177000", "buyDate": "2016-09-05 16:52:46", "supplierName": "\u7231\u6570", "keepNumber": "", "usemonth": ""}, {"guaranteeDate": "", "nodeType": "\u5907\u4efd\u8282\u70b9", "nodeName": "localhost172.localdomain", "models": "\u7231\u6570\u5907\u4efd\u4e00\u4f53\u673a\u8282\u70b9\u670d\u52a1\u5668", "ip": "172.17.111.172", "brand": "\u7231\u6570", "state": "server.status.offline", "nodeId": "15", "alarmdays": "", "keeper": "", "mac": "FH6G2SCV9COQPDM6", "location": "", "sourceCode": "EISABC", "descrip": "\u5907\u4efd\u8282\u70b9:localhost172.localdomain", "department": "site01", "uniqueFlag": "20160905165246177000", "buyDate": "2016-09-05 16:52:46", "supplierName": "\u7231\u6570", "keepNumber": "", "usemonth": ""}, {"guaranteeDate": "", "nodeType": "\u4ecb\u8d28\u670d\u52a1\u5668", "nodeName": "localhost172.localdomain", "models": "\u7231\u6570\u5907\u4efd\u4e00\u4f53\u673a\u4ecb\u8d28\u670d\u52a1\u5668", "ip": "172.17.111.172", "brand": "\u7231\u6570", "state": "server.status.offline", "nodeId": "16", "alarmdays": "", "keeper": "", "mac": "FH6G2SCV9COQPDM6", "location": "", "sourceCode": "EISABC", "descrip": "\u4ecb\u8d28\u670d\u52a1\u5668:localhost172.localdomain", "department": "site01", "uniqueFlag": "20160905165246177000", "buyDate": "2016-09-05 16:52:46", "supplierName": "\u7231\u6570", "keepNumber": "", "usemonth": ""}, {"guaranteeDate": "", "nodeType": "\u4ecb\u8d28\u670d\u52a1\u5668", "nodeName": "abcloud-54.localdomain", "models": "\u7231\u6570\u5907\u4efd\u4e00\u4f53\u673a\u4ecb\u8d28\u670d\u52a1\u5668", "ip": "172.17.111.186", "brand": "\u7231\u6570", "state": "server.status.normal", "nodeId": "34", "alarmdays": "", "keeper": "", "mac": "ERHU24LHLGMG7DFK", "location": "", "sourceCode": "EISABC", "descrip": "\u4ecb\u8d28\u670d\u52a1\u5668:abcloud-54.localdomain", "department": "\u5317\u4eac\u9996\u4fe1\u5927", "uniqueFlag": "20160905165246177000", "buyDate": "2016-09-05 16:52:46", "supplierName": "\u7231\u6570", "keepNumber": "", "usemonth": ""}, {"guaranteeDate": "", "nodeType": "\u5907\u4efd\u8282\u70b9", "nodeName": "localhost.localdomain", "models": "\u7231\u6570\u5907\u4efd\u4e00\u4f53\u673a\u8282\u70b9\u670d\u52a1\u5668", "ip": "172.17.111.227", "brand": "\u7231\u6570", "state": "server.status.abnormal", "nodeId": "41", "alarmdays": "", "keeper": "", "mac": "01RXUDJ2BBB3GRZI", "location": "", "sourceCode": "EISABC", "descrip": "\u5907\u4efd\u8282\u70b9:localhost.localdomain", "department": "Default group", "uniqueFlag": "20160905165246177000", "buyDate": "2016-09-05 16:52:46", "supplierName": "\u7231\u6570", "keepNumber": "", "usemonth": ""}, {"guaranteeDate": "", "nodeType": "\u4ecb\u8d28\u670d\u52a1\u5668", "nodeName": "localhost.localdomain", "models": "\u7231\u6570\u5907\u4efd\u4e00\u4f53\u673a\u4ecb\u8d28\u670d\u52a1\u5668", "ip": "172.17.111.227", "brand": "\u7231\u6570", "state": "server.status.normal", "nodeId": "42", "alarmdays": "", "keeper": "", "mac": "01RXUDJ2BBB3GRZI", "location": "", "sourceCode": "EISABC", "descrip": "\u4ecb\u8d28\u670d\u52a1\u5668:localhost.localdomain", "department": "Default group", "uniqueFlag": "20160905165246177000", "buyDate": "2016-09-05 16:52:46", "supplierName": "\u7231\u6570", "keepNumber": "", "usemonth": ""}]}
    #告警数据
#     send_data = {"appCode": "EISABC", "type": 1, "appPassword": "EISABC", "data": [{"name": "", "level": "10", "ip": "172.17.111.227", "content": "\u8fde\u63a5\u4e0d\u7a33\u5b9a", "typeName": "\u8fde\u63a5\u4e0d\u7a33\u5b9a\u544a\u8b66", "mac": "01RXUDJ2BBB3GRZI", "deviceId": "41", "sourceCode": "EISABC", "time": "2016-09-05 17:03:42", "type": "alarm.type.connection", "id": "209", "levelName": "\u4e00\u822c"}], "alarmAppCode": "EISABC"}
    #消警数据
#     send_data = {"appCode": "EISABC", "type": 2, "appPassword": "EISABC", "data": [{"name": "\u8fde\u63a5\u4e0d\u7a33\u5b9a", "ip": "172.17.111.227", "mac": "01RXUDJ2BBB3GRZI", "time": "2016-09-05 17:03:42", "id": "209", "source": "EISABC"}], "alarmAppCode": "EISABC"}
    
   
    send_data = {"appCode": "EISABC", "type": 2, "appPassword": "EISABC", "data":[{"id" :"2","time" : "2015-01-01 01:01:01","ip":"192.168.123.110","mac" : "11-22-33-44-55-66","source" : "EISABC"}], "alarmAppCode": "EISABC"}
#     send_data = {"appCode": "EISABC", "type": 1, "appPassword": "EISABC", "data":[{"id" :"2","name" :"MEM","content":"告警内容详情","type":"3","typeName":"安全","level":5,"levelName" :"五级严重","time":"2015-01-01 01:01:01","ip":"192.168.123.110","deviceId" :"11111","mac" : "11-22-33-44-55-66","sourceCode" : "EISABC"}], "alarmAppCode": "EISABC"}

    print json.dumps(send_data)
#     result = ws_client.service.sendAllDeviceInfo(json.dumps(send_data))
#     result = ws_client.service.sendAlarmInfo(json.dumps(send_data))
    result = ws_client.service.recoveryAlarm(json.dumps(send_data))
    print result
    json_data = json.loads(result)
    print json_data["result"]
    print 3 * 1024 * 1024 * 1024

