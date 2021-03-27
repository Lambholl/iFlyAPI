# iFlyAPI
通过搭建api服务器来改变畅言作业平台的内容
******
# 目录
> ### [思路](#p1)
> ### [准备工作](#p2)
> ### [搭建api](#p3)
******
# <span id="p1">思路</span>
通过网络抓包，我们可以发现畅言作业平台传输的数据基本上都是json格式。

同时，可以注意到，在登录界面有一个“修改域名”的选项。
![avatar](https://github.com/Lambholl/iFlyAPI/blob/main/images/1.png)

通过抓包，我们可以了解到畅言作业平台请求的域名是`http://www.yixuexiao.cn`
也就是说通过“修改域名”可以更改请求连接。
>例：原本的请求链接是`http://www.yixuexiao.cn/jcservice/Login/clientLogin`，输入`http://api.example.com`并确认，请求的链接会变成`http://api.example.com/jcservice/Login/clientLogin`
那么，如果我们搭建一个api服务器来模拟原来的服务器，就可以修改其中的内容。

# <span id="p2">准备工作</span>
* 为了能够长期、稳定地运行api，我们需要一台服务器。
* 如果没有服务器，可以暂时使用本地电脑来配置，但是我不推荐这种做法。
* 以下问题解答提供给新手：
  > 在哪里能租到服务器?
  >> 在资金充裕的情况下，我建议你选择大型IDC，如[阿里云](https://cn.aliyun.com/)、[腾讯云](https://cloud.tencent.com/)。你可以选择使用学生优惠租借轻量级应用服务器，那是这两家服务商提供的最优惠的方案。当然，你也可以选择华为云、旋律云这类次一级的服务商，他们不提供独立ip，因此只能提供给你几个特定的端口，但是对于这个用途来说，那些端口是足够使用的，而且他们从整体来说更优惠。
  >
  > 我应该选择什么配置的服务器？
  >> 如果只是搭个网页服务器，1H1G1M是够用的（当然，在可能的情况下，尽量选择比较大的带宽。如果你租的服务器是共享ip的，尽量选择5M以上的带宽。独立ip由于带宽成本较大，不用追求带宽，毕竟1M给十几个人同时用也没什么问题。如果你想进行其他开发或者想让系统更稳定，建议选择2H4G以上。
  >
  > 我应该给服务器选择安装什么系统？
  >> 在服务器配置足够的情况下，我推荐你安装Windows Server，因为大多数人都熟悉Windows系统。同时，我推荐你使用Windows Server 2019，此版本和Windows 10的操作体验相似，并且拥有相对来说最完善的开发环境。如果你对Linux系统比较熟悉，那么你当然也可以选择Ubuntu 18.04或者CentOS 7。
* 由于我们租到的服务器带宽有限，所以不适合提供文件下载功能，因此我们需要租借[阿里云](https://cn.aliyun.com/)或者[腾讯云](https://cloud.tencent.com/)的对象存储服务，同时为了节省经费，我建议开通CDN(内容分发网络)，并且将加速策略设置为“文件下载加速”。

# <span id="p3">搭建api</span>
* 首先，我们需要对畅言作业平台进行抓包。抓包工具的话，iOS建议选择[Stream](https://apps.apple.com/cn/app/stream/id1312141691)，安卓建议选择[HttpCanary](https://github.com/Lambholl/iFlyAPI/blob/main/tools/HttpCanary.apk)。
* 打开抓包工具，装好证书，开始抓包，然后用自己的账号登录畅言作业平台，尽量把每个页面都查看一遍，然后返回抓包工具，停止抓包。
* 接下来我们可以查看抓到的内容。

> 例：我们可以看到请求链接`http://www.yixuexiao.cn/jcservice/Start/getStartPic`，方式为`POST`，返回json数据为：
```
{
  "code": 1,
  "msg": "请求成功！",
  "data": {
    "vPicUrl": "http://fs.yixuexiao.cn/aliba/upload/doc/19/05/27/1024ab2a-0e48-8b99-565b-f4734a069c71/0.0.png",
    "tPicUrl": "http://fs.yixuexiao.cn/aliba/upload/doc/19/05/27/c6e1f96f-728c-871c-0701-fb62e04c2df8/0.0.png"
  },
  "responsetime": 1616308980000
}
```
> 此时我们可以观察到，responsetime使用的是毫秒时间戳，那么我们可以根据这个写出生成responsetime的代码：<br>
> php:
```
$time0 = explode(' ', microtime());
$time1 = sprintf('%d%03d',$time0[1], $time0[0] * 1000);
```
> Python:
```
import time
def getCurrentTime():
    result = int(time.time()*1.0e3)
    return result
#写成函数是为了方便调用
#php不写成函数是因为一次请求运行一次php，而python的Flask则是一直运行的状态
```

* 接下来的思路就简单了，我们可以使用php或者Flask来搭建这个api服务器。当然为了防止bug，返回的内容一定要写全了。
> 那么应该如何选择用php或者python呢？
>> 如果使用php，那么需要使用[Apache](https://www.apache.org/)、[NGINX](https://www.nginx.com/)或者[Java](https://www.java.com/)，因为IIS的CGI模块比较nt，apache建议对apache比较熟悉并且熟悉url重写的人使用（反正我搞的url重写没成功过，因为我比较菜），如果你会Java，那么它当然也是一个很好的选择。<br>
>> ## 看到这里，了解web搭建的小伙伴已经知道该怎么做了，那么你可以直接去看文章结尾了<br>
>> 对于还不会搭建的同学，或者想偷懒的同学，我推荐使用Python Flask

## Flask搭建思路
* 首先，你需要会Python，要是你连python都不会，那就先去学python吧，不管是看纸质书还是找在线教程
* 如果你看得懂廖雪峰版本的，那么我建议你去学[廖雪峰版本的Python教程](https://www.liaoxuefeng.com/wiki/1016959663602400)，当然学习的时候注重实例的开发，比如利用[LoliconAPI](https://api.lolicon.app/#/setu?id=apikey)写几个简单的脚本对其进行调用
* 如果你没接触过Python，在学习教程前，请你先安装python：
> 请去[Python官网](https://www.python.org)下载python。注意安装时的选项：
>> ![avatar](https://github.com/Lambholl/iFlyAPI/blob/main/images/py1.png)
>> ![avatar](https://github.com/Lambholl/iFlyAPI/blob/main/images/py2.png)
> 接下来安装依赖:
>> 先更改默认pypi源为tuna:
>> 
>>> `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
>>> 
>> 如果提示升级pip可以运行:
>> 
>>> `python -m pip install --upgrade pip`
>> 
>> 接着安装:
>>> `pip install Flask, requests, flask_compress, flask_cors`
* 对于大部分页面，我们可以直接返回固定不变的json数据，这里给出一个例子(当然这个例子不完全)
```
#example.py

from flask import Flask, request

#实例化
app = Flask(__name__)

#定义api返回
#jcservice/Login/addLoginInfo
@app.route('/jcservice/Login/addLoginInfo', methods=['POST', 'GET'])
#加入GET是为了方便用浏览器进行调试，实际使用过程中，可以把GET去掉
def addLoginInfo():
    #取这个函数名是为了方便辨别
    data = {
        "code":1,
        "data":None,
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

#jcservice/Login/clientLogin
@app.route('/jcservice/Login/clientLogin', methods=['POST'])
def clientLogin():
    data = {
        "code":1,
        "data":{
            "needchange":False,
            "schoolId":"学园都市-常盘台中学",
            "displayName":"御坂10032号",
            "id":requests.form['safeid'],
            "cycoreId":"1500000100072243788",
            "successType":"center",
            "token":requests.form['token'],
            "userType":2
        },
        "responsetime":int(round(time.time()*1000)),
        "msg":"请求成功！"
    }
    return data

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host='127.0.0.1', port=5000, debug=False
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8888)
    # 端口的话看你的服务器有哪些端口，选择能使用的端口，记得在防火墙里面开放端口，协议选择tcp。
    # 考虑到国内80端口需要备案，一般不建议使用80端口，当然请避开21 22 80 8080 433 3389
    # 畅言作业平台的“修改域名”支持加端口，所以请放心
```
* 进行测试：
```
>>>import requests
>>>url0 = 'http://127.0.0.1:8888/jcservice/Login/addLoginInfo'
>>>requests.post(url0).text
'{"code":1,"data":null,"msg":"请求成功！","responsetime":1616847952190}\n'
>>>
```
> 当然代码里面允许了GET，也可以用浏览器来测试
* <b>就这样，按照你的思路复制一遍科大讯飞的服务器的返回数据</b>，并不是特别困难（虽然可能有点麻烦）
* ### 当然，重头戏在于<u><b>/jcservice/courseware/listStuClassDoc</b></u>
* 为什么这么说呢，因为修改了这个就可以利用你搭建的服务器<b>向畅言智慧课堂学生机里面传文件</b>。虽然文件格式只支持以下几种：
> mp4<br>
> pdf<br>
> ppt<br>
> pptx<br>
> doc<br>
> docx<br>
> mp3<br>
> xls<br>
> xlsx<br>
* 假设你愿意把视频用ffmpeg转码成mp4，把音频用ffmpeg转码成mp3，把下载的epub文件转换成pdf，那么就可以解决绝大多数问题
> 关于epub:<br>  建议先用<b>Neat Converter</b>转成docx，再修改字体，导出pdf，如果行间距比较大用多倍行距设置成小于1的数值，千万不要使用固定行距，否则图片排版会出大问题。字体建议选择[XHei Intel](https://github.com/Lambholl/iFlyAPI/tree/main/tools/XHei_Intel.7z)，顺便分享一下一个特别美观的等距字体（中文严格为英文两倍）[XHei Inrwl Mono](https://github.com/Lambholl/iFlyAPI/tree/main/tools/XHei_Intel-Mono.7z)
* 为了方便维护，我建议将返回的数据另外存储到json文件中
> 举例: <br>存放json的文件夹的结构为:
>> list.json    - 列出所有可以加载的json文件<br>
>> xx.json      - 在list.json中列出的文件名<br>
>> xxx.json <br>
>> hidden       - 定义隐藏文件和搜索功能的文件夹<br>
>>> hidden.json - 列举出所有搜索的关键词与其匹配的json文件<br>
>>> abc.json    - hidden.json中被列举但在../list.json中未被列举的json文件，保存在这里以便区分<br>
>>> de.json
>>> 
>> backup       - 备份文件夹，为了防止误删导致数据丢失，建议在别的地方多弄几个备份文件夹<br>
>>> xx.json <br>
>>> xxx.json <br>
>>> abc.json <br>
>>> de.json <br>
```
from flask import Flask, request
import time, os
from json import load
from flask_compress import Compress
from collections import OrderedDict
from flask_cors import *
from requests import get

#定义常量
JSON_PATH = 'E:/json/' #本地json文件存储文件夹
JSON_URL_HEAD = 'http://www.example.com/json/' #当然你也可以存放在web端，只需要取消下面代码中的注释，然后把原来的代码注释掉就可以了
SEND_USER = 'Lambholl'
FILE_SIZE = '114514 TB'

#函数定义区
def getJsonData(path):
    with open(JSON_PATH+path, mode='r', encoding='utf-8') as fb:
        json_data = load(fb)
        fb.close()
    return json_data

#初始化
app = Flask(__name__)
CORS(app, supports_credentials=True)
Compress(app)
app.config['COMPRESS_MIMETYPES'] = ['application/json']  #启用了gzip压缩

#jcservice/courseware/listStuClassDoc 返回的数据
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
    # 以上这几行是提供转发本地php服务器返回结果的方法，因为php的运行速率要永远大于python，所有有兴趣的可以试试看，但是这种方法不推荐
    json_data = {
        'code': 1,
        'msg': '请求成功！',
        'data': [],
        'responsetime': int(round(time.time()*1000))
    }
    # 定义未找到结果时返回的json，不至于报错
    # url1 = JSON_URL_HEAD+'list.json'
    # resList = loads(get(url1).text)
    # 上面这几行就是在线json文件的代码了，把注释去掉，再把下面那行注释掉就好了
    resList = getJsonData('list.json')
    # 下面的代码看着有点臃肿，但是我暂时也想不出更好的方法了(其实是懒得想)
    # 要用在线json的话修改注释就好了
    try:
        keyword = request.form['keyword']
        #keyword = 'rzxyuan'
        if keyword != '':
            try:
                page = int(request.form['page'])
                #page=1
                if page != 1:
                    #lode_json_url = []
                    lode_json_file = []
                else: 
                    #url2 = JSON_URL_HEAD+'hidden/hidden.json'
                    #hiddenResList = loads(get(url2).text)
                    hiddenResList = getJsonData('hidden/hidden.json')
                    for kwName in hiddenResList["data"]["keywords"]:
                        resFound = True if keyword == kwName else False
                        if resFound:
                            resNum = hiddenResList["data"]["keywords"].index(keyword)
                            resFile = hiddenResList["data"]["files"][resNum]
                            #lode_json_url = [JSON_URL_HEAD+"hidden/"+resFile+".json"]
                            lode_json_file = ["hidden/"+resFile+".json"]
                            break
                    #lode_json_url = [] if not resFound else lode_json_url
                    lode_json_file = [] if not resFound else lode_json_file
            except KeyError:
                #url2 = JSON_URL_HEAD+'hidden/hidden.json'
                #hiddenResList = loads(get(url2).text)
                hiddenResList = getJsonData('hidden/hidden.json')
                for kwName in hiddenResList["data"]["keywords"]:
                    resFound = True if keyword == kwName else False
                    if resFound:
                        resNum = hiddenRes["data"]["keywords"].index(keyword)
                        resFile = hiddenResList["data"]["files"][resNum]
                        #lode_json_url = [JSON_URL_HEAD+"hidden/"+resnFile+".json"]
                        lode_json_file = ["hidden/"+resnFile+".json"]
                        break
                #lode_json_url = [] if not resFound else lode_json_url
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
                    "docsize": FILE_SIZE, # 这里采用了偷懒的方法，如果你有兴趣，也可以获取到文件大小再返回，但是这样做会导致效率大大降低，可能导致不能及时返回数据
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
                # 为了美观用了三目表达式，希望不会影响运行效率
                json_data['data'].append(appendData)
    # print(json_data)  #这行用来debug
    return json_data

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=30389)
```
## 待续
