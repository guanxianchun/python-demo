#!/usr/bin/env python
#-*- coding:utf-8 -*-
import httplib,pdb,ssl,urllib,json
headers = {"Content-type": "application/json","Accept": "text/plain",
                        'Accept-Language':'zh-cn,zh;q=0.5'}
host = ""
def convert_unicode(value):
    """
    将字符转换为Unicode格式（中文字符处理）
    @param value
    @:return 返回转换的字符串  转换失败返回None
    """
    if not isinstance(value, unicode):
        try:
            value = value.decode("utf8")
        except UnicodeDecodeError:
            try:
                value = value.decode("gbk")
            except UnicodeDecodeError:
                return None
    return value
def connect():
    try:
        userName = 'admin'
        password = '123456'
        host = raw_input("input host ip:")
        port = '9801'
        login_anybackup(headers,host, port, userName, password)
        connect_open_api(userName,password,host,port)
    except Exception as ex:
        print "login fialed!!!"
        
def login_anybackup(headers, host, port, user, passwd):
    # ����ab6.0�ӿ�
    auth_uri = '/svr/local/users/login?userName=%s&userPwd=%s&userIp=%s' % (user, passwd, '127.0.0.1')
    result = ''
    try:
        result = send_request('GET',auth_uri,"",host,port)
    except Exception as e:
        raise e
    return result        
        
def connect_open_api(user_name,passwd,host,port):
    """
    #ͨ��open api���ӵ�AB�ڵ�
    @param user_name: �û���
    @param passwd: ����
    """
    try:
        uri = "/svr/local/applications"
        result = send_request("GET",uri,"",host,port)
        if result:
            client_id = result["result"][0]["appId"]
            authorize_status = result["result"][0]["status"]
            if not authorize_status:
                #û�п������ŷ�����Ȩ
                uri_open_authorize = "/svr/local/application/1"
                send_request("PUT", uri_open_authorize, "",host,port)
        else:
            return
        local_ip = "127.0.0.1"
        del headers["Cookie"]
        uri_authorize = "/openapi/v1/login_in?userName=%s&userPwd=%s&appId=%s&redirectUri=http://%s/response*HTTP/1.1"  %(user_name,passwd,client_id,local_ip)
        result = send_request("GET",uri_authorize,"",host,port)
        print result
        code = result.split("code=")[1]
        _body={
               "client_id":client_id,
               "code":convert_unicode(code).encode("utf-8"),
               "redirect_uri":"http://%s/response*HTTP/1.1" %(local_ip)
               }
        uri_access_token = "/openapi/v1/oauth2/access_token"
        result_access_token = send_request("POST",uri_access_token,_body,host,port)
        access_token = result_access_token["access_token"]
        print host
        print access_token
    except:
        import traceback
        traceback.print_exc()
        print "get access_token error!!!"
        
def send_request(method,uri,body,host=None,port=None):
    if hasattr(ssl,'_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    if isinstance(body, dict):
        body = json.dumps(body)
    if method.upper() in ('GET', 'DELETE'):
        body = None
    httpClient = httplib.HTTPSConnection(host,int(port))
    response = None
    try:
        print method, uri
        httpClient.request(method,uri,body,headers)
        response = httpClient.getresponse()
        result = response.read()
        import re
        if re.search("/svr/local/users/login", uri) or re.search("/openapi/v1/login_in", uri):
            headers["Cookie"] = response.getheader("set-cookie")
        if response.status != 200:
            print "get access_token error!!!"    
            print result
        if re.search("/openapi/v1/login_in", uri):
            return result    
        result = json.loads(result,"UTF-8")
        return result
    except:
        import traceback
        traceback.print_exc()
        print "get access_token error!!!"
        
if __name__=="__main__":
    connect()