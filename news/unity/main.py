from multiprocessing import Process, Manager
import os,webbrowser,requests,json,time,re
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from flask import Flask, redirect, render_template
from pystray import MenuItem as item
import pystray
from PIL import Image


class Croler:
    runingObjects = []
    def __init__(self,key,url):
        self.newsDic = OrderedDict()
        self.key = key
        self.url = url

    
    def main(self):
        try:
            header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
            while True:
                    try:
                        res = requests.get(self.url, headers=header)
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
                try:
                    if not self.newsDic[newsA[i]]:
                        continue
                    if not inner :
                        continue
                    else:
                        self.newsDic[newsA[i].get_text().replace("\t","").replace("\n","").replace("\""," ").replace("\'"," ")] = inner.get_text().replace("\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback()","").replace("\n","").replace("\""," ").replace("\'"," ")+"|"+newsA[i]["href"]

                except:
                    self.newsDic[newsA[i].get_text().replace("\t","").replace("\n","").replace("\""," ").replace("\'"," ")] = inner.get_text().replace("\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback()","").replace("\n","").replace("\""," ").replace("\'"," ")+"|"+newsA[i]["href"]
        except Exception as e:
            print(self.key," : ",e)
            self.main()

    def totxt(self):
        for i in self.newsDic.copy().keys():
            if i == "": continue
            try:
                inner = OrderedDict()
                inner[self.key] = i+" | "+self.newsDic[i].replace("\t","").replace("{}","")
                i_ = re.sub('[\/:*?"<>|“”~]',' ',i)
                if not os.path.exists(f"./data/{self.key}"):
                    os.mkdir(""f"./data/{self.key}")
                with open(f'./data/{self.key}/{i_}.json','x', encoding="utf-8") as f:
                    json.dump(inner,f,ensure_ascii=False)
            except:
                self.newsDic.move_to_end(i)
                self.newsDic.pop(i)


    def loop(self,p):
        p[self.key] = self
        print(p)
        while True:
            for i in range(5):
                self.main()
                time.sleep(180)
            self.totxt()

    def stop(self):
        exit()

app = Flask(__name__)

@app.route("/")
def main_():
    print(obs)
    return render_template("main.html",test="test",list_ = obs)

@app.route("/<name>")
def lobby(name):
    try:
        return render_template("lobby.html",filelist = os.listdir(f"./data/{name}"))
    except:
        return redirect("/")

@app.route("/kill/<name>")
def killer(name):
    try:
        obs[name].stop()
        obs.pop(name)
        return redirect("/")
    except Exception as e:
        print("fail", e)
        return redirect("/")

def flaskmain(q):
    global obs
    obs = q
    app.run(host="127.0.0.1", port="2022")
        

def showfile():
    webbrowser.open_new_tab("http://127.0.1:2022")

def stop():
    icon_.stop()
    exit(0)

def main():
    image = Image.open("./data/img/trayimg.jpg")
    menu = (item("showFiles",showfile),item("exit",stop))
    global icon_
    icon_ = pystray.Icon('name',image,"허브 수집기",menu)
    with open("./data/setting/crol_setting.json","r") as f:
        global targetList
        targetList = json.load(f)["targetList"]
        for i in targetList.keys():
            ob = Croler(i,targetList[i])
            p = Process(target=ob.loop, args=(runingObjects,), daemon=True)
            p.start()
    Fp = Process(target=flaskmain,args=(runingObjects,) , daemon=True)
    Fp.start()
    icon_.run()


if __name__ == "__main__":
    man = Manager()
    runingObjects = man.dict()
    main()