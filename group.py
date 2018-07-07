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
        exit()
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
    items = group.select(".fi-mu-list")
     #中英文对照字典
    team = {'Argentina':'阿根廷','Egypt':'埃及','Australia':'澳大利亚','Panama':'巴拿马','Brazil':'巴西','Belgium':'比利时','Iceland':'冰岛','Poland':'波兰','Denmark':'丹麦','Germany':'德国','Russia':'俄罗斯','France':'法国','Colombia':'哥伦比亚','Costa Rica':'哥斯达黎加','Korea Republic':'韩国','Croatia':'克罗地亚','Peru':'秘鲁','Mexico':'墨西哥','Nigeria':'尼日利亚','Portugal':'葡萄牙','Japan':'日本','Sweden':'瑞典','Switzerland':'瑞士','Serbia':'塞尔维亚','Senegal':'塞内加尔','Saudi Arabia':'沙特阿拉伯','Tunisia':'突尼斯','Uruguay':'乌拉圭','Spain':'西班牙','IR Iran':'伊朗','England':'英格兰','Morocco':'摩洛哥'}
    hosts = {'Moscow':'莫斯科','Ekaterinburg':'叶卡特琳堡','St. Petersburg':'圣彼得堡','Sochi':'索契','Kazan':'喀山','Saransk':'萨兰斯克','Kaliningrad':'加里宁格勒','Samara':'萨马拉','Rostov-On-Don':'顿河罗斯托夫','Nizhny Novgorod':'下诺夫哥罗德','Volgograd':'伏尔加格勒'}

    for item in items :
        matches = item.select(".fi-mu__link")
        for match in matches :
          try:
            time = str.strip(match.select(".fi-mu__info__datetime")[0].text.split("Local time")[0])
            dt = datetime.datetime.strptime(time, "%d %b %Y - %H:%M") + datetime.timedelta(hours=5)
            group = match.select(".fi__info__group")[0].text.split(" ")[1]
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
               #中英文时间
            timeZh = dt.strftime("%Y年%m月%d日 %H:%M")   
            timeEn = dt.strftime("%Y %b %d - %H:%M")            
            statium = match.select(".fi__info__stadium")[0].text
            home = match.select(".home .fi-t__nText")[0].text
            away = match.select(".away .fi-t__nText")[0].text
            score = str.strip(match.select(".fi-s__scoreText")[0].text)
               #打印判断
            if lang == "cn":
                print(timeZh.split(' ')[0] + "\t" + timeZh.split(' ')[1] + '\t' + group + "\t" + team[home].rjust(5,"　") + "\t" + score.center(5) + "\t" + team[away].ljust(10) + "\t" + hosts[city].ljust(7) + "\t" + statium)
            if lang == "en":
                print(timeEn.split(' - ')[0] + "\t" + timeEn.split(' - ')[1] + '\t' + group + "\t" + home.rjust(15) + "\t" + score.center(5) + "\t" + away.ljust(15) + "\t" + city.ljust(10) + "\t" + statium)
          except Exception as ex:
            print(ex)
     
