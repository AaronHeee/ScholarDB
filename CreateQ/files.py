# encoding=utf-8

#create by aaron

import zipfile
import re
import os

def divide_file(path,zip_name):
    num = 0
    flag = 0
    zip_path = os.path.join(path,zip_name)
    total_file = zipfile.ZipFile(zip_path.encode('utf-8'),'r')
    file_list = total_file.namelist()
    length = len(file_list)

    if length == 0:
        return {'num': 0}

    temp_path = os.path.join(path,"temp").encode('utf-8')
    for file in file_list:
        total_file.extract(file.encode('utf-8'),temp_path)

    #将文件分割成若干份，每份中有100个待标记数据

    for root,dirs,files in os.walk(temp_path):

        count = -1 #why no zero
        cycle = 0
        path_archive = path + "/%d" % cycle + ".zip"
        zipFile = zipfile.ZipFile(path_archive.encode('utf-8'), 'w')

        for filename in files:
            if count == 99:
                zipFile.close()
                cycle = cycle + 1
                path_archive = path + "/%d" % cycle + ".zip"
                zipFile = zipfile.ZipFile(path_archive.encode('utf-8'), 'w')
            file_path = os.path.join(root,filename)
            zipFile.write(file_path,filename)
            count = (count + 1) % 100
        zipFile.close()

    #读取文件的后缀名，假设zip中每个文件格式相同，即读取一个文件即可
    str = total_file.namelist()[1]
    datatype = re.search('\..*$',str).group()


    return (cycle+1,datatype)

def get_datatype(datatype_suffix):
    text = {'.txt','.rtf','.doc','.doc'}
    audio = {'.cda','.WAV','.mp3','.WMA','.RA','.mid','.OGG'}
    image = {'.bmp','.jpg','.tif','.gif','.jpeg','.svg','.pcx','.tga','.psd','.png'}
    video = {'.rm','.rmvb','.wmv','.avi','.mp4','.3gp','.mkv','.flv','.mpeg'}
    if datatype_suffix in text:
        return u'文本数据'
    if datatype_suffix in audio:
        return u'语音数据'
    if datatype_suffix in image:
        return u'图片数据'
    if datatype_suffix in video:
        return u'视频数据'
    return u'未知类型'


