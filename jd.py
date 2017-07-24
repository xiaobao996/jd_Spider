# -*- coding: gbk -*-
import uuid
import socket
import os
import time
import requests
import pymysql
import re
import random
import json
from lxml import etree

USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    ]

def header_connet():
    useragent = random.choice(USER_AGENTS)
    header = {
        'Host': 'cd.jd.com',
        'Connection': 'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'Accept': '*/*',
        # 'Referer': 'http://item.jd.com/11141027907.html',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'user-key=2bfbe09b-0f42-42c0-811b-ab56450db8e8; ipLoc-djd=1-2800-2849-0.138300342; ipLocation=%u5317%u4EAC; areaId=1; unpl=V2_ZzNtbUJSERJ9AERQf0teV2IKGglKU0AcdVgSA3wZCwYzB0UJclRCFXMUR1NnGVgUZAIZXEFcQxVFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2V3oZXwdhAhJdQWdzEkU4dld4G1UBYDMTbUNnAUEpC0NTeBtbSGQCEl5AUUIVdQt2VUsa; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_14c699355c3c489e95281aef61f2e5fe|1497528124631; mt_xid=V2_52007VwATUl5aVFsfSRpsUDcHElRcC1pGTE0cVBliVhQGQVAGCkxVGg8HNAdHAV9YAVkbeRpdBWEfE1VBWFZLHEgSXQZsABJiX2hSah9JEV8AZgIaU21YV1wY; pin=guanfangzhanghao; _tp=Q65pAl67vai0QY5ZcDYFjN%2BLg8cBR7nqqHw9I0DlABg%3D; _pst=guanfangzhanghao; TrackID=1Z3HN0vwCksbe3xembF38t1V0iShJpm8CIhbCVsYYdNehxHMhHeXfnJAfKqYOYsmqCHUCx-iLItRozWL5og6WGbd5LmoQem0U9GDvI4gBeWA|||xupYxaphrv2-V2BUUpiB6LV9-x-f3wj7; unick=guanfangzhanghao; pinId=xupYxaphrv2-V2BUUpiB6LV9-x-f3wj7; cn=0; 3AB9D23F7A4B3C9B=IK4KNJCB5IKI3TZOLTHYUNLR7CSSZQQXQJHK7LXWVXVR3CA4QICX4GJMCK3ODS4LQYXFCO5ATFOEEGN2Q3KMKQTXQM; __jda=122270672.2012370112.1494920356.1497518633.1497578162.34; __jdb=122270672.7.2012370112|34.1497578162; __jdc=122270672; __jdu=2012370112; thor=8D545014BC7B0DA50777F43FFED760334CF7139A43DD89736F837F4A6E1412E5989DD4744AB7CB431B29D41DF581DF2249A269AF2E5B7942C190BAAFB95F2275B24F25EA35CD43753EBA4B1DCD2AB99D50ACCC6BBBF95EF8F650088DC9CE362ACFED4924B528F54E480C0E1205B4254341DD46CE770D857CE3A041AAB768F3FBF5CA836215BDAB0C3A194C6D7D5E867F06824C2F0D3F5D4A527D7857D39CA38B'
        # 'If-Modified-Since': 'Fri, 16 Jun 2017 02:07:20 GMT'
    }
    return header

def header_price():
    useragent = random.choice(USER_AGENTS)
    header_price = {
        'Host':'p.3.cn',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':useragent,
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4'
    }
    return header_price

def head():
    useragent = random.choice(USER_AGENTS)
    head2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    return head2

def getMysqlUrl():
    skurl_list = []
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'weibo_info_eb', charset='utf8')
    # 创建游标
    cursor = db.cursor()
    # sql查询zjd表中数据
    sql = "select * from zjd"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()

        for row in results:
            skurl_dict = {}
            skurl_dict[row[1]] = row[3]
            skurl_list.append(skurl_dict)
    except:
        print("Error: unable to fetch data")

        # 关闭数据库连接
    db.close()
    return skurl_list

#n用来记录for循环次数

def SaveDateMySql(page_url,original_url,floor,source_host,column,column1,post_title,promotionInfos,text,proCurPrice,detailParam,Offtheshelf,proClassify):
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'weibo_info_eb', charset='utf8')
    # 创建游标
    cursor = db.cursor()
    # sql查询zjd表中数据
    sql = 'INSERT INTO jd_price(page_url,original_url,floors,source_host,columns,column1,post_title,promotionInfos,text,proCurPrice,detailParam,Offtheshelf,proClassify) VALUES ("%s","%s","%d","%s","%s","%s","%s","%s","%s","%f","%s","%d","%s" )' % (page_url,original_url,floor,source_host,column,column1,post_title,promotionInfos,text,proCurPrice,detailParam,Offtheshelf,proClassify)
    try:
        cursor.execute(sql)
        print('插入数据成功')
    except Exception as e:
        print('插入数据异常',e)
    db.close()

def request_price(priceAPI):
    try:
        resq_price = requests.get(priceAPI, headers=header_price(), verify=False).text
        return resq_price
    except Exception as e:
        print(e)
        return False

def inde(ulist,history_list):
    skurl_list = ulist
    for n, dic in enumerate(skurl_list):
        skurl = list(dic.keys())[0]
        column = list(dic.values())[0]
        floor = 0
        skuid = re.compile(r'\d+').findall(skurl)[0]
        # proxies = {"http": "http://111.13.109.27:80"}
        # html = requests.get(skurl,headers=head(),proxies=proxies).text
        try:
            html = requests.get(skurl, headers=head(), timeout=20, verify=False).text
        except Exception as e:
            print(e)
            history = {}
            history[skurl] = column
            history_list.append(history)
            print('第', n, '条任务')
            continue
        tree = etree.HTML(html)
        Offtheshelf = tree.xpath('//div[@class="itemover-tip"]/text()')
        if Offtheshelf:
            Offtheshelf = 0
        else:
            Offtheshelf = 1
        try:
            post_title = tree.xpath('//div[@class="sku-name"]/text()')
            if len(post_title) > 1:
                post_title = tree.xpath('//div[@class="sku-name"]/text()')[1].replace('\n', '').strip()
            else:
                post_title = tree.xpath('//div[@class="sku-name"]/text()')[0].replace('\n', '').strip()
        except Exception as e:
            print('post_title:', e)
            print('第', n, '条任务')
            continue

        try:
            text = tree.xpath('//ul[@class="parameter2 p-parameter-list"]')[0].xpath('string(.)').strip().replace('\n',
                                                                                                                  '').replace(
                ' ', '')
        except Exception as e:
            print(e)
            history1 = {}
            history1[skurl] = column
            history_list.append(history1)
            print('第', n, '条任务')
            continue

        cat = tree.xpath('//ul[@id="parameter-brand"]/li/a/@href')[0]
        cat = cat[str(cat).index('?') + 1:str(cat).index('&')]
        proClassify = tree.xpath('//div[@class="crumb fl clearfix"]')[0].xpath('string(.)').strip().replace(' ',
                                                                                                            '').replace(
            '\n', '')

        shopid = tree.xpath('//a[@class="btn-def follow-shop J-follow-shop"]/@data-vid')[0]
        venderid_num = html.index('venderId:')
        venderid = re.compile(r'\d+').findall(html[venderid_num:html.index('shopId:')])[0]
        times = int(time.time())
        promotionAPI = 'http://cd.jd.com/promotion/v2?callback=jQuery3850309&skuId=' + skuid + '&area=1_2800_2849_0&shopId=' + shopid + '&venderId=' + venderid + '&' + cat
        priceAPI = 'https://p.3.cn/prices/mgets?callback=jQuery1801546&type=1&area=1&pdtk=&pduid='+str(times)+'&pdpin=&pdbp=0&skuIds=J_' + skuid + '&ext=10000000&source=item-pc'


        try:
            resq_text = requests.get(promotionAPI, headers=header_connet())
        except Exception as e:
            print(e)
            history2 = {}
            history2[skurl] = column
            history_list.append(history2)
            print('第', n, '条任务')
            continue
        try:
            data_json = json.loads(resq_text.text.replace('jQuery3850309', '').replace('(', '').replace(')', ''))
        except Exception as e:
            print(e)
            print('请求价格异常:', e)
            history5 = {}
            history5[skurl] = column
            history_list.append(history3)
            print('第', n, '条任务')
            continue

        skuCoupon = data_json['skuCoupon']

        # print(skuCoupon)

        if skuCoupon:
            for sku in skuCoupon:
                quota = ['满' + str(sku['quota']) + '减' + str(sku['discount']) for sku in skuCoupon]
        else:
            quota = []
        # print(quota)   #满减
        try:
            tags = data_json['prom']['tags']
        except Exception as e:
            print(e)
            history6 = {}
            history6[skurl] = column
            history_list.append(history6)
            print('第', n, '条任务')
            continue
        if tags:
            pass
        e = {huangou['name']: huangou['content'] for huangou in tags}
        pickOneTag = data_json['prom']['pickOneTag']
        w = {cuxiao['name']: cuxiao['content'] for cuxiao in pickOneTag}

        promotion = dict(e, **w)  # 把换购和促销整合在一起dict
        # print(promotion)
        # proxies = {"http": "http://42.159.119.154:80"}
        # print(priceAPI)

        resq_price = request_price(priceAPI)
        if not resq_price:
            history4 = {}
            history4[skurl] = column
            history_list.append(history4)
            print('第', n, '条任务')
            continue
        # print(resq_price)

        data_json_price = json.loads(resq_price.replace('jQuery1801546(', '').replace(');', ''))
        # print(priceAPI)
        try:
            price = data_json_price[0]['p']
        except Exception as e:
            print('请求价格异常:', e)
            history3 = {}
            history3[skurl] = column
            history_list.append(history3)
            print('第', n, '条任务')
            continue
        # print(price)
        JdInfo = {}
        JdInfo["original_url"] = skurl
        JdInfo["floor"] = floor
        JdInfo["source_host"] = '电商'
        JdInfo["column1"] = '价格监测_京东'
        JdInfo["column"] = column
        JdInfo['post_title'] = post_title
        JdInfo['promotionInfos'] = quota
        JdInfo['text'] = str(text)
        JdInfo['proCurPrice'] = float(price)
        JdInfo['detailParam'] = promotion
        JdInfo['Offtheshelf'] = Offtheshelf
        JdInfo['proClassify'] = proClassify
        source_host = '电商'
        column1 = '价格监测_京东'

        data = {}
        data["page_url"] = skurl
        data["data"] = []
        data["data"].append(JdInfo)

        scene = {}
        scene["isremote"] = 1
        scene["historystat"] = None

        runTimeParam = {}
        runTimeParam["scene"] = scene
        runTimeParam["run_url"] = skurl
        runTimeParam["original_url"] = skurl

        param = {}
        param["runTimeParam"] = json.dumps(runTimeParam)
        data["param"] = param
        print('第', n, '条任务')
        print(data)
        SaveDateMySql(skurl, skurl, int(floor), source_host, column, column1, post_title, str(quota), str(text),float(price), promotion, int(Offtheshelf), proClassify)
        # print(post_title)
        # print('promotionAPI:'+promotionAPI)
        # print('priceAPI:'+priceAPI)

        # with open("d:\\1.txt","w",encoding='utf-8') as f:
        #     datas = json.dumps(data,ensure_ascii=False)
        #    # datas=datas.encode('utf-8')
        #     f.write(datas)
        
    return history_list

if __name__ == "__main__":
    history_list = []
    skurl_list = getMysqlUrl()
    history_list = inde(skurl_list,history_list)
    print('失败列表history:',history_list,len(history_list))
    while history_list:
        newhistory = []
        history_list = inde(history_list,newhistory)
        print('history_list:',history_list,len(history_list))
