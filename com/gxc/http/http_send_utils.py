#    /usr/bin/env python
#    coding:utf-8
import ssl,  httplib, traceback,json
from requests.auth import HTTPDigestAuth

class HttpUtil:
    
    @classmethod
    def send_http_request(cls, host,port,method,uri,headers,body):
        if isinstance(body, dict):
            body = json.dumps(body)
        if method.upper() in ('GET', 'DELETE'):
            body = None
        httpClient = httplib.HTTPConnection(host,int(port))
        response = None
        try:
            httpClient.request(method,uri,body,headers=headers)
            response = httpClient.getresponse()
            return response
        except Exception as e:
            traceback.print_exc()
            raise e
    @classmethod
    def send_https_request(cls,host,port,method,uri,headers,body):
        if hasattr(ssl,'_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        if isinstance(body, dict):
            body = json.dumps(body)
        if method.upper() in ('GET', 'DELETE'):
            body = None
        httpClient = httplib.HTTPSConnection(host,int(port))
        response = None
        try:
            httpClient.request(method,uri,body,headers=headers)
            response = httpClient.getresponse()
            return response
        except Exception as e:
            traceback.print_exc()
            raise e
        

        
if __name__ == "__main__":
    uri = '/v2/auth/token'
    import time
    body = {
            "UserId":"zjuadmin",
            "RequestInfo": "QmPbPS7fA55qHn4n/8vH19wN362iDHLWApMjiN7F8ijqKuOA824onZq3FNEiz1qAs/BGDH/BRPyz1MVnHJWFBi3B5kiPwwFRIHN9Fq4ND1fxHqoMkd5Jc1rnll6kcgX3LyzXfuUuT7g3lisPPdNmJOGWjxYIYSvWO85y3fsKba8=",
            "AppCode": "H3C",
            "Expire": 3
        }
    success_count = 0
    failure_count = 0
    _start_time = time.time()
    while True:
        try:
            response = HttpUtil.send_https_request('127.0.0.1', 8080, "POST", uri, {}, body)
            if response and response.status ==200:
                success_count+=1
            else:
                failure_count+=1
        except:
            failure_count+=1
        if time.time()-_start_time>60:
            break
    end_time = time.time()-_start_time
    print 'time:%s success request :%s'%(end_time,success_count)
    print 'time:%s failure request :%s'%(end_time,failure_count)
    print HTTPDigestAuth('user', 'pass')
    