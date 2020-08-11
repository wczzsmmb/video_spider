#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: lenovo by XYF
@file: crawler.py
@time: 2020/03/10
@function: 
"""
import requests
import json
import time
import os
import re

INFO = {
    "name": "kuaishou-crawler",
    "author": "oGsLP",
    "repository": "www.github.com/oGsLP/kuaishou-crawler",
    "version": "0.5.0",
    "publishDate": "20-08-06"
}

PROFILE_URL = "https://live.kuaishou.com/profile/"
DATA_URL = "https://live.kuaishou.com/m_graphql"
WORK_URL = "https://m.gifshow.com/fw/photo/"


class Crawler:
    __param_did = ""

    __headers_web = {
        'accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'live.kuaishou.com',
        'Origin': 'https://live.kuaishou.com',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # User-Agent/Cookie 根据自己的电脑修改
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Cookie': ''
    }
    __headers_mobile = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36'
    }

    __crawl_list = []

    __date_cache = ""
    __date_pic_count = 0

    def __init__(self, prod=True):
        self.__intro()
        if prod:
            time.sleep(5)
        else:
            self.__read_preset()

    def set_did(self, did):
        self.__param_did = did
        self.__headers_web['Cookie'] = 'did=' + did + "; userId="
        self.__headers_mobile['Cookie'] = 'did=' + did

    def crawl(self):
        print("准备开始爬取，共有%d个用户..." % len(self.__crawl_list))
        print()
        time.sleep(2)
        for uid in self.__crawl_list:
            self.__date_cache = ""
            self.__date_count = 0
            self.__crawl_user(uid)

    def add_to_list(self, uid):
        self.__crawl_list.append(uid)

    def __crawl_user(self, uid):
        if uid.isdigit():
            uid = self.__switch_id(uid)

        payload = {"operationName": "privateFeedsQuery",
                   "variables": {"principalId": uid, "pcursor": "", "count": 999},
                   "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}
        res = requests.post(DATA_URL, headers=self.__headers_web, json=payload)

        works = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']

        if not os.path.exists("../data"):
            os.makedirs("../data")

        # 这两行代码将response写入json供分析
        # with open("data/" + uid + ".json", "w") as fp:
        #     fp.write(json.dumps(works, indent=2))

        # 防止该用户在直播，第一个作品默认为直播，导致获取信息为NoneType
        if works[0]['id'] is None:
            works.pop(0)
        name = re.sub(r'[\\/:*?"<>|\r\n]+', "", works[0]['user']['name'])

        dir = "data/" + name + "(" + uid + ")/"
        # print(len(works))
        if not os.path.exists(dir):
            os.makedirs(dir)

        # if not os.path.exists(dir + ".list"):
        #     print("")

        #print("开始爬取用户 " + name + "，保存在目录 " + dir)
        #print(" 共有" + str(len(works)) + "个作品")

        #for j in range(len(works)):
            #self.__crawl_work(dir, works[j], j + 1)
            #time.sleep(1)

        #print("用户 " + name + "爬取完成!")
        #print()
        time.sleep(1)
        print(works)
        def __crawl_work(self, dir, work, wdx, like=False):
            w_type = work['workType']
            w_caption = re.sub(r"\s+", " ", work['caption'])
            w_name = re.sub(r'[\\/:*?"<>|\r\n]+', "", w_caption)[0:24]
            w_time = time.strftime('%Y-%m-%d', time.localtime(work['timestamp'] / 1000))
            w_index = ""
            if not like:
                if self.__date_cache == w_time:
                    self.__date_count = self.__date_count + 1
                    if self.__date_count > 0:
                        w_index = "(%d)" % self.__date_count
                else:
                    self.__date_cache = w_time
                    self.__date_count = 0
                if w_type == 'vertical' or w_type == 'multiple' or w_type == "single" or w_type == 'ksong':
                    w_urls = work['imgUrls']
                    l = len(w_urls)
                    print("  " + str(wdx) + ")图集作品：" + w_caption + "，" + "共有" + str(l) + "张图片")
                    for i in range(l):
                        p_name = w_time + w_index + "_" + w_name + "_" + str(i + 1) + '.jpg'
                        pic = dir + p_name
                        if not os.path.exists(pic):
                            r = requests.get(w_urls[i].replace("webp", "jpg"))
                            r.raise_for_status()
        with open("1"+".txt",mode="a+",encoding="utf-8")as f:
              f.write(str(works))

    '''
    快手分为五种类型的作品，在作品里面表现为workType属性
     * 其中两种图集: `vertical`和`multiple`，意味着拼接长图和多图，所有图片的链接在imgUrls里
     * 一种单张图片: `single` 图片链接也在imgUrls里
     * K歌: `ksong` 图片链接一样，不考虑爬取音频...
     * 视频: `video` 需要解析html获得视频链接
    '''

    def __crawl_work(self, dir, work, wdx, like=False):
        w_type = work['workType']
        w_caption = re.sub(r"\s+", " ", work['caption'])
        w_name = re.sub(r'[\\/:*?"<>|\r\n]+', "", w_caption)[0:24]
        w_time = time.strftime('%Y-%m-%d', time.localtime(work['timestamp'] / 1000))
        w_index = ""
        if not like:
            if self.__date_cache == w_time:
                self.__date_count = self.__date_count + 1
                if self.__date_count > 0:
                    w_index = "(%d)" % self.__date_count
            else:
                self.__date_cache = w_time
                self.__date_count = 0
        
        if w_type == 'vertical' or w_type == 'multiple' or w_type == "single" or w_type == 'ksong':
            w_urls = work['imgUrls']
            l = len(w_urls)
            print("  " + str(wdx) + ")图集作品：" + w_caption + "，" + "共有" + str(l) + "张图片")
            for i in range(l):
                p_name = w_time + w_index + "_" + w_name + "_" + str(i + 1) + '.jpg'
                pic = dir + p_name
                if not os.path.exists(pic):
                    r = requests.get(w_urls[i].replace("webp", "jpg"))
                    r.raise_for_status()
                    with open("1"+".txt",mode="a+",encoding="utf-8")as f:
                        f.write(works)
                    print("    " + str(i + 1) + "/" + str(l) + " 图片 " + p_name + " 下载成功 √")
                else:
                    print("    " + str(i + 1) + "/" + str(l) + " 图片 " + p_name + " 已存在 √")

        
        elif w_type == 'video':
            w_url = WORK_URL + work['id']
            res = requests.get(w_url, headers=self.__headers_mobile,
                               params={"did": self.__param_did})
            html = res.text
            # with open("data/" + work['id'] + ".html", "w") as fp:
            #     fp.write(html)
            pattern = '"srcNoMark":"(https:.*?).mp4'

            v_url = re.search(pattern, html).group(1)+".mp4"

            # print(v_url)
            # pattern = re.compile(r"playUrl", re.MULTILINE | re.DOTALL)
            # script = soup.find("script", text=pattern)
            # s = pattern.search(script.text).string
            # v_url = s.split('playUrl":"')[1].split('.mp4')[0].encode('utf-8').decode('unicode-escape') + '.mp4'
            try:
                print("  " + str(wdx) + ")视频作品：" + w_caption)
            except:
                print("  这里似乎有点小错误，已跳过")
            v_name = w_time + w_index + "_" + w_name + ".mp4"
            video = dir + v_name

            if v_url:
                if not os.path.exists(video):
                    r = requests.get(v_url)
                    r.raise_for_status()

                    with open(video, "wb") as f:
                        f.write(r.content)
                    print("    视频 " + v_name + " 下载成功 √")
                else:
                    print("    视频 " + v_name + " 已存在 √")
            else:
                print("未找到视频")
        else:
            print("错误的类型")

    def crawl_like(self, uid):
        payload = {"operationName": "likedFeedsQuery",
                   "variables": {"principalId": uid, "pcursor": "", "count": 9999},
                   "query": "query likedFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  likedFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}
        cookie_like = "live_deviceid=web_2761de01059f8b0a60555ae7ff5d69e4; client_key=65890b29; clientid=3; did=web_2761de01059f8b0a60555ae7ff5d69e4; didv=1583906306185; userId=734830893; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1585027806; kuaishou.live.bfb1s=ac5f27b3b62895859c4c1622f49856a4; userId=734830893; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAVDawiXZPtyTC5VMgLpjQ3-Qbeq711iW5YSERJLxNu8GdpK4_sVV7noXOpmENiqNqOR33JD4y3KVH1I-DrCL2YAlluhKNcYx5aoAfZ1UPBDGvaOc26zb0y4Vlnozd394yASJJr8dx-18Rmh9lL2DeHS9ki5itZuKKWdXXvB3gfVmzKs4bv_9EH_GBVYMpXyX5H9fgdM6Rtw4wyzbPVrS_48aEurKvNghXkU0vIm_W_UXPUfuwSIgNlpIpBIpRlbM9q8mF6SBu_1NHP6ppeFPEtUrmAs0TMUoBTAB; kuaishou.live.web_ph=10695f787577fd9ccd02071217a8b1a73ad0"
        self.__headers_web["Cookie"] = cookie_like
        res = requests.post(DATA_URL, headers=self.__headers_web, json=payload)
        dta = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['likedFeeds']
        works = dta['list']
        print("开始爬取用户 " + uid + " 的喜欢作品")
        print(" 共有" + str(len(works)) + "个作品")
        for i in range(len(works)):
            self.__crawl_work("data/Liked/", works[i], i + 1, True)

    def __read_preset(self):
        p_path = "preset"
        if not os.path.exists(p_path):
            print("创建预设文件 preset ...")
            open(p_path, "w")
        if not os.path.getsize(p_path):
            print("请在预设文件 preset 中记录需要爬取的用户id，一行一个")
            exit(0)
        with open(p_path, "r") as f:
            for line in f:
                if line[0] != "#":
                    self.__crawl_list.append(line.strip())

    def __switch_id(self, uid):
        payload = {"operationName": "SearchOverviewQuery",
                   "variables": {"keyword": uid, "ussid": None},
                   "query": "query SearchOverviewQuery($keyword: String, $ussid: String) {\n  pcSearchOverview(keyword: $keyword, ussid: $ussid) {\n    list {\n      ... on SearchCategoryList {\n        type\n        list {\n          categoryId\n          categoryAbbr\n          title\n          src\n          __typename\n        }\n        __typename\n      }\n      ... on SearchUserList {\n        type\n        ussid\n        list {\n          id\n          name\n          living\n          avatar\n          sex\n          description\n          counts {\n            fan\n            follow\n            photo\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on SearchLivestreamList {\n        type\n        lssid\n        list {\n          user {\n            id\n            avatar\n            name\n            __typename\n          }\n          poster\n          coverUrl\n          caption\n          id\n          playUrls {\n            quality\n            url\n            __typename\n          }\n          quality\n          gameInfo {\n            category\n            name\n            pubgSurvival\n            type\n            kingHero\n            __typename\n          }\n          hasRedPack\n          liveGuess\n          expTag\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

        res = requests.post(DATA_URL, headers=self.__headers_web, json=payload)
        dt = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']
        # with open("data/jj_" + uid + ".json", "w") as fp:
        #     fp.write(json.dumps(dt, indent=2))

        return dt['pcSearchOverview']['list'][1]['list'][0]['id']

    def __intro(self):
        print()
        print("|  %s (v%s %s)" % (INFO["name"], INFO["version"], INFO["publishDate"]))
        print("|  本程序由%s提供, %s, 喜欢的话可以给个star >_<" % (INFO["author"], INFO["repository"]))
        print()
