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
> 此时我们可以观察到，responsetime使用的是毫秒时间戳，那么我们可以根据这个写出生成responsetime的代码：
> 
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
>> 如果使用php，那么需要使用[Apache](https://www.apache.org/)、[NGINX](https://www.nginx.com/)或者[Java](https://www.java.com/)，因为IIS的CGI模块比较nt，apache建议对apache比较熟悉并且熟悉url重写的人使用（反正我搞的url重写没成功过，因为我比较菜），如果你会Java，那么它当然也是一个很好的选择。
>> 
>> ## 看到这里，了解web搭建的小伙伴已经知道该怎么做了，那么你可以直接去看文章结尾了
>> 
>> 对于还不会搭建的同学，或者想偷懒的同学，我推荐使用Python Flask

## Flask搭建思路
* 首先，你需要会Python，要是你连python都不会，那就先去学python吧，不管是看纸质书还是找在线教程
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
    data = {"code":1,
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
## 待续
