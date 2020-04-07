# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import time
## __VIEWSTATE
## __VIEWSTATEGENERATOR
## __EVENTVALIDATION
## ctl00$ContentPlaceHolder1$rooms #value=13 #"三六九山莊"
## ctl00$ContentPlaceHolder1$ddlYear
## ctl00$ContentPlaceHolder1$ddlMonth
## ctl00$ContentPlaceHolder1$hidYear
## ctl00$ContentPlaceHolder1$hidMonth 
## ctl00$ContentPlaceHolder1$btnsearch #value="查詢"

##url = "https://www.nownews.com/cat/column"
url = "https://npm.cpami.gov.tw/bed_1.aspx" ## 雪霸國家公園,登山入園床位查詢
headers ={
        #"Host": "npm.cpami.gov.tw",
        #"Origin":"https://npm.cpami.gov.tw",
        "Referer": "https://npm.cpami.gov.tw/bed_1.aspx",
        "X-MicrosoftAjax":"Delta = true",
        "X-Requested-With":"XMLHttpRequest",
        "Content-Type":"application/x-www-form-urlencoded",
        ## "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"  ### Firefox
        ## "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" ### Chrome
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
         }
# 模擬 browser 作 get動作
# res = requests.get(url, headers=headers)
# print(res.text)
# soup = bs(res.text,"lxml")
# print(soup)
# room_dict={}

#for ele in soup.select("div.form-group select option"): ## 幫我抓 div物件中 class為 form-group >> select物件 >> option物件
#    if ele['value'] !="": 
#    #  print(int(ele['value']),ele.text)
#        room_dict[ele.text]=int(ele['value']) ### 將山屋名稱與編號存入字典 room_dict{}
#        room_dict

def parsing_hidden_params(soup):
    __VIEWSTATE = soup.select("input#__VIEWSTATE")[0]['value']
    __VIEWSTATEGENERATOR = soup.select("input#__VIEWSTATEGENERATOR")[0]['value']
    __EVENTVALIDATION = soup.select("input#__EVENTVALIDATION")[0]['value']
    output = {
            "__VIEWSTATE":__VIEWSTATE,
            "__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,
            "__EVENTVALIDATION":__EVENTVALIDATION
             }
    return output

## -- main --
with requests.session() as s:
    res = s.get(url,headers=headers)
    soup = bs(res.content, "lxml")
    p = parsing_hidden_params(soup)
    # print(p)
    payload={}
    payload["ctl00$ScriptManager1"]="ctl00$ScriptManager1|ctl00$ContentPlaceHolder1$btnsearch"
    payload["__EVENTTARGET"]=""
    payload["__EVENTARGUMENT"]=""
    payload["__VIEWSTATE"] = p["__VIEWSTATE"]
    payload["__VIEWSTATEGENERATOR"] = p["__VIEWSTATEGENERATOR"]
    payload["__EVENTVALIDATION"] = p["__EVENTVALIDATION"]
    payload["ctl00$txSerch"]=""
    payload["ctl00$ContentPlaceHolder1$rooms"] = 13
    payload["ctl00$ContentPlaceHolder1$ddlYear"] = 2020
    payload["ctl00$ContentPlaceHolder1$ddlMonth"] = 3
    payload["ctl00$ContentPlaceHolder1$hidYear"] = 2020
    payload["ctl00$ContentPlaceHolder1$hidMonth"] = 3
    payload["__ASYNCPOST"]="true"
    payload["ctl00$ContentPlaceHolder1$btnsearch"] = "查詢"
    #print(payload)
    print("="*80)
    #print(res.cookies.items())
    #headers["Cookie"]=res.cookies
    result = requests.post(url,data=payload,headers=headers,allow_redirects=False)
    #result = requests.post(url,data=payload,timeout=3.0)
    soup2 = bs(result.text,"lxml")
    #print(soup.select("div#ContentPlaceHolder1_CalendarDiv"))
    print(soup2)