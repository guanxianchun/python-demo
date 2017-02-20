#!/usr/bin/env python
#-*- encoding:utf-8 -*-
'''

时间: 2016年12月13日 上午9:45:39
@author: guan.xianchun
'''
import ssl,  httplib, traceback,json
import hmac,time,uuid
import hashlib
import base64
def get_euop_signature(method, uri, access_key, expires, body_str=''):
    """获取euop 签名
    @:param method http调用方法大写，GET POST
    @:param uri 接口名称
    @:param access_key
    @:param expires  unix 时间戳 如'1477992604'"""
    string_2_sign = ''.join([method, '\n', expires, '\n', uri, '\n', body_str])
    signature = base64.urlsafe_b64encode(hmac.new(access_key, string_2_sign, hashlib.sha1).digest())
    return signature

class HttpUtil:
    
    @classmethod
    def send_http_request(cls, host,port,method,uri,headers,body,timeout=None):
        if isinstance(body, dict):
            body = json.dumps(body)
        if method.upper() in ('GET', 'DELETE'):
            body = None
        if timeout:
            httpClient = httplib.HTTPConnection(host,int(port), timeout=timeout)
        else:
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
    def send_https_request(cls,host,port,method,uri,headers,body,timeout=None):
        if hasattr(ssl,'_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        if isinstance(body, dict):
            body = json.dumps(body)
        if method.upper() in ('GET', 'DELETE'):
            body = None
        if timeout:
            httpClient = httplib.HTTPSConnection(host,int(port),timeout=timeout)
        else:
            httpClient = httplib.HTTPSConnection(host,int(port))
        response = None
        try:
            httpClient.request(method,uri,body,headers=headers)
            response = httpClient.getresponse()
            return response
        except Exception as e:
            traceback.print_exc()
            raise e
        
def get_local_mac_addr():
    """
    获取本地IP对应的网卡MAC地址
    注（风险）：在windows下，如果有虚拟网卡，取得的mac地址可能是虚拟网卡的地址
        同时多网卡情况下，有可能取得的数据会不同
    @:return 返回本地IP对应的网卡MAC地址
    """
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    _mac = ""
    for i  in range(len(mac)/2):
        _mac +=mac[i*2:i*2+2]+":"
    _mac = _mac[:-1]
    return _mac

def get_abc_identity_for_euop():
    mac = get_local_mac_addr()
    strhash = hashlib.md5(mac).hexdigest()
    midlen = len(strhash) / 2
    machine_code = ''
    strmode = '0123456789ABCDEFGHIJKLMNOPQRSTUV'
    for i in range(midlen):
        n = ord(strhash[i])
        m = ord(strhash[midlen + i])
        machine_code += strmode[(m ^ n) - n & 0x1f]
    return machine_code
        
if __name__ == "__main__":
    method = "GET"
    euop_addr=""
    uri = "/v1/euop_abc_msp/quota"
    access_key=""
    access_id="access_id"
    expires = str(int(time.time())+20)
    abc_identify = get_abc_identity_for_euop()
    signature = get_euop_signature(method, uri, access_key, expires,body_str='')
    url = uri + '?' + "access_id=%s&signature=%s&expires=%s&identity=%s" %(access_id, signature, expires, abc_identify)
    https_rep = HttpUtil.send_https_request(euop_addr, euop_port, method, url, {}, '',timeout=5)
    status = https_rep.status
    response = json.loads(https_rep.read())