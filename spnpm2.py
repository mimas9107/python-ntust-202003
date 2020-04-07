# -*- coding:utf-8 -*-
## crawler 01
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


url = "https://npm.cpami.gov.tw/bed_1.aspx" ## 雪霸國家公園,登山入園床位查詢
headers ={
#             "Accept-Encoding": "gzip, deflate, br",
#             "Accept-Language": "zh-TW,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-JP;q=0.6,en;q=0.5,en-US;q=0.4",
#             "Cache-Control": "max-age=0",
            "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
            "Connection": "keep-alive",
#             "Cookie": "_ga=GA1.3.1596303645.1585377873; _gid=GA1.3.499809129.1585377873; _gat=1",
            "DNT": "1",
            "Origin":"https://npm.cpami.gov.tw",
            "Referer":"https://npm.cpami.gov.tw/bed_1.aspx",
            "Host": "npm.cpami.gov.tw",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "none",
#             "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
# 模擬 browser 作 get動作
res = requests.get(url, headers=headers)
# print(res.text)
soup = bs(res.text,"lxml")
# print(soup)

def parsing_room_dict(soup):
    room_dict={}

    for ele in soup.select("div.form-group select option"): ## 幫我抓 div物件中 class為 form-group >> select物件 >> option物件
        if ele['value'] !="": 
    #         print(int(ele['value']),ele.text)

            room_dict[ele.text]=int(ele['value']) ### 將山屋名稱與編號存入字典 room_dict{}
    return room_dict
result_rooms=parsing_room_dict(soup)
# print(result_rooms)

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
### ========= 將 ASP網頁的隱藏參數由 get中取得，並 parsing進 p字典中 ===========
p = parsing_hidden_params(soup)
# print(p)

# payload["ctl00$ScriptManager1"]="ctl00$ScriptManager1|ctl00$ContentPlaceHolder1$btnsearch"
# payload["__EVENTTARGET"]=""
# payload["__EVENTARGUMENT"]=""
# payload["__VIEWSTATE"] = p["__VIEWSTATE"]
# payload["__VIEWSTATEGENERATOR"] = p["__VIEWSTATEGENERATOR"]
# payload["__EVENTVALIDATION"] = p["__EVENTVALIDATION"]
# payload["ctl00$ContentPlaceHolder1$rooms"] = "13"
# payload["ctl00$ContentPlaceHolder1$ddlYear"] = "2020"
# payload["ctl00$ContentPlaceHolder1$ddlMonth"] = "4"
# payload["ctl00$ContentPlaceHolder1$hidYear"] = "2020"
# payload["ctl00$ContentPlaceHolder1$hidMonth"] = "4"

# payload["__ASYNCPOST"]="true"

# payload["ctl00$ContentPlaceHolder1$btnsearch"] = "查詢"
# payload["ctl00$txSerch"]=""

## ==== 字碼問題
## $ -> %24, | -> %7
## ====

payload={
    "ctl00$ScriptManager1": "ctl00$ScriptManager1|ctl00$ContentPlaceHolder1$btnsearch",
#     "ctl00%24ScriptManager1": "ctl00%24ScriptManager1%7ctl00%24ContentPlaceHolder1%24lbDownMonth",
    "__EVENTTARGET":"",
#     "__EVENTTARGET":"ctl00%24ContentPlaceHolder1%24lbDownMonth",
#      "__EVENTARGUMENT":"",
    "ctl00$txSerch":"",
#     "ctl00%24txSerch":"", 
    "ctl00$ContentPlaceHolder1$rooms": "13",
#     "ctl00%24ContentPlaceHolder1%24rooms": "13",
### ========== 這裡需要注意傳入的變數名稱字元 $ -> %24 可能有所差異，傳錯可能不成功，要多測試 ==========
    "ctl00%24ContentPlaceHolder1%24ddlYear": "2020",
    "ctl00%24ContentPlaceHolder1%24ddlMonth": "5",
    "ctl00%24ContentPlaceHolder1%24hidYear": "2020",
    "ctl00%24ContentPlaceHolder1%24hidMonth": "5",
#     "ctl00$ContentPlaceHolder1$ddlYear": "2020",
#     "ctl00$ContentPlaceHolder1$ddlMonth": "5",
#     "ctl00$ContentPlaceHolder1$hidYear": "2020",
#     "ctl00$ContentPlaceHolder1$hidMonth": "5",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl01$HiddenField1": "10",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl02$HiddenField1": "386",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl03$HiddenField1": "13",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl04$HiddenField1": "17",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl05$HiddenField1": "387",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl06$HiddenField1": "58",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl07$HiddenField1": "409",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl08$HiddenField1": "410",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl09$HiddenField1": "63",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl10$HiddenField1":"411",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl11$HiddenField1": "412",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl12$HiddenField1": "68",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl13$HiddenField1": "304",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl14$HiddenField1": "389",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl15$HiddenField1": "390",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl16$HiddenField1": "391",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl17$HiddenField1": "392",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl18$HiddenField1": "393",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl19$HiddenField1": "394",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl20$HiddenField1": "395",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl21$HiddenField1": "396",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl22$HiddenField1": "400",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl23$HiddenField1": "401",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl24$HiddenField1": "397",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl25$HiddenField1": "398",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl26$HiddenField1": "399",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl27$HiddenField1": "79",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl28$HiddenField1": "83",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl29$HiddenField1": "85",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl30$HiddenField1": "413",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl31$HiddenField1": "414",
#     "ctl00$ContentPlaceHolder1$Repeater_List$ctl32$HiddenField1": "382",
     "__ASYNCPOST": "true",
     "ctl00$ContentPlaceHolder1$btnsearch": "查詢",
}
# for kk in payload:
#     payload[kk.replace("$","%24").replace("|","%7")]=payload[kk].replace("$","%24").replace("|","%7")
    
# print(payload)

payload["__VIEWSTATE"] = p["__VIEWSTATE"]
payload["__VIEWSTATEGENERATOR"] = p["__VIEWSTATEGENERATOR"]
payload["__EVENTVALIDATION"] = p["__EVENTVALIDATION"]

### ========= 將欲查詢的 payload用 post傳入，取得結果 ==========
result2 = requests.post(url,data=payload,headers=headers,timeout=5.0)
soup2 = bs(result2.text,"lxml")
# print(soup2)

def parsing_updated_hidden_params(soup_update):
    a1 = soup_update.find("body").text.find("Field|__VIEWSTATE|")
    a2 = soup_update.find("body").text.find("|8|hid")
    # print(soup2.find("body").text[a1+18:a2])
    new_VIEWSTATE = soup_update.find("body").text[a1+18:a2]
#     print(new_VIEWSTATE)
    b1 = soup_update.find("body").text.find("1436|hiddenField")
    b2 = soup2.find("body").text.find("|327|asyncPostBackControlIDs")
    # print(soup2.find("body").text[b1+35:b2])
    new_EVENTVALIDATION = soup2.find("body").text[b1+35:b2]
#     print(new_EVENTVALIDATION)
    return {"__VIEWSTATE":new_VIEWSTATE,
            "__EVENTVALIDATION":new_EVENTVALIDATION}

### ========= 更新p字典中__VIEWSTATE 及 payload ===========
p = parsing_updated_hidden_params(soup2)
payload["__VIEWSTATE"] = p["__VIEWSTATE"]
payload["__EVENTVALIDATION"] = p["__EVENTVALIDATION"]
# print(soup2)

####======================================================================================
def parsing_date_from_url(str_url):
    if str_url!="": 
        output_str=str_url[str_url.find("sdate="):len(str_url)].replace("sdate=","")
    else:
        output=""
    return output_str
#### =====================================================================================
def parsing_calendar(soup_table):
    ## <td> <span id="ContentPlaceHolder1_cb_XX" > # 此為月曆日期儲存格 XX=01~37
    ## <td> <span id="ContentPlaceHolder1_cc_YY" > # 此為對應日期的床位詳細內容儲存格
    ## 回傳資料結構:    [ {dict1}, {dict2}, ... ,[dictX] ]
#     print(soup_table)
    dict_calendar={}
    output_calendar=[]
    for i in range(1,38):        
        for ele in soup_table.select("span[id='ContentPlaceHolder1_cc_{:2d}'] div.table-responsive".format(i)):
            dict_calendar["num"]=int(i)
            dict_calendar["日期"]=parsing_date_from_url(ele.select("a")[0]["href"])
            dict_calendar["餘額"]=int(ele.select("span")[0].text)        
            dict_calendar["待處理"]=int(ele.select("span")[1].text)            
            dict_calendar["補件"]=int(ele.select("span")[2].text)            
            dict_calendar["已通過"]=int(ele.select("span")[3].text)            
            dict_calendar["待排"]=int(ele.select("span")[4].text)            
            dict_calendar["候補"]=int(ele.select("span")[5].text)
            dict_calendar["URL"]="https://npm.cpami.gov.tw/"+ele.select("a")[0]["href"]
            if len(ele.select("span")) > 6 :
                dict_calendar["外籍"]=ele.select("span")[6].text
#             print("-"*80)
        output_calendar.append(dict_calendar)
        dict_calendar={}

    return output_calendar
#### =====================================================================================

result_cal = parsing_calendar(soup2)
print(result_cal)

payload={
#     "ctl00$ScriptManager1": "ctl00$ScriptManager1|ctl00$ContentPlaceHolder1$btnsearch",
     "ctl00$ScriptManager1": "ctl00$ScriptManager1|ctl00$ContentPlaceHolder1$lbDownMonth",
#     "__EVENTTARGET":"",
     "__EVENTTARGET":"ctl00$ContentPlaceHolder1$lbDownMonth",
#      "__EVENTARGUMENT":"",
    "ctl00$txSerch":"",
#     "ctl00%24txSerch":"", 
    "ctl00$ContentPlaceHolder1$rooms": "13",
#     "ctl00%24ContentPlaceHolder1%24rooms": "13",
### ========== 這裡需要注意傳入的變數名稱字元 $ -> %24 可能有所差異，傳錯可能不成功，要多測試 ==========
    "ctl00%24ContentPlaceHolder1%24ddlYear": "2020",
    "ctl00%24ContentPlaceHolder1%24ddlMonth": "6",
    "ctl00%24ContentPlaceHolder1%24hidYear": "2020",
    "ctl00%24ContentPlaceHolder1%24hidMonth": "5",
#     "ctl00$ContentPlaceHolder1$ddlYear": "2020",
#     "ctl00$ContentPlaceHolder1$ddlMonth": "7",
#     "ctl00$ContentPlaceHolder1$hidYear": "2020",
#     "ctl00$ContentPlaceHolder1$hidMonth": "7",
     "__ASYNCPOST": "true",
     "ctl00$ContentPlaceHolder1$btnsearch": "查詢",
}
p = parsing_updated_hidden_params(soup2)
payload["__VIEWSTATE"] = p["__VIEWSTATE"]
payload["__EVENTVALIDATION"] = p["__EVENTVALIDATION"]
payload["__VIEWSTATEGENERATOR"] = p["__VIEWSTATEGENERATOR"] = "545015F6"

### ========= 將欲查詢的 payload用 post傳入，取得結果 ==========
result3 = requests.post(url,data=payload,headers=headers,timeout=10.0)
soup3 = bs(result3.text,"lxml")
### ========= 更新p字典中__VIEWSTATE 及 payload ===========
# p = parsing_hidden_params(soup3)
# payload["__VIEWSTATE"] = p["__VIEWSTATE"]
# payload["__VIEWSTATEGENERATOR"] = p["__VIEWSTATEGENERATOR"]
# payload["__EVENTVALIDATION"] = p["__EVENTVALIDATION"]
print(soup3)


