# -*- coding:utf-8 -*-

import urllib.request, sys,base64,json,os,time,baiduSearch,screenshot,re
from PIL import Image
from common import config
from functools import partial
from common.baiduocr import get_text_from_image as bai_get_text
import requests


index = input("input: 百万英雄-1 冲顶大会-2 芝士超人-3 头脑王者-4\n")
config = config.open_accordant_config()
#region_kind = config['region_million']
if index=='1':
    region_kind_title = config['region_million_title']
    region_kind_answerA = config['region_million_answerA']
    region_kind_answerB = config['region_million_answerB']
    region_kind_answerC = config['region_million_answerC']
    region_kind_answerD = config['region_million_answerD']
elif index=='2':
    region_kind_title = config['region_top_title']
    region_kind_answerA = config['region_top_answerA']
    region_kind_answerB = config['region_top_answerB']
    region_kind_answerC = config['region_top_answerC']
    region_kind_answerD = config['region_top_answerD']
elif index=='3':
    region_kind_title = config['region_super_title']
    region_kind_answerA = config['region_super_answerA']
    region_kind_answerB = config['region_super_answerB']
    region_kind_answerC = config['region_super_answerC']
    region_kind_answerD = config['region_super_answerD']
elif index=='4':
    region_kind_title = config['region_tounao_title']
    region_kind_answerA = config['region_tounao_answerA']
    region_kind_answerB = config['region_tounao_answerB']
    region_kind_answerC = config['region_tounao_answerC']
    region_kind_answerD = config['region_tounao_answerD']
else:
    print('输入格式错误')

get_text_from_image = partial(bai_get_text,
                              app_id=config['app_id'],
                              app_key=config['app_key'],
                              app_secret=config['app_secret'],
                              api_version=config['api_version'][0],
                              timeout=5)

def start_answer():
    input('题目出现后按回车：\n')

    start = time.time()

    screenshot.pull_screenshot()

    im = Image.open(r"./data/screenshot.png")
    #screen_end = time.time()
   # print('截图用时：' + str(screen_end - start) + '秒')
    region_title = (tuple(region_kind_title))
    region_answerA = (tuple(region_kind_answerA))
    region_answerB = (tuple(region_kind_answerB))
    region_answerC = (tuple(region_kind_answerC))
    region_answerD = (tuple(region_kind_answerD))
    
    region_title = im.crop(region_title)
    region_title.save("./data/crop_title.png")
    
    region_answerA = im.crop(region_answerA)
    region_answerA.save("./data/crop_answerA.png")
    region_answerB = im.crop(region_answerB)
    region_answerB.save("./data/crop_answerB.png")
    region_answerC = im.crop(region_answerC)
    region_answerC.save("./data/crop_answerC.png")
    region_answerD = im.crop(region_answerD)
    region_answerD.save("./data/crop_answerD.png")

    f = open('./data/crop_title.png', 'rb')
    img_data_title = f.read()
    f.close()
    
    f = open('./data/crop_answerA.png', 'rb')
    img_data_answerA = f.read()
    f.close()
    f = open('./data/crop_answerB.png', 'rb')
    img_data_answerB = f.read()
    f.close()
    f = open('./data/crop_answerC.png', 'rb')
    img_data_answerC = f.read()
    f.close()
    f = open('./data/crop_answerD.png', 'rb')
    img_data_answerD = f.read()
    f.close()

    #ocr_start =time.time()

    keyword_title = get_text_from_image(
        image_data=img_data_title,
    )
    print('标题：' + keyword_title)
    
    keyword_answerA = get_text_from_image(
        image_data=img_data_answerA,
    )
    keyword_answerB = get_text_from_image(
        image_data=img_data_answerB,
    )
    keyword_answerC = get_text_from_image(
        image_data=img_data_answerC,
    )
    keyword_answerD = get_text_from_image(
        image_data=img_data_answerD,
    )
    print('答案：' + keyword_answerA + ',' + keyword_answerB + ',' +keyword_answerC + ',' +keyword_answerD)
    
    #ocr_end = time.time()
  #  print('OCR用时：' + str(ocr_end - ocr_start) + '秒')

  
    #countsA = search_count(keyword_title,keyword_answerA)
    countsA = words_count(keyword_title,keyword_answerA)
    a1 = int(countsA[0])
    #countsB = search_count(keyword_title,keyword_answerB)
    countsB = words_count(keyword_title,keyword_answerB)
    b1 = int(countsB[0])
    #countsC = search_count(keyword_title,keyword_answerC) 
    countsC = words_count(keyword_title,keyword_answerC)
    c1 = int(countsC[0])
    #countsD = search_count(keyword_title,keyword_answerD)
    countsD = words_count(keyword_title,keyword_answerD)
    d1 = int(countsD[0])
    a = [a1,b1,c1,d1]
    maxx = 0
    for i in range(0,len(a)):
        c = a[i]
        if c >= maxx:
            maxx = c
            maxxcounts = i
            
    b = {0:keyword_answerA,1:keyword_answerB,2:keyword_answerC,3:keyword_answerD}
    d = {0:region_kind_answerA,1:region_kind_answerB,2:region_kind_answerC,3:region_kind_answerD}
   # end = time.time()
   # print('程序用时：' + str(end - start) + '秒')
    print('正确答案为：' + b[maxxcounts])
    cmd = 'adb shell input tap {x1} {y1}'.format(
        x1=(d[maxxcounts][0]+d[maxxcounts][2])/2,
        y1=(d[maxxcounts][1]+d[maxxcounts][3])/2,
    )
    os.system(cmd)
    
    
    #print(keyword_title)

#计算问题＋每个选项搜索的结果数  
def search_count(question,answers):  
   # print ("根据结果数量：" ) 
    counts = [] 
    req = requests.get(url='http://www.baidu.com/s', params={'wd': question +"%20"+answers})
    body = req.text  
    start = body.find(u'百度为您找到相关结果约') + 11  
    body = body[start:]  
    end = body.find(u"个")  
    num = body[:end]  
    num = num.replace(',', '')  
    counts.append(num)  
   # print (answers + " ---> " + str(num) )  
    return counts

#根据问题搜索结果计算每个选项出现的次数  
def words_count(question,answers):  
    print ("根据词频:")  
    req = requests.get(url='http://www.baidu.com/s', params={'wd': question})  
    body = req.text  
    counts = []
    num = body.count(answers)  
    counts.append(num)  
    print (answers + " ---> " + str(num))  
    return counts

#---- 主程序
while(1):
    start_answer()


