#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
import traceback,threading,time
from tornado.websocket import WebSocketHandler
from tornado.options import define

define("port", default=11000, help="run on the given port", type=int)
import threading,time

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/v1/websocket/overview", DemoSocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class SendMessageThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        count=0
        while True:
            msg =self.getName()+":"+str(count)
            count+=1 
            DemoSocketHandler.update_cache(msg)
            DemoSocketHandler.send_updates(msg)
            time.sleep(5)
class DemoSocketHandler(WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200
    sendThread=None
    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        print self
        DemoSocketHandler.waiters.add(self)
        chat = {
            "id": str(self.__hash__()),
            "body":"connect",
        }
        DemoSocketHandler.update_cache(chat)
        
    def on_close(self):
        print 'close websocket',self
        DemoSocketHandler.waiters.remove(self)
        
    @classmethod
    def update_cache(cls, msg):
        print msg
        if isinstance(msg, dict) and "body" in msg and  msg["body"]=="connect":
            if cls.sendThread is None:
                cls.sendThread=SendMessageThread()
                cls.sendThread.setDaemon(True)
                cls.sendThread.start()
        cls.cache.append(msg)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]
        
    @classmethod
    def send_updates(cls, msg):
        if isinstance(msg, dict) and "body" in msg and  msg["body"]=="connect":
            return
        for waiter in cls.waiters:
            try:
                waiter.write_message(msg)
            except:
                traceback.print_exc()
    def on_message(self, message):
        dict_msg = {
            "id": str(self.__hash__()),
            "body":message,
            }
        DemoSocketHandler.update_cache(dict_msg)
        DemoSocketHandler.send_updates(dict_msg)

def main():
    tornado.options.parse_command_line()
    send=SendMessageThread()
    send.setDaemon(True)
    send.start()
    app = Application()
    app.listen(11000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
