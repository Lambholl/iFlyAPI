# iFlyAPI
通过搭建api服务器来改变畅言作业平台的内容
******
# 目录
> ### [思路](#p1)
> ### [准备工作](#p2)
> ### [搭建api](#p3)
> ### [DNS劫持](#p4)
******
# <span id="p1">思路</span>
通过网络抓包，我们可以发现畅言作业平台传输的数据基本上都是json格式。

同时，可以注意到，在登录界面有一个“修改域名”的选项。
![1](https://user-images.githubusercontent.com/55140169/112722683-eefcea80-8f45-11eb-9f45-ef590a0ebc0f.png)


通过抓包，我们可以了解到畅言作业平台请求的域名是`http://www.yixuexiao.cn`
也就是说通过“修改域名”可以更改请求连接。
>例：原本的请求链接是`http://www.yixuexiao.cn/jcservice/Login/clientLogin`，输入`http://api.example.com`并确认，请求的链接会变成`http://api.example.com/jcservice/Login/clientLogin`
那么，如果我们搭建一个api服务器来模拟原来的服务器，就可以修改其中的内容。
******
# <span id="p2">准备工作</span>
* 为了能够长期、稳定地运行api，我们需要一台服务器。
* 如果没有服务器，可以暂时使用本地电脑来配置，但是我不推荐这种做法。<b>如果你想要用这种方法，请查看[具体思路](#p5_1)。
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
******
# <span id="p3">搭建api</span>
* 首先，我们需要对畅言作业平台进行抓包。抓包工具的话，iOS建议选择[Stream](https://apps.apple.com/cn/app/stream/id1312141691)，安卓建议选择[HttpCanary](https://github.com/Lambholl/iFlyAPI/blob/main/tools/HttpCanary.apk)。
* 打开抓包工具，装好证书，开始抓包，然后用自己的账号登录畅言作业平台，尽量把每个页面都查看一遍，然后返回抓包工具，停止抓包。
* 接下来我们可以查看抓到的内容。

> 例：我们可以看到请求链接`http://www.yixuexiao.cn/jcservice/Start/getStartPic`，方式为`POST`，返回json数据为：
```json
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
```php
$time0 = explode(' ', microtime());
$time1 = sprintf('%d%03d',$time0[1], $time0[0] * 1000);
```
> Python:
```python
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
>> ## 看到这里，了解web搭建的小伙伴已经知道该怎么做了，那么你可以直接去看[文章结尾](#p4)了<br>
>> 对于还不会搭建的同学，或者想偷懒的同学，我推荐使用Python Flask

## Flask搭建思路
* 首先，你需要会Python，要是你连python都不会，那就先去学python吧，不管是看纸质书还是找在线教程
* 如果你看得懂廖雪峰版本的，那么我建议你去学[廖雪峰版本的Python教程](https://www.liaoxuefeng.com/wiki/1016959663602400)，当然学习的时候注重实例的开发，比如利用[LoliconAPI](https://api.lolicon.app/#/setu?id=apikey)写几个简单的脚本对其进行调用
* 如果你没接触过Python，在学习教程前，请你先安装python：
> 请去[Python官网](https://www.python.org)下载python。注意安装时的选项：
>> ![py1](https://user-images.githubusercontent.com/55140169/112722702-063bd800-8f46-11eb-9bc8-451f3cbe7442.png)
>> ![py2](https://user-images.githubusercontent.com/55140169/112722713-12c03080-8f46-11eb-96b4-57f8278c273e.png)

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
```python
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
> 关于epub:<br>  建议先用<b>Neat Converter</b>转成docx，再修改字体，导出pdf，如果行间距比较大用多倍行距设置成小于1的数值，千万不要使用固定行距，否则图片排版会出大问题。字体建议选择[XHei Intel](https://github.com/Lambholl/iFlyAPI/tree/main/tools/XHei_Intel.7z)，顺便分享一下一个特别美观的等距字体（中文严格为英文两倍）[XHei Intel Mono](https://github.com/Lambholl/iFlyAPI/tree/main/tools/XHei_Intel-Mono.7z)
* 为了方便维护，我建议将返回的数据另外存储到json文件中，下面先给出代码，稍后会讲解与之对应的json格式：
```python
from flask import Flask, request
import time, os
from json import load, loads
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
    # json_data = post('http://127.0.0.1:30387/jcservice/courseware/listStuClassDoc', data={'page':page,'keyword':kw}).json()
    # 以上这几行是提供转发本地php服务器返回结果的方法，因为php的运行速率要永远大于python，所有有兴趣的可以试试看，但是这种方法不推荐
    json_data = {
        'code': 1,
        'msg': '请求成功！',
        'data': [],
        'responsetime': int(round(time.time()*1000))
    }
    # 定义未找到结果时返回的json，不至于报错
    # url1 = JSON_URL_HEAD+'list.json'
    # resList = get(url1).json()
    # 上面这几行就是在线json文件的代码了，把注释去掉，再把下面那行注释掉就好了
    resList = getJsonData('list.json')
    # 下面的代码看着有点臃肿，但是我暂时也想不出更好的方法了(其实是懒得想)
    # 要用在线json的话修改注释就好了
    if 'keyword' in request.form:
        if request.form['page'] == 1 and request.form['keyword']!='':
            keyword = request.form['keyword']
            kws = getJsonData('hidden/hidden.json')
            lode_json_file = [JSON_PATH+'hidden/'+kws['files'][kws['keywords'].index(keyword)]+'.json'] if keyword in kws['keywords'] else []
            # lode_json_url = [JSON_URL_HEAD+'hidden/'+kws['files'][kws['keywords'].index(keyword)]+'.json'] if keyword in kws['keywords'] else []
        else:
            lode_json_file = []
            # lode_json_url = []
    else:
        page = int(request.form['page']) if 'page' in request.form else 1
        fileList = getJsonData(JSON_PATH+'list.json')['data']
        # fileList = get(JSON_URL_HEAD+'list.json').json()['data']
        if page < len(fileList):
            lode_json_file = [JSON_PATH+fileList[0], JSON_PATH+fileList[1]] if page==1 else [JSON_PATH+fileList[page]]
            # lode_json_url = [JSON_URL_HEAD+fileList[0], JSON_URL_HEAD+fileList[1]] if page==1 else [JSON_URL_HEAD+fileList[page]]
        else:
            lode_json_file = []
            # lode_json_url = []
    # for url3 in lode_json_url:
        # jsonFile = get(url3).json()
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
* ### 接下来讲解本地json的格式
> 举例: <br>存放json的文件夹的结构为:
>> list.json    - 列出所有可以加载的json文件<br>
>> head.json    - 总是保持在学案顶部的json文件，方便用来发送公告类文件<br>
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
* json文件的格式为:
> list.json
```json
{
  "status": 200,
  "data": [
    "head.json",
    "xx.json",
    "xxx.json"
  ]
}
```
> 这样在加载的时候，学案第一页返回head.json和xx.json，第二页返回xxx.json，第三页返回data留空的json (上面定义过的) <br>

> hidden.json
```json
{
  "status": 200,
  "data": {
    "files": [
      "../xx",
      "../xxx",
      "abc.json",
      "de.json"
    ],
    "keywords": [
      "某科学的超电磁炮",
      "路人女主的养成方法",
      "缘之空",
      "最近，我的妹妹有点奇怪？"
    ]
  }
}
```
> 其中files定义的是json文件，keywords定义的是关键词，只要搜索的关键词在keywords里面，就会获取其在列表里面的位置，并且获取files列表相同位置的值作为json文件<br>
> 值得注意的是，本文件中的json文件地址不需要加上json后缀名

> 其他json：
>> head.json
```json
{
  "status": 200,
  "data": [
    {
      "name": "资源列表",
      "date": "1616367600000",
      "type": "文档",
      "pic": null,
      "doctype": "pdf",
      "data": [
        {
          "title": "及 更新日志",
          "url": "http://fs.yixuexiao.cn/list/210322.pdf",
          "docid": "0.1014"
        }
      ]
    },
    {
      "name": "有bug或下载问题请反馈至",
      "date": "1612213200000",
      "type": "Notice",
      "pic": null,
      "doctype": "png",
      "data": [
        {
          "title": "example@gmail.com",
          "url": "http://fs.yixuexiao.cn/a.png",
          "docid": "0.0002"
        }
      ]
    }
  ]
}
```
>> xx.json
```json
{
  "status": 200,
  "data": [
    {
      "name": "某科学的超电磁炮",
      "date": "1254412800000",
      "type": "动漫",
      "pic": "http://fs.yixuexiao.cn/videos/chaopao/chaopao/cover.jpg",
      "doctype":"mp4",
      "data": [
        {
          "title": "第1话 电击使ElectroMaster",
          "url": "http://fs.yixuexiao.cn/videos/chaopao/chaopao/01.mp4",
          "docid": "3.101"
        },
        {
          "title": "第2话 炎日下工作必须补充水分",
          "url": "http://fs.yixuexiao.cn/videos/chaopao/chaopao/02.mp4",
          "docid": "3.102"
        },
        {
          "title": "第3话 被盯上的常盘台",
          "url": "http://fs.yixuexiao.cn/videos/chaopao/chaopao/03.mp4",
          "docid": "3.103"
        }
      ]
    }
  ]
}
```
> 由于代码中是遍历data中的每一个数据，因此自定义性得到了保证。<br>
> <b>注意</b>：docid是判断文档是否下载的唯一依据，假设有两个不同的文件的docid都是abcde，下载完其中一个时，另一个也会显示下载完成。因此为了便于区分，建议使用小数点分隔数字的方式或者干脆使用uuid<br>
> 最终合成文件名的方式为name+' '+title

* 这里我给出一个写好的py脚本以供参考:
   [iFlyAPI.py](https://github.com/Lambholl/iFlyAPI/blob/main/iFlyAPI.py)
******
# <span id='p4'>DNS劫持</span>
* <b>在畅言智慧课堂学生机里面，畅言作业平台是有白名单限制的。也就是说你就算修改了域名到你的服务器，还是会被拦截下来。</b><br>
  Q: 有什么方法可以通过白名单？<br>
  ~~A: 当然有，你把`www.yixuexiao.cn`买下来就好了~~<br>
  A: 在电脑上劫持DNS，再转发网络到学生机上面。<br>
  ![dnschange1](https://user-images.githubusercontent.com/55140169/112723438-6e3fed80-8f49-11eb-9313-4ff2a4fae124.png)<br>
* Q: 怎么劫持DNS?
  A: 电脑本地的DNS劫持，用的最多的就是修改hosts了，只要在hosts里面加上一行，就可以立马生效
  > 格式是`IP 劫持域名`，和我们平时的思路似乎不太一样。
  ### 但是如果你用对象存储和CDN，这种方法就会出问题。因为这样无法通过腾讯云或者阿里云的鉴权，会被认为是无效请求<br>
  所以我们需要采用迂回的方法：
    > 如果你的下载服务器是普通的服务器，那么你根本不需要使用此方法，直接修改hosts就行了
    1. 下载[开发者神器库_7](http://www.lingmax.top/)
    2. 打开你的IDC的控制台，打开对象存储-存储桶列表-域名与源站管理-自定义CDN加速域名，以腾讯云为例：![dnschange3](https://user-images.githubusercontent.com/55140169/112724983-d9d98900-8f50-11eb-92c9-10ea8bd57fa4.png)
    3. 打开CDN控制台，对你的CDN加速域名策略进行修改(被攻击了就亏大了)
    4. 打开你的域名管理，添加一条cname记录(你的IDC会告诉你一个cname什么内容)![dnschange4](https://user-images.githubusercontent.com/55140169/112725092-5d937580-8f51-11eb-8d73-0a1bf9aae38e.png)
    5. <span id='fin'>打开开发者神器库7，把`fs.yixuexiao.cn`指向你添加的记录</span>
    6. 打开“DNS劫持，添加一条规则，把`www.yixuexiao.cn`指向你的服务器![dnschange2](https://user-images.githubusercontent.com/55140169/112724782-e8737080-8f4f-11eb-84f3-9584d8e4605a.png)
*  打开设置-网络和Internet-移动热点，共享网络![dnschange5](https://user-images.githubusercontent.com/55140169/112725150-b531e100-8f51-11eb-9e28-375479d7ee4c.png)
<br>如果没有无线网卡，那就去买一个USB无线网卡吧
* 至此设置完成，把你填的下载链接全部替换掉，把学生机连上这个网络，修改域名（可以加上端口），登录，大功告成。


# 附录
## <span id='p5_1'>利用本地电脑搭建api服务器方法</span>
* 不是很推荐这种方法，当然如果你只是想临时用一下，就按照下面的方法来吧。<br><br>
* 因为只是临时用一下，下载服务器就放在本地好了；
> 因此劫持域名只需劫持一个，且不需要用到开发者神器库，只需修改`C:\Windows\System32\drivers\etc\hosts`就好了。<br>
> 修改建议使用[NotePad++](https://github.com/Lambholl/iFlyAPI/blob/main/tools/npp.7.9.5.Installer.x64.exe)，以管理员身份运行，不建议使用Windows自带记事本，当然如果你一定要用，请以管理员身份运行。<br>
* 在电脑上共享WiFi：
> ![dnschange5](https://user-images.githubusercontent.com/55140169/112725150-b531e100-8f51-11eb-9e28-375479d7ee4c.png)<br>
> 如果没有无线网卡，买个USB无线网卡凑合一下吧
* 用手机或者平板连上这个WiFi，打开WiFi详细信息，查看“路由器”的地址 
> ![dnschange6](https://user-images.githubusercontent.com/55140169/113497642-9c6c9100-9538-11eb-974a-c928986e8ba0.png)
* 在随便哪里加上一行 `“路由器”中显示的ip 空格 www.yixuexiao.cn`
> ![image](https://user-images.githubusercontent.com/55140169/113497680-dd64a580-9538-11eb-9e1c-c256b90eed97.png)
* 按照上面的方法运行iFlyAPI.py，当然里面的几项参数得自己修改，如果你嫌listStuClassDoc麻烦，可以直接定义一个`dict`，里面包含返回的数据，再直接`return`即可，参考别的几个函数。
* 下载服务器可以用`Flask`，具体函数写法请百度；当然也可以用`IIS`，毕竟比较方便。

# 如果还有什么疑问，可以在B站私聊我：[Lambholl](https://space.bilibili.com/32319246)，我会尽快回答
