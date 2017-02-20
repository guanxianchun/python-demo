#-*- encoding:utf-8 -*-
import pika,json

class RabbitMQSend(object):
    def __init__(self,exchange,exchange_type,queue_name,routing_key,host=None, port=None, virtual_host=None,username=None,password = None,
                 channel_max=None,frame_max=None,heartbeat_interval=None,ssl=None,ssl_options=None,
                 connection_attempts=None,retry_delay=None,socket_timeout=None,locale=None,backpressure_detection=None):
        """
        :param str host: 连接RabbitMQ服务的主机名或主机IP
        :param int port: RabbitMQ服务器的端口  默认端口为5672或5671(ssl)
        :param str virtual_host: RabbitMQ使用的虚拟主机
        :param username: 用户名
        :param password: 密码
        :param queue_name: 消息队列名
        :param routing_key: 消息路由KEY
        :param int channel_max:允许的连接的最大通道数  默认不限制
        :param int frame_max: AMQP帧的最大字节数   默认是131072字节
        :param int heartbeat_interval: 默认由服务器来确定
        :param bool ssl: 是否使用SSL连接   默认不使用
        :param dict ssl_options: SSL连接参数
                ssl_options = {"cacerts": "/etc/rabbitmq/ssl/testca/cacert.pem",
                               "certfile": "/etc/rabbitmq/ssl/client/cert.pem",
                               "keyfile": "/etc/rabbitmq/ssl/client/key.pem",
                               "cert_reqs": CERT_REQUIRED,
                               "verify": "verify_peer",
                               "fail_if_no_peer_cert": True}
        :param int connection_attempts: 最大重连次数
        :param int|float retry_delay: Time to wait in seconds, before the next
        :param int|float socket_timeout: 端口超时时间，用于高延时网络
        :param str locale: 国际化语言 默认是en_US
        :param bool backpressure_detection: Toggle backpressure detection
        """
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.exchange = exchange
        self.exchange_type = exchange_type
        credentials = None
        if username is not None and password is not None:
            credentials = pika.credentials.PlainCredentials(username,password)
        #创建连接connection到rabbitmq server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, virtual_host,credentials,
                 channel_max,frame_max,heartbeat_interval,ssl,ssl_options,connection_attempts,retry_delay,
                 socket_timeout,locale,backpressure_detection))
        #创建虚拟连接channel
        self.channel = self.connection.channel()
        print self.channel
        channel = self.connection.channel()
        print channel
        #创建队列,durable参数为真时，队列将持久化；exclusive为真时，建立临时队列
        args = {} 
#         args = {"x-message-ttl":60000}
        result=self.channel.queue_declare(queue=self.queue_name,durable=True,exclusive=False,arguments=args)
        #创建名为$EXCHANGE_NAME的exchange，类型为topic，如果指定durable为真，exchange将持久化
        self.channel.exchange_declare(exchange=self.exchange,type=self.exchange_type)
        #绑定exchange和queue,result.method.queue获取的是队列名称
        self.channel.queue_bind(exchange=self.exchange,  queue=result.method.queue,routing_key=self.routing_key) 
        #公平分发，使每个consumer在同一时间最多处理一个message，收到ack前，不会分配新的message
        self.channel.basic_qos(prefetch_count=1)
        
    def send_message(self,message):
        """
                发送消息
        @param message: 要发送的消息   type : dict or str unicode
        """
        send_massage = ""
        if isinstance(message, dict):
            send_massage = json.dumps(message)
        else:
            send_massage = message
        #消息持久化指定delivery_mode=2
        self.channel.basic_publish(self.exchange, self.routing_key, send_massage, pika.BasicProperties(delivery_mode = 2,))
        
    def __del__(self):
        #关闭连接
        if self.connection:
            self.connection.close()
           
def get_tape_lib_msg():
    return {   
            "backup_server_ip": "192.168.100.100",
            "backup_server_machine_code": "MY86ZX7BUYE2Q1NL",
            "backup_server_guid": "SFMY86ZX7BUYE2Q1NLSDFSFADF",
            "backup_server_name": "infoworks1",
            "msg_type":7,
            "operator_type":4,
            "result":[{
                    "media_server_name": "localhost.redhat",
                    "media_server_ip": "192.168.100.100",
                    "media_server_machine_code": "MY86ZX7BUYE2Q1NL",
                    "media_server_guid": "sdfadsfdsafdsfdf3",
                    "tape_lib_list":[{
                            "tape_lib_name": "L700 0105",
                            "tape_lib_serial": "01RXUDJ2BBB3GRZI:XYZZY_A",
                            "tape_lib_media_path": "/dev/sg15",
                            "tape_lib_vendor": "STK",
                            "tape_lib_model": "[1:0:0:0]",
                            "tape_lib_slot_num": 43,
                            "tape_lib_driver_num": 6
                    },{
                            "tape_lib_name": "L700 0106",
                            "tape_lib_serial": "01RXUDJ2BBB3GRZI:XYZZY_AB",
                            "tape_lib_media_path": "/dev/sg16",
                            "tape_lib_vendor": "STK",
                            "tape_lib_model": "[1:0:0:0]",
                            "tape_lib_slot_num": 42,
                            "tape_lib_driver_num": 5
                    }]
            }]        
    }
def get_tenant_space_msg():
    message = {  
                "backup_server_ip": "192.168.100.100",
                "backup_server_machine_code": "MY86ZX7BUYE2Q1NL",
                "backup_server_name": "infoworks1",
                "msg_type":1,
                "operator_type":2,
                "backup_server_uuid": "SFMY86ZX7BUYE2Q1NLSDFSFADF", 
                "tenant_spaces":[{
                        "tenant_name": "zjuadmin",
                        "used_space":1000,
                        "usage_time":time.time(),
                    }]
            }
    return message

def get_tap_msg():
    return {
            "backup_server_ip": "192.168.100.100",
            "backup_server_machine_code": "MY86ZX7BUYE2Q1NL",
            "backup_server_guid": "SFMY86ZX7BUYE2Q1NLSDFSFADF",
            "backup_server_name": "infoworks1",
            "msg_type":8,
            "operator_type":4,
            "result":[{
                "media_server_name": "localhost.redhat",
                "media_server_ip": "192.168.100.100",
                "media_server_machine_code": "MY86ZX7BUYE2Q1NL",
                "media_server_guid": "sdfadsfdsafdsfdf3",
                "tape_tape_list":[{
                    "tape_lib_name": "L700 0105",
                    "tape_lib_serial": "01RXUDJ2BBB3GRZI:XYZZY_A",
                    "tape_list":[{
                        "tape_slot_id": 1,
                        "tape_volume_tag": "E01001L2"
                    },{
                        "tape_slot_id": 2,
                        "tape_volume_tag": "E01001L3"
                    }]
                }]
            }]
        }
    
def get_task_result_msg():
    return {
        "backup_server_ip": "192.168.100.100",
        "backup_server_machine_code": "MY86ZX7BUYE2Q1NL",
        "backup_server_guid": "SFMY86ZX7BUYE2Q1NLSDFSFADF",
        "backup_server_name": "infoworks1",
        "msg_auth_info": 'xxfsafe',
        "msg_type": 4,
        "operator_type": 4,
        "exec_job_list": [{
                "job_id": 1,
                "job_type": 1,
                "exec_job_id": 5,   
                "exec_job_type": 1,
                "backup_mode": 1,
                "exec_job_status": 32,
                "status_description": {
                    "status_code": "",
                    "status_message": "",
                },
                "exec_speed": 10240,
                "exec_complete_size": 10240000,
                "exec_start": 1486352564394438,
                "exec_end": 1486352564394438,
                "source_dest": [{
                    "source_node_id": 2,
                    "source_node_name": "localhost.centos",
                    "source_node_type": 2,
                    "source_node_ip": "192.168.100.102",
                    "source_node_machine_code": "XX86ZX7BUYE2Q1XX",
                    "source_node_guid": "d77b5011-2cf5-4dd8-a7fc-17023dd3bfca",
                    "source_node_status": 1,
                    "dest_node_id": 1,
                    "dest_node_name": "localhost.redhat",
                    "dest_node_type": 1,
                    "dest_node_ip": "192.168.100.101",
                    "dest_node_machine_code": "XX86ZX7BUYE2Q1YY",
                    "dest_node_guid": "4dad7da9-3f79-4d0d-a9b7-a3b6ab408930",
                    "dest_node_status": 1,
                }]
            }]
        }
    
def get_task_exec_msg():
    return  {
        "backup_server_ip": "192.168.100.100",
        "backup_server_machine_code": "MY86ZX7BUYE2Q1NL",
        "backup_server_guid": "SFMY86ZX7BUYE2Q1NLSDFSFADF",
        "backup_server_name": "infoworks1",
        "msg_auth_info": 'xxfsafe',
        "msg_type": 3,
        "operator_type": 4,
        "job_list": [{
            "job_id": "1",
            "job_name": "file_backup",
            "creation_time": 1121213432345,
            "modification_time": 1121213432375,
            "job_data_source_type": "@eisoo.com/backupengine/filebackupengine;1",
            "job_type": 1,
            "job_status": 1,
            "last_exec_time": 1213452333234567,
            "next_exec_time": 1213456543234567,
            "source_dest": [{
                "source_node_id": 2,
                "source_node_name": "localhost.centos",
                "source_node_type": 2,
                "source_node_ip": "192.168.100.102",
                "source_node_machine_code": "XX86ZX7BUYE2Q1XX",
                "source_node_guid": "d77b5011-2cf5-4dd8-a7fc-17023dd3bfca",
                "source_node_status": 1,
                "dest_node_id": 1,
                "dest_node_name": "localhost.redhat",
                "dest_node_type": 1,
                "dest_node_ip": "192.168.100.101",
                "dest_node_machine_code": "XX86ZX7BUYE2Q1YY",
                "dest_node_guid": "4dad7da9-3f79-4d0d-a9b7-a3b6ab408930",
                "dest_node_status": 1
            }]
        }, {
            "job_id": "2",
            "job_name": "dxxx",
            "creation_time": 1121213432345,
            "modification_time": 1121213432375,
            "job_data_source_type": "@eisoo.com/backupengine/filebackupengine;1",
            "job_type": 7,
            "job_status": 1,
            "last_exec_time": 0,
            "next_exec_time": 0,
            "source_dest": [{
                "source_node_id": 3,
                "source_node_name": "localhost.redhat2",
                "source_node_type": 9,
                "source_node_ip": "192.168.100.103",
                "source_node_machine_code": "XX86ZX7BUYE2Q1ZZ",
                "source_node_guid": "d77b5011-2cf5-4dd8-a7fc-17023dd3bfca",
                "source_node_status": 1,
                "dest_node_id": 2,
                "dest_node_name": "localhost.centos",
                "dest_node_type": 2,
                "dest_node_ip": "192.168.100.102",
                "dest_node_machine_code": "XX86ZX7BUYE2Q1XX",
                "dest_node_guid": "4dad7da9-3f79-4d0d-a9b7-a3b6ab408930",
                "dest_node_status": 1,
            }, {
                "source_node_id": 2,
                "source_node_name": "localhost.centos",
                "source_node_type": 2,
                "source_node_ip": "192.168.100.102",
                "source_node_machine_code": "XX86ZX7BUYE2Q1XX",
                "source_node_guid": "d77b5011-2cf5-4dd8-a7fc-17023dd3bfca",
                "source_node_status": 1,
                "dest_node_id": 1,
                "dest_node_name": "localhost.redhat1",
                "dest_node_type": 10,
                "dest_node_ip": "192.168.100.101",
                "dest_node_machine_code": "XX86ZX7BUYE2Q1YY",
                "dest_node_guid": "4dad7da9-3f79-4d0d-a9b7-a3b6ab408930",
                "dest_node_status": 1,
            }]
        }],
        "exec_job_list": [{
            "job_id": 1,
            "job_type": 1,
            "exec_job_id": 1,
            "exec_job_description": "auto start",
            "exec_job_type": 1,
            "backup_mode": 1,
            "exec_job_status": 32,
            "exec_speed": 10240,
            "exec_complete_size": 10240000,
            "exec_schedule": 100,
            "exec_start": 1486352564394438,
            "exec_end": 1486352564394438,
         }, {
            "job_id": 2,
            "job_type": 7,
            "exec_job_id": 2,
            "exec_job_description": "auto start",
            "exec_job_type": 7,
            "exec_job_status": 4,
            "exec_speed": 10240,
            "exec_complete_size": 10240000,
            "exec_schedule": 50,
            "exec_start": 1486352564394438,
            "exec_end": 0,
         }]
    }
import time
if __name__ == '__main__':
    queue_name = "SFMY86ZX7BUYE2Q1NLSDFSFADF"
    #queue_name = "abcloud"
    rabbitmq_send = RabbitMQSend(host="172.17.111.167",port=5672,username='abcloud',password='P@sswd4Eis00',queue_name=queue_name,
                                 routing_key=queue_name,exchange=queue_name,exchange_type="direct")
    count = 1
    while count>0:
        count -=1
#         rabbitmq_send.send_message(get_task_exec_msg())
        rabbitmq_send.send_message(get_task_result_msg())