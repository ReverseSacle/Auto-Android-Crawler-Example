## 前言

这是一个案例，涉及以下知识

- Appium Inspector工具的使用
- [→Appium-Python-Client库←](https://github.com/appium/python-client)
- 爬虫的基本逻辑
- 基本的解决问题逻辑思维

滑动判定的逻辑写的不太行，职位重复率大概在3%左右。

详情页面的滑动逻辑写的不太行，公司名丢失率在1%，要求特别多就有可能丢失。

页面详情页的点击逻辑也写的不太行，逻辑上是直接丢弃最后两个职位，目前都没到底。

从停留在职位选择页面开始计算，直到获取完全部信息再退出，消耗时间大于或等于13s。猜测占据大部分时间的是cv2的模板匹配，剩下大部分的就是Appium元素查找与获取文本的时间，最后剩下的就是网速问题了。



## 使用方法

测试用的是小米8 Lite，环境为Windows，IDE为Pycharm.

APP先手动登录一次。

先看看[→Android Debug Bridge(adb)教程←](https://www.reversesacle.com/computer-science/programming/android-development/automation-testing/adb-integration/)与[→Appium自动化测试←](https://www.reversesacle.com/computer-science/programming/android-development/automation-testing/appium-automated-testing/)。

PC端与手机端连接同一网络，或者用USB连接。

修改`config.py`中的个别变量

- capabilities变量 - platformVersion改为你的手机的安卓版本
- adb变量 - 将`192.168.55.153:5555`改为`你手机的ip地址:5555`或USB数据线连接后通过cmd输入`adb devices`出现的值中`devies`前面的字段

```tex
### button_location.py文件
通过Appium Inspector定位`button_location.py`里的元素坐标，
用的是中间值(就是左上坐标叫右下坐标的和再除以2)，
只有`first_card`的计算方法是不一样的(x轴取中间值，y轴取右下坐标的y轴值减去100左右)，
基本`button_location.py`文件所有变量的坐标都要改，
因为手机的像素不同，坐标会发生改变。

app body的分辨率用Appium Inspector打开左上角的一个圆圈有个×的图标，
选择中心位置的一个圆圈有个×的图标，点击后选择左边的小方格，
右边可以看到bounds值，第二个[]就是该resolution的变量值了。
```

`main.py`为主入口，直接Run就行了。


## 留言
爬取一定量时，该app会采取反制措施，解决方法就是不用Appium，直接用adb + python + 图像处理(附加OCR识别)，但是OCR识别文字后，还要考虑文字输出格式/段落/属于哪部分等问题。
