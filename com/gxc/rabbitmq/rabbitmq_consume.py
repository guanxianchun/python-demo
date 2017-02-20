#-*- encoding:utf-8 -*-
import pika,time
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

EXCHANGE_NAME='abcloud'
MESSAGE_TYPE = 'topic'
ROUTING_KEY = "abcloud"
QUEUE_NAME = 'abcloud'

import threading,time
#定义回调函数
def consume_message(ch, method, properties, body):
    print "Received message :%s" % (convert_unicode(body))
    print 'delivery_tag=',method.delivery_tag
    time.sleep(1)
    ch.basic_ack(delivery_tag = method.delivery_tag)
class MessageClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        #建立连接connection到localhost
        con = pika.BlockingConnection(pika.ConnectionParameters("172.17.111.167", 5672, None,pika.credentials.PlainCredentials("abcloud","P@sswd4Eis00")))
        #创建虚拟连接channel
        cha = con.channel()
        #创建队列anheng
        result=cha.queue_declare(queue=QUEUE_NAME,durable=True)
        #创建名为yanfa,类型为fanout的交换机，其他类型还有direct和topic
        cha.exchange_declare(exchange=EXCHANGE_NAME,type=MESSAGE_TYPE)
        #绑定exchange和queue,result.method.queue获取的是队列名称
        cha.queue_bind(exchange=EXCHANGE_NAME, queue=result.method.queue, routing_key=ROUTING_KEY)
        #公平分发，使每个consumer在同一时间最多处理一个message，收到ack前，不会分配新的message
        cha.basic_qos(prefetch_count=1)
        print '**************************start consume message..**************************************'
        cha.basic_consume(consume_message,queue=QUEUE_NAME,no_ack=False)
        cha.start_consuming()
if __name__ == '__main__':
    messageClient = MessageClientThread()
    messageClient.setDaemon(True)
    messageClient.start()
    count = 1000
    while count>0:
        time.sleep(2)
        count=count-1
