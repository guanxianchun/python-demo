#-*- encoding:utf-8 -*-
'''
Created on 2016年7月13日

@author: admin
'''
import websocket

def on_message(ws,message):
    print 'client rev message:',message
    
if __name__ == '__main__':
    websocket.enableTrace(True)
    url ="ws://172.17.111.153:1080/chatsocket"
    ws = websocket.WebSocketApp(url,on_message=on_message)
    ws.run_forever()