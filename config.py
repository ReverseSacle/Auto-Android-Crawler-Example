############################# Appium #############################
boss_appPackage = 'com.hpbr.bosszhipin'
boss_appActivity = 'com.hpbr.bosszhipin.module.launcher.WelcomeActivity'

capabilities = dict(
    platformName='Android',
    platformVersion='9',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage=boss_appPackage,
    appActivity=boss_appActivity,
    noReset=True
)

appium_server_url = 'http://localhost:4723'
# device_name = '192.168.55.153:5555'
device_name = '6a29887'
adb = f'adb -s {device_name}'
############################# Appium #############################

job_key = 'C++后端'
# 综合排序/最新优先/匹配度优先
order_require = '匹配度优先'


more_img_path = 'more.png'
search_bar_bias = [-50,-50]
resolution = [5,1256]
