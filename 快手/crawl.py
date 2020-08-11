#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: lenovo by XYF
@file: crawl.py
@time: 2020/02/20
@function: 
"""

import os
from lib.crawler import Crawler

param_did = "web_4d278843dfe8426034453bf2c2212f1f"


def crawl():
    crawler = Crawler(False)
    crawler.set_did(param_did)
    crawler.crawl()


if __name__ == "__main__":
    crawl()
