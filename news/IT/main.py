import requests
from bs4 import BeautifulSoup as bs
import json
from collections import OrderedDict
import time
import re

newsDic = OrderedDict()

def main():
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    while True:
            try:
                res = requests.get("https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230", headers=header)
                break
            except:
                continue
    b = res.text
    soup = bs(b,"html.parser")
    newsList = soup.select_one("#main_content > div.list_body.newsflash_body > ul.type06_headline")
    newsA = newsList.select("a")
    for i in range(len(newsA)) :
        while True:
            try:
                res_ = requests.get(newsA[i]["href"],headers=header)
                break
            except:
                continue
        newses = res_.text
        soup_ = bs(newses,"html.parser")
        inner = soup_.select_one('#articleBodyContents')
        # print(inner.get_text())
        try:
            if newsDic(newsA[i]):
                continue
            else:
                newsDic[newsA[i].get_text().replace("\t","").replace("\n","").replace("\""," ").replace("\'"," ")] = inner.get_text().replace("\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback()","").replace("\n","").replace("\""," ").replace("\'"," ")+"|"+newsA[i]["href"]

        except:
            newsDic[newsA[i].get_text().replace("\t","").replace("\n","").replace("\""," ").replace("\'"," ")] = inner.get_text().replace("\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback()","").replace("\n","").replace("\""," ").replace("\'"," ")+"|"+newsA[i]["href"]
    # print(newsDic.keys())
    # print(len(newsDic))
            
# print("""
# ########################################
# """)
# print(newsDic)
# print("""
# ########################################
# """)

def tojson():
    try:
        with open("./news.json","a", encoding="utf-8") as F :
            # newsDic = json.dumps(newsDic, ensure_ascii=False)
            print(newsDic)
            json.dump(newsDic,F,ensure_ascii=False, indent="\t")
    except:
        print("r")

def totxt():
    for i in newsDic.copy().keys():
        if i == "": continue
        try:
            inner = OrderedDict()
            inner["it"] = i+" | "+newsDic[i].replace("\t","").replace("{}","")
            i_ = re.sub('[\/:*?"<>|“”~]',' ',i)
            with open(f'./data/{i_}.json','x', encoding="utf-8") as f:
                json.dump(inner,f,ensure_ascii=False)
        except Exception as e:
            newsDic.move_to_end(i)
            newsDic.pop(i)
            # print(e)
            # print("file is alread exist")


while True:
    for i in range(5):
        main()
        # print("----")
        # print(newsDic)
        # print('----',i)
        time.sleep(180)
    # print("####")
    totxt()
    
