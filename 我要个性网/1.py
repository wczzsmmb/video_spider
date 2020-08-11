from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
 
html = urlopen(input("请输入链接：")) #获取网页
bs = BeautifulSoup(html, 'html.parser') #解析网页
hyperlink = bs.find_all('a')  #获取所有超链接
for h in hyperlink:
    hh = h.get('href')
    #print(hh)
ddd = bs.find_all('img')
print(ddd)
with open("1"+".txt",mode="a+",encoding="utf-8")as f:
              f.write(str(ddd))
              f.write("\n")
print("完成")