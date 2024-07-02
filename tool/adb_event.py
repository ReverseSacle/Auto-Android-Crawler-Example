import os
from config import adb, resolution

def open_app(appPackage,boss_appActivity):
    os.system(f"{adb} shell am start -n {appPackage}/{boss_appActivity}")
    print(f"start app event => start {appPackage}")

def stop_app(appPackage):
    os.system(f"{adb} shell am force-stop {appPackage}")
    print(f"stop app event => stop app {appPackage}")

def tap(x,y):
    os.system(f"{adb} shell input tap {x} {y}")
    print(f"click event => tap ({x},{y})")

def tap_element(location):
    x = location['x'] + location['width'] / 2
    y = location['y'] + location['height'] / 2
    os.system(f"{adb} shell input tap {x} {y}")
    print(f"click event => tap ({x},{y})")

# 沿着边缘滑动，防止误触
def edge_scroll(y,slow_down=False,duration=500):
    # 向上滑动y为负数，向下滑动y为正数，即模拟手指上滑为负，手指下滑为正
    x1 = resolution[0]
    y1 = resolution[1]
    if slow_down: y += y1
    os.system(f"{adb} shell input swipe {x1} {y1} {x1} {y} {duration}")
    print(f"center scroll event => scroll to {x1} {y1+y}")

def horizon_swipe(switcher=False,duration=200):
    x_bias = -500
    if switcher: x_bias = 500
    x1 = resolution[0] / 2
    y1 = resolution[1] / 2
    os.system(f"{adb} shell input swipe {x1} {y1} {x1 + x_bias} {y1} {duration}")

def screenshot():
    os.system(f'{adb} exec-out screencap -p > ./screenshot.png')
    print(f"screenshot event => ./screenshot.png")
