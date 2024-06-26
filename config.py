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
adb = 'adb -s 192.168.55.153:5555'
############################# Appium #############################

job_key = 'C++后端'