#!/usr/bin/env python
#-*- encoding:utf-8 -*-
'''

时间: 2017年2月8日 下午2:02:15
@author: guan.xianchun
'''

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from concurrent.futures import ThreadPoolExecutor
import tornado.ioloop
import tornado.web
import os




    
class UploadFileHandler(tornado.web.RequestHandler):
    '''
    classdocs
    '''
    def post(self):
    #文件的暂存路径
        upload_path=os.path.join(os.path.dirname(__file__),'files')  
        #提取表单中‘name’为‘file’的文件元数据
        file_metas=self.request.files['file']    
        for meta in file_metas:
            filename=meta['filename']
            filepath=os.path.join(upload_path,filename)
            #有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath,'wb') as up:      
                up.write(meta['body'])
            self.write('finished!')
        
    def get(self):
        filename = self.get_argument("filename")
        print('i download file handler : ',filename)
        #Content-Type这里我写的时候是固定的了，也可以根据实际情况传值进来
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+filename)
        #读取的模式需要根据实际情况进行修改
        buf_size=1024
        with open("D:/develop/git/abcloud/deps/redis/"+filename, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        #记得有finish哦
        self.finish()
        
        
app=tornado.web.Application([
    (r'/file',UploadFileHandler),
])

if __name__ == '__main__':
#     app.listen(3000)
#     tornado.ioloop.IOLoop.instance().start()
    cloud = "Abcloud_Webconsole_bak_package_1.0.4.0.610_2016_09_18-00_00_00.cbp"
    import re
    m = re.search(r'(\.|\d)+', cloud)
    if m:
        print m.group()
    else:
        print 'not find'