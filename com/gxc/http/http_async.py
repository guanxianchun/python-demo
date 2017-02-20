#-*- encoding:utf-8 -*-
'''
Created on 2016��11��29��

@author: martin
'''
from tornado.httpclient import AsyncHTTPClient
from tornado import httpclient
import json,tornado,time,tornado.web,tornado.gen
def handler():
    body = json.dumps({
            "UserId":"zjuadmin",
            "RequestInfo": "QmPbPS7fA55qHn4n/8vH19wN362iDHLWApMjiN7F8ijqKuOA824onZq3FNEiz1qAs/BGDH/BRPyz1MVnHJWFBi3B5kiPwwFRIHN9Fq4ND1fxHqoMkd5Jc1rnll6kcgX3LyzXfuUuT7g3lisPPdNmJOGWjxYIYSvWO85y3fsKba8=",
            "AppCode": "H3C",
            "Expire": 120
        })
    request = httpclient.HTTPRequest(url="https://localhost:8080/v2/auth/token",method="POST",body=body,validate_cert=False)
    client = AsyncHTTPClient()
    response = yield tornado.gen.Task(client.fetch, request)
    if response.error:
        print "Error:", response.error
    else:
        print 'called'
        print response.body
    
def request(handler_request):
    yield handler_request()
    
@tornado.web.asynchronous
@tornado.gen.engine
def handler_response(result):
    body = json.dumps({
            "UserId":"zjuadmin",
            "RequestInfo": "QmPbPS7fA55qHn4n/8vH19wN362iDHLWApMjiN7F8ijqKuOA824onZq3FNEiz1qAs/BGDH/BRPyz1MVnHJWFBi3B5kiPwwFRIHN9Fq4ND1fxHqoMkd5Jc1rnll6kcgX3LyzXfuUuT7g3lisPPdNmJOGWjxYIYSvWO85y3fsKba8=",
            "AppCode": "H3C",
            "Expire": 120
        })
    print body
    request = httpclient.HTTPRequest(url="https://localhost:8080/v2/auth/token",method="POST",body=body,validate_cert=False)
    client = AsyncHTTPClient()
    response = yield client.fetch(request)
    if response.error:
        print "Error:", response.error
    else:
        print 'called'
        print response.body
if __name__ == '__main__':
    handler_response(1)
    tornado.ioloop.IOLoop.instance().start()
    