#!/usr/bin/env python
#-*- coding:utf-8 -*-
import httplib,ssl,urllib,json,hmac,hashlib,base64,traceback
headers = {"Content-type": "application/json","Accept": "text/plain",
                        'Accept-Language':'zh-cn,zh;q=0.5'}

def get_token():
    try:
        host = raw_input("Input AB IP:")
        app_secret = raw_input("Input App Secret:")
        client_id = raw_input("Input App Id:")
        port = 9801
        signature = get_signature(app_secret)
        connect_open_api(client_id,signature,host,port)
    except:
        traceback.print_exc()
        
def get_signature(app_secret):
    method="GET"
    uri="/openapi/v1/application/access_token"
    decisive_element = base64.b64encode(str(method) + str(uri))
    return base64.b64encode(hmac.new(str(app_secret), decisive_element, hashlib.sha1).digest())

def connect_open_api(client_id,signature,host,port):
    try:
        uri_authorize = "/openapi/v1/application/access_token?client_id=%s&signature=%s"  %(client_id,signature)
        result = send_request("GET",uri_authorize,"",host,port)        
        access_token = result["access_token"]
        print host
        print "access_token="+access_token
    except:
        traceback.print_exc()
        
def send_request(method,uri,body,host,port):
    if hasattr(ssl,'_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    if isinstance(body, dict):
        body = json.dumps(body)
    if method.upper() in ('GET', 'DELETE'):
        body = None
    httpClient = httplib.HTTPSConnection(host,int(port))
    response = None
    try:
        httpClient.request(method,uri,body,headers)
        response = httpClient.getresponse()
        result = response.read()
        result = json.loads(result,"UTF-8")
        return result
    except:
        traceback.print_exc()
        
if __name__=="__main__":
    get_token()
