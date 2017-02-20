#!/usr/bin/env python
#-*- encoding:utf-8 -*-
'''

时间: 2016年12月14日 上午10:40:51
@author: guan.xianchun
'''
import json

class H3CResultCode:
    Success = "success"
class CompareType:
    New = 1
    Update = 2
    Same = 3
    
class H3CTenantSync(object):
    def __init__(self):
        self._h3c_root_uri = ""#SingletonServiceConfig().get_value("ROOT_URI","H3C")
        self.userName = ""#SingletonServiceConfig().get_value("userName","H3C")
        self.password = "" #SingletonServiceConfig().get_value("password","H3C")
        self._token_uri = "/iclouds/v2/auth/token"
        self._tenant_uri = "/iclouds/v2/tenants/list"
        self.token_expire = 300
        self.host = None
        self.port = None
        self.MAX_COUNT = 20
        self.headers = {"Content-Type":"application/json;charset=utf-8","Accept":"application/json"}
        if self._h3c_root_uri:
            self.host = self._get_host()
            self.port = self._get_port()
            
    def _get_host(self):
        index = self._h3c_root_uri.find("//")
        if index <0:
            return None
        end_index = self._h3c_root_uri.find(":",index+2)
        if end_index<0:
            end_index = self._h3c_root_uri.find("/",index+2)
        if end_index<0:
            return None
        return self._h3c_root_uri[index+2:end_index]
    
    def _get_port(self):
        index = self._h3c_root_uri.find("//")
        if index<0:
            return None
        index = self._h3c_root_uri.find(":",index+2)
        if index <0:
            if self._is_https():
                return 443
            else:
                return 80
        end_index = self._h3c_root_uri.find("/",index+1)
        if end_index <0:
            return self._h3c_root_uri[index+1:]
        else:
            return self._h3c_root_uri[index+1:end_index]
        
    def _is_https(self):
        if "https" in self._h3c_root_uri.lower():
            return True
        return False
    
    def _get_json_data(self,response):
        json_data = json.loads(response.body)
        if "result" in json_data and json_data["result"]==H3CResultCode.Success:
            return json_data
        raise Exception("request error:%s"%(response.body))
    def _get_token(self):
        data = {
                "RequestInfo": h3c_encrypt(json.dumps({"loginName":self.userName,"password":self.password})),
                "AppCode": "AISHU"
            }
        if _is_https():
            response = HttpUtil.send_https_request(self.host, self.port, "POST", self._token_uri, self.headers, data, 120)
        else:
            response = HttpUtil.send_http_request(self.host, self.port, "POST", self._token_uri, self.headers, data, 120)
        if response.status ==200:
            json_data = self._get_json_data(response)
            if "result" in json_data and json_data["result"]==H3CResultCode.Success:
                return json_data["record"]["I_CLOUDOS_TOKEN"]
            else:
                raise Exception("Get H3C token error:%s"%(response.body))
        else:
            raise Exception("Get H3C token error:%s"%(response.body))
    def _get_sync_tenants(self,start,count):
        if _is_https():
            response = HttpUtil.send_https_request(self.host, self.port, "POST", self._tenant_uri, self.headers, data, 120)
        else:
            response = HttpUtil.send_http_request(self.host, self.port, "POST", self._tenant_uri, self.headers, data, 120)
        if response.status ==200:
            json_data = self._get_json_data(response)
            return json_data
        else:
            raise Exception("Get H3C tenants error:%s"%(response.body))
        
    def _get_db_tenants(self):
        return self.db_tenant.get_all_tenant(TenantAppCode.H3C)
    
    def compare(self,sync_tenant,local_tenant):
        compare_type = CompareType.New
        if sync_tenant["TenantAdminCode"] == local_tenant["Name"]:
            compare_type = CompareType.Update
            if local_tenant["DepartmentCode"]==sync_tenant["TenantId"] and local_tenant["Department"]==sync_tenant["TenantName"]:
                compare_type = CompareType.Same
        return compare_type
    
    def get_add_update_tenants(self,dbtenants,synctenants):
        add_tenants = []
        update_tenants = []
        same_tenants = []
        isFound = False
        for item in synctenants:
            isFound = False
            for dbitem in dbtenants:
                if item["TenantAdminCode"] == dbitem["Name"]:
                    isFound = True
                    compare_type = self.compare(item, dbitem)
                    if compare_type == CompareType.Update:
                        update_tenants.append(item)
                    elif compare_type == CompareType.Same:
                        same_tenants.append(item)
                    break
            if not isFound:
                add_tenants.append(item)
                
        return add_tenants,update_tenants,same_tenants
    
    def get_delete_tenants(self,dbtenants,synctenants):
        del_tenants = []
        isFound = False
        for dbitem in dbtenants:
            isFound = False
            for item in synctenants:
                if item["TenantAdminCode"] == dbitem["Name"]:
                    isFound = True
                    break
            if not isFound:
                del_tenants.append(dbitem)
        return del_tenants
    
    def sync_tenants(self):
        if is_none_empty(self._h3c_root_uri) or is_none_empty(self.host) or is_none_empty(self.port):
            return
        dbtenants = self._get_db_tenants()
        self.headers["I_CLOUDS_TOKEN"] = self._get_token()
        json_data = self._get_sync_tenants(0, 100)
        synctenants = json_data["record"]
        add_tenants,update_tenants,same_tenants = self.get_add_update_tenants(dbtenants,synctenants)
        del_tenants = self.get_delete_tenants(dbtenants, synctenants)
        self.add_tenants(add_tenants)
        self.update_tenants(update_tenants)
        self.del_tenants(del_tenants)
        self.update_tenants_server(same_tenants)
        
    def create_ab_user(self,server_info,user_name):
        ab_caller = AnybackupCaller(server_info["ServerId"], server_info['ServerIp'], 9801)
        ab_caller.create_tenant(user_name)
        
    def add_tenants(self,tenants):
        for item in tenants:
            try:
                server_info = self.get_server_info(item["MacList"])
                if not server_info or server_info is None:
                    continue
                self.create_ab_user(server_info, item['TenantAdminCode'])
                dic_tenant= {
                    'Name': item['TenantAdminCode'],
                    'CreateTime': datetime.datetime.now(),
                    'Status': TenantQuotaStatus.NOT_ASSIGNED,
                    'Scale':0,
                    'QuotaMonth':1,
                    'QuotaSpace':0,
                    'UsedSpace':0,
                    'Phone':"",
                    'Email':"",
                    'TenantAppCode':TenantAppCode.H3C,
                    'TenantType':item["TenantType"],
                    'DepartmentCode': item['TenantId'],
                    'Department': item['TenantName']
                }
                data = self.db_tenant.add_tenant(dic_tenant)
                dic_relation = {'TenantId':data['f_id'], 'RelationServerId':server_info["ServerId"]}
                self.db_tenant.add_tenant_server_relation(dic_relation)
            except:
                if data:
                    self.db_tenant.delete_tenant_by_id(data['f_id'])
                    self.db_tenant.delele_tenant_server_relation_by_tenant_id(data['f_id'])
                self.system_log.error(traceback.format_exc())
        
    def get_tenant_info_by_name(self,tenant_name):
        tenants = self.db_tenant.get_all_tenant_info(sync_tenant["TenantAdminCode"], 0, 10)
        if is_none_empty(tenants):
            return
        for item in tenants:
            if item["TenantType"] ==TenantAppCode.H3C:
                return item
            
    def update_tenant_server(self,tenant_id,sync_tenant):
        server_info = self.get_server_info(sync_tenant["MacList"])
        if not server_info or server_info is None:
            return
        db_result = self.db_tenant.get_relation_by_tenant_id(tenant_id)
        if is_none_empty(db_result):
            dic_relation = {'TenantId':tenant_info["Id"], 'RelationServerId':server_info["ServerId"]}
            self.create_ab_user(server_info, sync_tenant['TenantAdminCode'])
            self.db_tenant.add_tenant_server_relation(dic_relation)
            self.db_tenant.update_tenant_status_by_id(tenant_info["Id"], TenantQuotaStatus.NOT_ASSIGNED)
        elif db_result["RelationServerId"] != server_info["ServerId"]:
            dic_relation = {'TenantId':tenant_info["Id"], 'RelationServerId':server_info["ServerId"]}
            self.delete_ab_user(server_info, sync_tenant["TenantAdminCode"])
            self.db_tenant.delele_tenant_server_relation_by_server_id(db_result["RelationServerId"])
            self.create_ab_user(server_info, sync_tenant['TenantAdminCode'])
            self.db_tenant.add_tenant_server_relation(dic_relation)
            self.db_tenant.update_tenant_status_by_id(tenant_info["Id"], TenantQuotaStatus.NOT_ASSIGNED)
    def update_tenants(self,tenants):
        for item in tenants:
            try:
                tenant_info = self.get_tenant_info_by_name(item["TenantAdminCode"])
                if is_none_empty(tenant_info):
                    continue
                self.db_tenant.update_tenant_department(tenant_info["Id"], item["TenantId"], item["TenantName"])
                self.update_tenant_server(tenant_info["Id"],item)
            except:
                self.system_log.error(traceback.format_exc())
                
    def delete_ab_user(self,server_info,user_name,raise_exception=False):
        try:
            ab_caller = AnybackupCaller(server_info["ServerId"], server_info['ServerIp'], 9801)
            ab_caller.delete_tenant(user_name)
        except Exception as e:
            self.system_log.error('delete user form anybackup(%s) error:%s'%(server_info["ServerIp"],e.message))
            if raise_exception:
                raise e
            
        
    def del_tenants(self,tenants):
        for item in tenants:
            try:
                server_info = self.db_tenant.get_backup_node_by_tenant_id(item["Id"])
                if not server_info or server_info is None:
                    continue
                self.delete_ab_user(server_info, item['TenantAdminCode'])
                self.db_tenant.delele_tenant_server_relation_by_tenant_id(item["Id"])
                self.db_tenant.delete_tenant_by_id(item["Id"])
            except:
                self.system_log.error(traceback.format_exc())
                
    def update_tenants_server(self,tenants):
        for item in tenants:
            try:
                tenant_info = self.get_tenant_info_by_name(item["TenantAdminCode"])
                if is_none_empty(tenant_info):
                    continue
                self.update_tenant_server(tenant_info["Id"],item)
            except:
                self.system_log.error(traceback.format_exc())
    def get_server_info(self,maclist):
        for mac in maclist:
            db_mac = mac["MAC"].upper().replace("-",":")
            db_result = self.db_server_nic.get_backup_node_info_by_mac(db_mac)
            if db_result:
                return db_result
        return None

if __name__=="__main__":
    sync = H3CTenantSync()
    sync.sync_tenants()
    