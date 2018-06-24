# -*- coding: UTF-8 -*-
from urllib import request
from bs4 import BeautifulSoup 
import string
import datetime
import sys

if __name__ == "__main__":
     #参数判断
    if len(sys.argv) != 2:
        print("清添加参数: en-英文 cn-中文")
    lang = sys.argv[1]
    if lang != "en" and lang != "cn":
        print("Invalid Parameter")
        exit()
     #添加urllib头绕过FIFA反爬虫
    req = request.Request("https://www.fifa.com/worldcup/matches/#knockoutphase",headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}) 
    response = request.urlopen(req)
    html = response.read()
    #print(html)
     #使用lxml解析器可以支持中文
    soup = BeautifulSoup(html, "lxml")
     #主赛况列表css类
    group = soup.select("[data-tab='groupphase']")[0]
    knockout = soup.select("[data-tab='knockoutphase']")[0]
    items = knockout.select(".fi-mu-list")
     #中英文对照字典
    hosts = {'Moscow':'莫斯科','Ekaterinburg':'叶卡特琳堡','St. Petersburg':'圣彼得堡','Sochi':'索契','Kazan':'喀山','Saransk':'萨兰斯克','Kaliningrad':'加里宁格勒','Samara':'萨马拉','Rostov-On-Don':'顿河罗斯托夫','Nizhny Novgorod':'下诺夫哥罗德','Volgograd':'伏尔加格勒'}
    rounds = {'Round of 16':'1/8决赛','Quarter-finals':'1/4决赛','Semi-finals':'半决赛','Play-off for third place':'季军赛','Final':'决  赛'}

    for item in items :
        matches = item.select(".fixture")
        for match in matches :
          try:
            time = str.strip(match.select(".fi-mu__info__datetime")[0].text.split("Local time")[0])
            dt = datetime.datetime.strptime(time, "%d %b %Y - %H:%M") + datetime.timedelta(hours=5)
            stage = str.strip(item.select(".fi-mu-list__head")[0].text)
            city = match.select(".fi__info__venue")[0].text
               #加里宁格勒时区校准
            if city == "Kaliningrad":
                dt = dt + datetime.timedelta(hours=1)
               #萨马拉时区校准
            if city == "Samara":
                dt = dt + datetime.timedelta(hours=-1)
               #叶卡捷琳堡时区校准
            if city == "Ekaterinburg":
                dt = dt + datetime.timedelta(hours=-2)
            timeZh = dt.strftime("%Y年%m月%d日 %H:%M")    
            timeEn = dt.strftime("%Y %b %d - %H:%M")              
            statium = match.select(".fi__info__stadium")[0].text
            home = match.select(".home .fi-t__nText")[0].text
            away = match.select(".away .fi-t__nText")[0].text
            score = str.strip(match.select(".fi-s__scoreText")[0].text)
               #打印判断
            if lang == "cn":
                print(timeZh.split(' ')[0] + "\t" + timeZh.split(' ')[1] + "\t" + rounds[stage].ljust(4) + "\t" + home.rjust(3) + "\t" + score.center(5) + "\t" + away.ljust(3) + "\t" + hosts[city].ljust(7) + "\t" + statium)
            if lang == "en":
                print(timeEn.split(' - ')[0] + "\t" + timeEn.split(' - ')[1] + "\t" + stage.ljust(24) + "\t" + home.rjust(5) + "\t" + score.center(5) + "\t" + away.ljust(10) + "\t" + city.ljust(14) + "\t" + statium)
          except Exception as ex:
            print(ex)
     
