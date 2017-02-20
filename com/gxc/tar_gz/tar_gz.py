#!/usr/bin/env python
#-*- encoding:utf-8 -*-
'''

时间: 2017年2月17日 上午11:31:07
@author: guan.xianchun
'''
import tarfile
def get_tar_gz_file_names(file_name):
    with tarfile.open(file_name,"r:gz") as tar:
        filenames = tar.getnames()
        return filenames

def get_tar_gz_files(file_name):
    with tarfile.open(file_name,"r:gz") as tar:
        name_list = []
        for item in tar:
            file_name = item.name.split('/')[-1:]
            if file_name:
                name_list.append(tuple(file_name)[0])
if __name__ == '__main__':
    import time
    file_name = "E:/software/MinGW/Abcloud_Webconsole_bak_package_1.0.10.0.774_2017_02_13-11_58_51.cbp"
    
    
    _start_time = time.time()
    get_tar_gz_files(file_name)
    print time.time()-_start_time
    
    _start_time = time.time()
    get_tar_gz_file_names(file_name)
    print time.time()-_start_time