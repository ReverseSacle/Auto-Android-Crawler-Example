## 前言

这只是一个案例，安卓版Boss直聘APP自动化浏览。

可获取的信息包括 

- 职位
- 薪资
- 工作地点
- 经验要求/学历要求
- 职位要求详情页的全部信息
- 工作相关标签
- 公司名
- 公司详情
- 职位要求详情页链接。

该项目涉及以下知识

- Appium Inspector工具的使用
- [→Appium-Python-Client库←](https://github.com/appium/python-client)
- 爬虫的基本逻辑
- 基本的解决问题逻辑思维

网络通畅的情况下，速率为：[4s~6s]/篇。

经测试1s/篇的速率特别容易被封，账号有限，不推荐太高速率。

由于其岗位只能选特定地区，因此建议以多进程配合多账号的形式进行信息聚合。



## 使用方法

测试用的是小米8 Lite，环境为Windows，IDE为Pycharm.

APP先手动登录一次。

先看看[→Android Debug Bridge(adb)教程←](https://www.reversesacle.com/computer-science/programming/android-development/automation-testing/adb-integration/)与[→Appium自动化测试←](https://www.reversesacle.com/computer-science/programming/android-development/automation-testing/appium-automated-testing/)。

PC端与手机端连接同一网络，该方法容易`device offline`，推荐用USB连接。

修改`config.py`中的个别变量

- capabilities变量 - platformVersion改为你的手机的安卓版本
- adb变量
  - WIFI连接 - 将`192.168.55.153:5555`改为`你手机的ip地址:5555`
  - USB数据线连接 - 通过cmd输入`adb devices`出现的值中`devies`前面的字段


`main.py`为主入口，直接Run就行了。


## 留言
爬取一定量时(大概在70条左右)，该app会采取反制措施，强制隐藏UI元素。

解决方法就是不用Appium，直接用adb + python + OCR的方式，但是OCR识别文字后，还要考虑文字输出格式/段落/属于哪部分等问题，该逻辑部分需手动实现。
