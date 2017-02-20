#-*- encoding:utf-8 -*-
'''
Created on 2016年10月26日

@author: martin
'''
from rabbitmq_product import RabbitMQSend
if __name__ == '__main__':
    rabbitmq_send = RabbitMQSend(host="localhost",port=5672)
    message = {   
            "backup_server_ip": "192.168.100.100",
            "backup_server_machine_code": "MY86ZX7BUYE2Q1NL",
            "backup_server_name": "infoworks1",
            "msg_type":1,              
            "operator_type":1,           
            "servers":[{
                  "id":1,
                  "guid":"sdfadsfdsafdsfdf",
                  "name":"localhost.centos",
                  "server_type":3,            
                  "ip":"172.17.112.27",
                  "machine_code":"XX86ZX7BUYE2Q1ZZ",
                  "version":"5.0.1.0.2315",
                  "os_version": "centos 6",
                  "status": 0,         
                  "except_type":1
                 }]
        }
    rabbitmq_send.send_message(message)