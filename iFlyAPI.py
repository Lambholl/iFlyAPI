# -*- coding:utf-8 -*-
from flask import Flask, request
import time, _thread, os
from requests import post, get
from json import loads, load
from flask_compress import Compress
from collections import OrderedDict
from flask_cors import *
from random import randint
#常量定义区
#JSON_URL_HEAD = 'http://www.example/json/'
JSON_URL_HEAD = 'http://127.0.0.1:1234/'
JSON_PATH = 'E:/json/'
FILE_SIZE_NUM  = ['114514', '1919810', '10032', '20001']
FILE_SIZE_TYPE = ['GB', 'TB', 'MB', 'PB']
SEND_USER = 'Your name here'
SEND_ADMIN_MAIL = "example@gmail.com"

#函数定义区
def getJsonData(path):
    with open(JSON_PATH+path, mode='r', encoding='utf-8') as fb:
        json_data = load(fb)
        fb.close()
    return json_data

def getFileSize():
    file_size_num = FILE_SIZE_NUM[randint(0,len(FILE_SIZE_NUM)-1)]
    file_size_type = FILE_SIZE_TYPE[randint(0,len(FILE_SIZE_TYPE)-1)]
    return file_size_num + ' ' + file_size_type

def getLodePath(page, keyword):
    pass

#初始化
app = Flask(__name__)
CORS(app, supports_credentials=True)
Compress(app)
app.config['COMPRESS_MIMETYPES'] = ['application/json']

#jcservice/courseware/listStuClassDoc
@app.route('/jcservice/courseware/listStuClassDoc', methods=['POST', 'GET'])
def listStuClassDoc():
    # try:
        # kw=request.form['keyword']
    # except KeyError:
        # kw=''
    # try:
        # page=request.form['page']
    # except KeyError:
        # page=1
    # json_data = loads(post('http://127.0.0.1:30387/jcservice/courseware/listStuClassDoc', data={'page':page,'keyword':kw}).text)
    json_data = {
        'code': 1,
        'msg': '请求成功！',
        'data': [],
        'responsetime': int(round(time.time()*1000))
    }
    # url1 = JSON_URL_HEAD+'list.json'
    # resList = loads(get(url1).text)
    resList = getJsonData('list.json')
    try:
        keyword = request.form['keyword']
        # keyword = 'test'
        if keyword != '':
            try:
                page = int(request.form['page'])
                # page=1
                if page != 1:
                    # lode_json_url = []
                    lode_json_file = []
                else: 
                    # url2 = JSON_URL_HEAD+'hidden/hidden.json'
                    # hiddenResList = loads(get(url2).text)
                    hiddenResList = getJsonData('hidden/hidden.json')
                    for kwName in hiddenResList["data"]["keywords"]:
                        resFound = True if keyword == kwName else False
                        if resFound:
                            resNum = hiddenResList["data"]["keywords"].index(keyword)
                            resFile = hiddenResList["data"]["files"][resNum]
                            # lode_json_url = [JSON_URL_HEAD+"hidden/"+resFile+".json"]
                            lode_json_file = ["hidden/"+resFile+".json"]
                            break
                    # lode_json_url = [] if not resFound else lode_json_url
                    lode_json_file = [] if not resFound else lode_json_file
            except KeyError:
                # url2 = JSON_URL_HEAD+'hidden/hidden.json'
                # hiddenResList = loads(get(url2).text)
                hiddenResList = getJsonData('hidden/hidden.json')
                for kwName in hiddenResList["data"]["keywords"]:
                    resFound = True if keyword == kwName else False
                    if resFound:
                        resNum = hiddenRes["data"]["keywords"].index(keyword)
                        resFile = hiddenResList["data"]["files"][resNum]
                        # lode_json_url = [JSON_URL_HEAD+"hidden/"+resnFile+".json"]
                        lode_json_file = ["hidden/"+resnFile+".json"]
                        break
                # lode_json_url = [] if not resFound else lode_json_url
                lode_json_file = [] if not resFound else lode_json_file
        else:
            try:
                page = int(request.form['page'])
            except KeyError:
                page = 1
            if page <= 1:
                # lode_json_url = [
                    # JSON_URL_HEAD+resList["data"][0],
                    # JSON_URL_HEAD+resList["data"][1]
                # ]
                lode_json_file = [
                    resList["data"][0],
                    resList["data"][1]
                ]
            elif page >= len(resList["data"]):
                #lode_json_url = []
                lode_json_file = []
            else:
                #lode_json_url = [JSON_URL_HEAD+resList["data"][page]]
                lode_json_file = [resList["data"][page]]
    except KeyError:
        try:
            page = int(request.form['page'])
        except KeyError:
            page = 1
        if page <= 1:
            # lode_json_url = [
                # JSON_URL_HEAD+resList["data"][0],
                # JSON_URL_HEAD+resList["data"][1]
            # ]
            lode_json_file = [
                    resList["data"][0],
                    resList["data"][1]
                ]
        elif page >= len(resList["data"]):
            #lode_json_url = []
            lode_json_file = []
        else:
            #lode_json_url = [JSON_URL_HEAD+resList["data"][page]]
            lode_json_file = [resList["data"][page]]
    # for url3 in lode_json_url:
        # jsonFile = loads(get(url3).text)
    for path in lode_json_file:
        jsonFile = getJsonData(path)
        i = 0
        for v in jsonFile['data']:
            for n in v['data']:
                appendData = {
                    "displayname": SEND_USER,
                    "isdeleted": 0,
                    "commentcount": 3,
                    "docsize": getFileSize(),
                    "seecount": 1415,
                    "categoryname": v["type"],
                    "pirurls": [v["pic"]],
                    "bankname": v["name"],
                    "downloadurl": n["url"],
                    "dynamicid": n["docid"],
                    "title": v["name"]+' '+n["title"],
                    "datecreated": int(v["date"]),
                    "sendobject": None,
                    "convertstatus": 0,
                    "docid": n["docid"],
                    "doctype": v["doctype"],
                    "flowercount": 926,
                    "thumbpath": v["pic"]
                }
                appendData['thumbpath']='' if appendData['thumbpath']==None else appendData['thumbpath']
                appendData['pirurls']=[''] if appendData['pirurls']==[None] else appendData['pirurls']
                json_data['data'].append(appendData)
    # print(json_data)
    return json_data #, 200, {'Connect-Type':'application/json;charset=UTF-8','Transfer-Encoding':'chunked','Vary':'Accept-Encoding','Connection':'keep-alive'}
    #return str(page)

#jcservice/courseware/listStuAtDoc
@app.route('/jcservice/courseware/listStuAtDoc')
def listStuAtDoc():
    data = {
        "code": 1,
        "msg": "请求成功！",
        "data": [],
        "responsetime": int(round(time.time()*1000))
    }
    return data

#jcservice/Common/getSecretStr
@app.route('/jcservice/Common/getSecretStr', methods=['POST', 'GET'])
def getsecretstr():
    data = {
        "code":1,
        "data":{
            "accessKeyId":"LTAI4GEs3CXWXuQsWF5M68fE",
            "publicSecretStr":"AzGIX2uCA8m1bP9mfF3pN1EkXvwwULzRf4jLB0gG88fNYIxdd+47AhjBSTcTRETOozQhSTnGxpSP8G1rdo4NLZB3BMrA9uaRSkbAcfLxWh1AEPb2YiKwnkpSwsKKZWPGvxUSqspu73sptE3UmZQMzy\/XsAG7C4pI3Q4iRZ2sMew="
        },
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
        }
    return data

#jcservice/Common/listBanksByUserId
@app.route('/jcservice/Common/listBanksByUserId', methods=['POST', 'GET'])
def listBanksByUserId():
    data = {
        "code":1,
        "data":[
            {
                "title":"动漫",
                "iflycode":"01"
            }
        ],
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/Login/addLoginInfo
@app.route('/jcservice/Login/addLoginInfo', methods=['POST', 'GET'])
def addLoginInfo():
    data = {"code":1,
        "data":None,
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/Login/clientLogin
@app.route('/jcservice/Login/clientLogin', methods=['POST', 'GET'])
def clientLogin():
    data = {
        "code":1,
        "data":{
            "needchange":False,
            "schoolId":"学园都市-常盘台中学",
            "displayName":"御坂10032号",
            "id":request.form['safeid'],
            "cycoreId":"1500000100072243788",
            "successType":"center",
            "token":request.form['token'],
            "userType":2
        },
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/Message/getRecordCount
@app.route('/jcservice/Message/getRecordCount', methods=['POST', 'GET'])
def getRecordCount():
    data = {
        "code":1,
        "data":-1,
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/Message/judgeUpdate
@app.route('/jcservice/Message/judgeUpdate', methods=['POST', 'GET'])
def judgeUpdate():
    data = {
        "code":1,
        "data":-1,
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/SafeManage/checkStatus
@app.route('/jcservice/SafeManage/checkStatus', methods=['POST', 'GET'])
def CheckStatus():
    data = {
        "code":1,
        "data":-1,
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/Sign/getSignRecordToday
@app.route('/jcservice/Sign/getSignRecordToday', methods=['POST', 'GET'])
def getSignRecordToday():
    data = {
        "code":1,
        "data":{
            "dvalue":114514,
            "honorname":"超能力者",
            "issign":True,
            "isfull":False
        },
    "responsetime":int(round(time.time()*1000)),
    "msg":"请求成功！"
    }
    return data

#jcservice/Start/getStartPic
@app.route('/jcservice/Start/getStartPic', methods=['POST', 'GET'])
def getStartPic():
    data = {
        "code":1,
        "data":{
            "vPicUrl":"http://fs.yixuexiao.cn/title.png",
            "tPicUrl":"http://fs.yixuexiao.cn/title.png"
        },
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/User/getExpAndHonorInfo
@app.route('/jcservice/User/getExpAndHonorInfo', methods=['POST', 'GET'])
def getExpAndHonorInfo():
    data = {
        "code":1,
        "data":{
            "levelInfo":[
                {
                    "exp":9982,
                    "title":"LV1",
                    "level":1,
                    "name":"弱能力者"
                },
                {
                    "exp":10031,
                    "title":"LV2",
                    "level":2,
                    "name":"异能力者"
                },
                {
                    "exp":10086,
                    "title":"LV3",
                    "level":3,
                    "name":"强能力者"
                }
            ],
            "honorList":[],
            "levelList":[],
            "exgUserVo":{
                "exp":10032,
                "id":request.form['safeid'],
                "title":"LV2",
                "level":2,
                "name":"缺陷电气"
            }
        },
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/User/getUserDetailInfo
@app.route('/jcservice/User/getUserDetailInfo', methods=['POST', 'GET'])
def getUserDetailInfo():
    data = {
        "code":1,
        "data":{
            "userid":request.form['safeid'],
            "classname":"bilibili·狗·德川家康·薛定谔·保留",
            "opensubjectleader":0,
            "schooltype":"2",
            "schoolname":"常盘台中学",
            "displayname":"御坂10032号",
            "studySection":2,
            "hascommunity":0,
            "userroles":"",
            "isreg":False,
            "usertype":1,
            "schoolid":"r-juanomjrri5ezp5i-7gw",
            "txurl":"http://fs.yixuexiao.cn/10032.png",
            "email":"",
            "cycoreid":"1500000100072243788",
            "mobile":"",
            "bankid":"",
            "bankname":"",
            "isdevicelock":False,
            "username":"misaka10032"
        },
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#Netease/NEUser-getNEStudent
#@app.route('//Netease/NEUser-getNEStudent', methods=['POST', 'GET'])
def getNEStudent():
    data = {
        "msg":"success",
        "data":{
            "neUser":{
                "status":2,
                "cartoonUrl":"",
                "userName":"misaka10032",
                #"studentId":request.form['safeid'],
                "token":"","tutorCount":0,"accid":"","balance":0}},"code":200}
    return data

#forum/fsnoticehome-getUnreadMNcount
#@app.route('/forum/fsnoticehome-getUnreadMNcount')
def getUnreadMNcount():
    data = {
        "msg":"success",
        "data":{
            "neUser":{
                "status":2,
                "cartoonUrl":"",
                "userName":"misaka10032",
                "studentId":"6jrmapwrdy1kyrv38ky1la",
                "token":"",
                "tutorCount":0,
                "accid":"","balance":0
            }
        },
        "code":200
    }
    return data


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host='127.0.0.1', port=5000, debug=False
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=30389)
    #print(liststuclassdoc())
