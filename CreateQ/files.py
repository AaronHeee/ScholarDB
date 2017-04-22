# encoding=utf-8

#create by aaron

import zipfile
import re

def divide_file(path):
    num = 0
    flag = 0
    print path
    zip_path = path[0]+"/"+path[1]
    total_file = zipfile.ZipFile(zip_path,'r')
    file_list = total_file.namelist()
    length = len(file_list)
    print length

    if length == 0:
        return {'num': 0}

    #将文件分割成若干份，每份中有100个待标记数据
    while(1):
        archive_path = path[0] + "/%d" % num

        for i in range(0,100):
            if num * 100 + i >= length:
                flag = 1
                break
            else:
                total_file.extract(file_list[num*100+i],archive_path)
        if flag:
            break
        num += 1

    #读取文件的后缀名，假设zip中每个文件格式相同，即读取一个文件即可
    str = total_file.namelist()[1]
    print "-------------"
    print str
    datatype = re.search('\..*$',str).group()

    print datatype

    return (num,datatype)

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


