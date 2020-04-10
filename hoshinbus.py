# -*- coding:utf-8 -*-
## crawler for 和欣客運
import requests
from bs4 import BeautifulSoup as bs
import time

url = "https://www.ebus.com.tw/online_trans/Web/Add_Step1.asp" ## 網路訂／購票須知 => 按 『我同意』[post]
url2 = "https://www.ebus.com.tw/online_trans/Web/Add_Step2.asp" ## 網路訂／購票 => 頁面會導到 addOrder.aspx
url3 = "https://www.ebus.com.tw/NetOrder/payOrder/addOrder.aspx" ## 輸入起訖站跟姓名、身分證、電話... 頁面.
url3_checkimg = "https://www.ebus.com.tw/NetOrder/CheckImageCode.aspx" ## 有驗證圖片數字需要由回傳 cookies解析[response.cookies明碼]

headers1={
    "Host":"www.ebus.com.tw",
    "Referer":"http://www.ebus.com.tw/ebus/top.html",
    "Connection":"keep-alive",
    "TE":"Trailers",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
}

payload1={
    "Agreement":"%A7%DA%A6P%B7N"
}

headers2={
    "Host":"www.ebus.com.tw",
    "Connection":"keep-alive",
    "TE":"Trailers",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Referer":"https://www.ebus.com.tw/online_trans/Web/Add_Step1.asp",    
}

### ===== function 預先定義區塊 =====

def get_personal_data(filename):
    filedata = []
    try:
        with open(filename,"r",encoding="utf8") as f6:
            filedata = f6.readlines()
    except:
        print("get_personal_data() didn't find a {} in the same directory! \n".format(filename))
        print("A new {} file will be created! Please try to fill up your data with another editor!".format(filename))
        with open(filename,"x",encoding="utf8") as f7:
            f7.close()
        with open(filename,"w",encoding="utf8") as f5:
            f5.write("id={}\n".format("id"))
            f5.write("name={}\n".format("name"))
            f5.write("tel={}\n".format("tel"))
        return ["id","name","tel"]
    else:
        return filedata
    
def parsing_hidden_params(soup):
    __VIEWSTATE = soup.select("input#__VIEWSTATE")[0]['value']
    __VIEWSTATEGENERATOR = soup.select("input#__VIEWSTATEGENERATOR")[0]['value']
#     __EVENTVALIDATION = soup.select("input#__EVENTVALIDATION")[0]['value']
    __VIEWSTATEENCRYPTED = soup.select("input#__VIEWSTATEENCRYPTED")[0]['value']
    __PREVIOUSPAGE = soup.select("input#__PREVIOUSPAGE")[0]['value']
    
    
    output = {
        "__VIEWSTATE":__VIEWSTATE,
        "__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,
#         "__EVENTVALIDATION":__EVENTVALIDATION
        "__VIEWSTATEENCRYPTED":__VIEWSTATEENCRYPTED,
        "__PREVIOUSPAGE":__PREVIOUSPAGE,
    }
    return output

### ==== parsing tools ========================================================================================
def parsing_checkcode(responsed):
    return responsed.cookies['CheckCode']

def parsing_station_str_from_id(station_id):
    clean_listGsStationId['B9']="台南六甲頂"
    return clean_listGsStationId[station_id]

def parsing_station_id_from_str(string):
    return listGsStationId[string][:2]

def parsing_route_id_from_str(string):
    ## mode=0傳回    id   str list
    ## mode=1傳回 station str list
    left_star_pos=listGsStationId[string].find("*")
    right_star_pos=listGsStationId[string].rfind("*")
    tmp_id_list = listGsStationId[string][left_star_pos+1:right_star_pos].split(",")
    return tmp_id_list

### ============================================================================================================    
    
### ==== test 準備這邊寫 parsing table =========================================================================
def parsing_table(soup):
    table_buslist=[]
    dict_buslist ={}
    ## dict ={ "time":             tr.select("td")[0].text, 
    ##         "empty_seatamount": tr.select("td")[2].text,
    ##         "next_trip_url":    tr.select("td a")[0].text,
    ##         "round_trip_url":   tr.select("td a")[1].text }         
    column =[]
    column = [ele.text for ele in soup.select("table#GView_GBusTime th")]
#     print(column)

    tdata=[]
    lnks=[]

    for tr in soup.select("table#GView_GBusTime tr")[1:]:
        tdata.append([tr.select("td")[gg].text for gg in range(0,6)])

    for tr in soup.select("table#GView_GBusTime tr")[1:]:
        lnks.append([tr.select("a")[gg]['href'] for gg in range(0,2)])

    total_buslist_count = len(soup.select("table#GView_GBusTime tr")[1:])

    for cnt in range(0,total_buslist_count):
        dict_buslist={}
        dict_buslist["num"] = cnt
        dict_buslist[column[0]]=tdata[cnt][0]
        dict_buslist[column[1]]=tdata[cnt][1]
        dict_buslist[column[2]]=tdata[cnt][2]
        dict_buslist[tdata[cnt][4]]=lnks[cnt][0]
        dict_buslist[tdata[cnt][5]]=lnks[cnt][1]

        table_buslist.append(dict_buslist)

#     print(table_buslist)    
    return table_buslist
### ============================================================================================================

### === main() =================================================================================================

filedata = get_personal_data("personal.txt")
p_txtCId=filedata[0].replace("\n","").replace("id=","")
p_txtCName=filedata[1].replace("\n","").replace("name=","")
p_txtCTel=filedata[2].replace("\n","").replace("tel=","")


### === connection process =====================================================================================
session1=requests.Session()
session1.headers = headers1

print("="*100,"\n=\n=\n= [python] 以下為 {} GET 後結果: \n=\n".format(url),"="*100)
response1 = session1.get(url)
print(response1)
soup1 = bs(response1.text,'lxml')
print(soup1.select("input"))





time.sleep(2)
print("="*100,"\n=\n=\n= [python] 以下為 {} POST 後結果: \n=\n".format(url2),"="*100)
response2 = session1.post(url2,headers=headers1,data=payload1)
print(response2)
soup2 = bs(response2.text,'lxml')
print(soup2.select("title"))



## ---- parsing soup2 頁面中的網頁網站資訊 ----
## ---- 1. 取得站點資料 for UI ----
SelectAddr = {}
for ele in soup2.select("select#SelectAddr option"):
#     print(ele.text, ele['value'])
    SelectAddr[ele.text] = ele['value']
# print(SelectAddr)
## ---- 2. 取得起訖資料 for UI ----
listGsStationId={}
clean_listGsStationId={}
for ele in soup2.select("select#listGsStationId option"):
    listGsStationId[ele.text]=ele['value']
    clean_listGsStationId[ele['value'][:2]]=ele.text
# print(listGsStationId)
# print(clean_listGsStationId)
## ---- 3. 取得日期資料 for UI ----
listGDate = {}
for ele in soup2.select("select#listGDate option"):
    listGDate[ele.text]=ele['value']
# print(listGDate)
## ---- 4. 取得時間資料 for UI ----
listGTime={}
for ele in soup2.select("select#listGTime option"):
    listGTime[ele.text]=ele['value']
# print(listGTime)
## --- parsing 工具使用測試: ---
print(parsing_station_id_from_str("新竹站"))
print(parsing_station_str_from_id('E1'))
print(parsing_route_id_from_str("新竹站"))
print([parsing_station_str_from_id(m) for m in parsing_route_id_from_str("新竹站")])





time.sleep(1)
print("="*100,"\n=\n=\n= [python] 以下為 {} GET 後結果: \n=\n".format(url3_checkimg),"="*100)
## ---- 再送一次 get到 url3_checkimg取得驗證碼資料:----
response3 = session1.get(url3_checkimg)
print(response3)
CheckCode = parsing_checkcode(response3)

### === 準備要送出的參數: ======================================================================================
p___EVENTTARGET=""
p___EVENTARGUMENT=""
p_tkData=""
p_Seat0Number=""
p_Seat1Number=""
p_defeStationId=""
p_SelectAddr="高雄市建國二路255號　Tel：(07)236-0209"
p_listGsStationId=listGsStationId['新竹站']
p_listGeStationId=parsing_station_id_from_str("臺南轉運站")
p_listGDate="2020/04/18"
p_listGTime="18:00,21:00"
p_txtChkCode=CheckCode
p_butgBusTimeList="下一步"

order_bus_time_payload={
    "__EVENTTARGET":p___EVENTTARGET,
    "__EVENTARGUMENT":p___EVENTARGUMENT,
    "tkData":p_tkData,
    "Seat0Number":p_Seat0Number,
    "Seat1Number":p_Seat1Number,
    "defeStationId":p_defeStationId,
    "SelectAddr":p_SelectAddr,
    "txtCName":p_txtCName,
    "txtCId":p_txtCId,
    "txtCTel":p_txtCTel,
    "listGsStationId":p_listGsStationId,
    "listGeStationId":p_listGeStationId,
    "listGDate":p_listGDate,
    "listGTime":p_listGTime,
    "txtChkCode":p_txtChkCode,
    "butgBusTimeList":p_butgBusTimeList,
}
p = parsing_hidden_params(soup2)
# print(p)
order_bus_time_payload["__VIEWSTATE"]=p["__VIEWSTATE"]
order_bus_time_payload["__VIEWSTATEGENERATOR"]=p["__VIEWSTATEGENERATOR"]
order_bus_time_payload["__VIEWSTATEENCRYPTED"]=p["__VIEWSTATEENCRYPTED"]
order_bus_time_payload["__PREVIOUSPAGE"]=p["__PREVIOUSPAGE"]

time.sleep(1)
print("="*100,"\n=\n=\n= [python] 以下為 {} POST 後結果: \n=\n".format(url3),"="*100)
response4 = session1.post(url3,headers=headers2,data=order_bus_time_payload)
print(response4)
soup4 = bs(response4.text,'lxml')
## ---- 先印出旅途資料測試是否得到目的網頁response ----
print(soup4.select("table span#label_gTravelData")[0].text)

## ---- parsing 出頁面中 table資料為list = [ { dict1 }, { dict2 },...{dictn} ] ----
target_table = parsing_table(soup4)
print(target_table)


## ---- 以下繼續寫接下來動作 ----



session1.close()


