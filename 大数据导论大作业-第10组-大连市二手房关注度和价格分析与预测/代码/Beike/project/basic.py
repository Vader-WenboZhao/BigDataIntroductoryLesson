import csv

import configparser
import scrapy
import random
import requests
import os
import time
from lxml import etree
from project.houseInfo import HouseInfo
from project.beikeershoufangPage import ErshoufangPage

config=configparser.ConfigParser()
if(os.path.exists(os.path.abspath(os.curdir)+'/config.ini')):
    config.read(os.path.abspath(os.curdir) + '/config.ini', encoding='utf-8')
    path = config['DEFAULT']['path']
    startPage = config['DEFAULT']['startPage']
    startItems = config['DEFAULT']['startItems']
    number = config['DEFAULT']['number']
    icount = config['DEFAULT']['icount']
else:
    print("配置文件不存在！")
    exit(0)
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
ip_list=[
    "121.40.108.76:80",
    "182.35.85.188:9999",
    "60.13.42.252:9999",
    "222.190.222.69:9999",
    "117.25.155.86:12345",
    "49.51.70.42:1080",
    "183.164.238.241:9999",
    "117.57.91.56:9999",
    "42.228.3.158:8080",
    "222.64.158.143:9000",
    "47.98.241.70:1080",
    "123.163.122.5:9999",
    "123.207.43.128:1080",
    "122.228.19.92:3389",
    "123.171.6.121:8118",
]


class BasicSpider(scrapy.Spider):
    name = "basic"
    def parse(self, response, items):                   #解析HTML，得到想要的数据

        pageTitle = str(response.xpath('//title/text()')[0]).strip()
        titel = str(response.xpath('//h1[@class="main"]/text()')[0]).strip()
        sub = str(response.xpath('//div[@class="sub"]/text()')[0]).strip()
        favCount = str(response.xpath('//span[@id="favCount"]/text()')[0]).strip()
        totalPrice = str(response.xpath('//span[@class="total"]/text()')[0]).strip()
        totalPriceUnit = str(response.xpath('//span[@class="unit"]/span/text()')[0]).strip()
        unitPrice = str(response.xpath('//span[@class="unitPriceValue"]/text()')[0]).strip()
        unitPriceUnit = str(response.xpath('//div[@class="unitPrice"]/i/text()')[0]).strip()
        mainInfo = response.xpath('//div[@class="houseInfo"]//div[@class="mainInfo"]/text()')  # 三个互相对应
        subInfo = response.xpath('//div[@class="houseInfo"]//div[@class="subInfo"]/text()')
        aroundLabel = response.xpath('//div[@class="aroundInfo"]//span[@class="label"]/text()')
        communityName = str(response.xpath('//a[@class="info no_resblock_a"]/text()')[0]).strip()
        communityArea = response.xpath('//div[@class ="areaName"]//a/text()')
        visitTimeInfo = str(
            response.xpath('//div[@class="aroundInfo"]//div[@class="visitTime"]//span[@class="info"]/text()')[
                0]).strip()
        idInfo = str(
            response.xpath('//div[@class="aroundInfo"]//div[@class="houseRecord"]//span[@class="info"]/text()')[
                0]).strip()
        # 前两个是地区
        subInfoDict = {}
        subInfoDict[aroundLabel[0]] = communityName
        subInfoDict[aroundLabel[1]] = str(communityArea[0]).strip() + " " + str(communityArea[1]).strip()
        subInfoDict[aroundLabel[2]] = visitTimeInfo
        subInfoDict[aroundLabel[3]] = idInfo
        baseLabel = response.xpath('//div[@class="base"]//span[@class="label"]/text()')  # 相互对应
        baseInfo = response.xpath('//div[@class="base"]//li/text()')
        baseInfoDict = {}
        for base in baseLabel:
            baseInfoDict[str(base).strip()] = str(baseInfo[baseLabel.index(base)]).strip()
        flag = 0
        transactionLabel = response.xpath('//div[@class="transaction"]//span[@class="label"]/text()')  # 相互对应,无抵押信息
        transactionInfo = response.xpath('//div[@class="transaction"]//li/text()')
        pledge = str(response.xpath(
            '//div[@class="transaction"]//span[@style = "display:inline-block;width:64%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;vertical-align:middle;"]/text()')[
                         0]).strip()
        for transaction in transactionLabel:
            if (str(transaction).strip() == "抵押信息"):
                flag = -1
                baseInfoDict[str(transaction).strip()] = pledge
                continue
            baseInfoDict[str(transaction).strip()] = str(
                transactionInfo[transactionLabel.index(transaction) + flag]).strip()
        featureLabel = response.xpath('//div[@class="introContent showbasemore"]//div[@class="name"]/text()')
        feature = response.xpath('//div[@class="introContent showbasemore"]//div[@class="content"]/a/text()')  # 特色
        featureContent = response.xpath('//div[@class="introContent showbasemore"]//div[@class="content"]/text()')
        featureDict = {}
        i = 0
        for f in featureLabel:
            if (str(f).strip() == "房源特色"):
                featureItems = ""
                for s in feature:
                    if (len(str(s).strip()) > 0):
                        featureItems = featureItems + str(s).strip() + " "
                featureDict[str(f).strip()] = featureItems.strip()
                i = i + 1
                continue
            while (len(str(featureContent[i]).strip()) < 1):
                i = i + 1
            featureDict[str(f).strip()] = str(featureContent[i]).strip()
            i = i + 1
        layout = response.xpath('//div[@id = "infoList"]//div[@class="col"]/text()')  # 四个为一组
        layoutDict = {}
        i = 0
        while (i < len(layout) / 4):
            layoutDict[str(layout[i * 4]).strip()] = str(layout[i * 4 + 1]).strip() + " " + str(
                layout[i * 4 + 2]).strip() + " " + str(layout[i * 4 + 3]).strip()
            i = i + 1
        houseInfo = HouseInfo()
        houseInfo.setFavCount(favCount)
        houseInfo.setPrice(totalPrice, totalPriceUnit, unitPrice, unitPriceUnit)
        houseInfo.setSimpleInfo(mainInfo[0], subInfo[0], mainInfo[1], subInfo[1], mainInfo[2], subInfo[2])
        houseInfo.setSubInfo(subInfoDict)
        houseInfo.setBaseInfo(baseInfoDict)
        houseInfo.setHouseFeature(featureDict)
        houseInfo.setHouseLayout(layoutDict)
        ershoufangPage = ErshoufangPage(pageTitle, titel, sub, houseInfo)
        out = open(path, 'a+', newline='')
        data = [ershoufangPage.pageTitle, ershoufangPage.title, ershoufangPage.sub, ershoufangPage.houseInfo.favCount,
                str(ershoufangPage.houseInfo.totalPrice).strip() + str(ershoufangPage.houseInfo.totalUnit).strip(),
                str(ershoufangPage.houseInfo.unitPrice).strip() + str(ershoufangPage.houseInfo.unitPriceUnit),
                ershoufangPage.houseInfo.roomMainInfo, ershoufangPage.houseInfo.roomSubInfo,
                ershoufangPage.houseInfo.typeMainInfo, ershoufangPage.houseInfo.typeSubInfo,
                ershoufangPage.houseInfo.areaMainInfo, ershoufangPage.houseInfo.areaSubInfo,
                ershoufangPage.houseInfo.strSubInfo(), ershoufangPage.houseInfo.strBaseInfo(),
                ershoufangPage.houseInfo.strHouseFeature(), ershoufangPage.houseInfo.strHouseLayout(), items]
        # 数据结构：[网页标题，房源标题，标题补充，关注房源人数，总价，平米价，几室几厅，楼层，朝向，精简装，平米大小，建造时间，房屋补充信息，房屋基本信息，房屋特色，各个房间信息，在原网站的位置]
        # 房屋补充信息，基本信息，特色，房间信息，为多项拼接，每一项用$分割；每一项为对应关系，用:分割（英文":"）

        csv_write = csv.writer(out, dialect='excel')
        csv_write.writerow(data)

    def startspid(self, startPage, startItems, number, icount):     #爬虫主体
        count = icount
        ipage = startPage
        items = startItems - 1
        while (ipage < number + startPage):
            proxies = {
                'http': 'http://' + ip_list[random.randint(0, len(ip_list)) - 1]
            }
            headers = {
                'User-Agent': user_agent_list[random.randint(0, len(user_agent_list) - 1)],
                'Referer': "https://dl.ke.com/?utm_source=baidu&utm_medium=pinzhuan&utm_term=biaoti&utm_content=biaotimiaoshu&utm_campaign=wydalian"
            }
            url = "https://dl.ke.com/ershoufang/pg" + str(ipage) + "rs%E5%A4%A7%E8%BF%9E/"
            print(url)
            r = requests.get(url, headers=headers)
            html = etree.HTML(r.text)
            print(r.text)
            houseHtml = html.xpath('//div[@class="info clear"]//div[@class="title"]//a/@href')
            print(houseHtml)
            while (items < len(houseHtml)):
                s = "第" + str(ipage) + "页第" + str(items + 1) + "个房源"
                self.parse(etree.HTML(requests.get(houseHtml[items], headers=headers).text), s)
                count = count + 1
                items = items + 1
                print("正在爬取" + s + "\n共爬取了" + str(count) + "个房源")
                time.sleep(1)
            ipage = ipage + 1
            items = 0
            # time.sleep(2)


if __name__ == '__main__':
    b = BasicSpider()
    b.startspid(int(startPage), int(startItems), int(number), int(icount))
