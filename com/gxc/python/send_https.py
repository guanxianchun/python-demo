'''


@author: admin
'''
import hashlib, ssl, urllib, httplib, traceback
def send_https_request(host,port,method,uri,headers,body):
        if hasattr(ssl,'_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        if isinstance(body, dict):
            body = urllib.urlencode(body)
        if method.upper() in ('GET', 'DELETE'):
            body = None
        httpClient = httplib.HTTPSConnection(host,int(port))
        response = None
        try:
            print body
            httpClient.request(method,uri,body,headers=headers)
            response = httpClient.getresponse()
            return response
        except Exception as e:
            traceback.format_exc()
            raise e
if __name__ == '__main__':
    _body = {
        "code":"S6/fo4NCwWPFTnzaSnfQGDCOTt8=", 
        "client_id":"MTQ2NDIyNTY4Mi4xOA==", 
        "redirect_uri":"http://172.17.24.105/response*HTTP/1.1"
    }
    uri = "/openapi/v1/oauth2/access_token"
    import json,urllib2
    headers = {}
    jdata = json.dumps(_body)
    response = send_https_request("172.17.112.7", 9801, "POST", uri, headers, jdata)
    print response.read()
    
#     request = urllib2.Request("https://%s:%s%s"%("172.17.112.7",9801,uri),jdata)
#     request.get_method = lambda:"POST"
#     request = urllib2.urlopen(request)
#     print request.status
#     print request.read()
    