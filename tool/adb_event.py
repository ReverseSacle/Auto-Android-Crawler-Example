import os
import cv2
from config import adb

from button_location import resolution

def tap(x,y):
    os.system(f"{adb} shell input tap {x} {y}")
    print(f"click event => tap ({x},{y})")

def open_app(appPackage,boss_appActivity):
    os.system(f"{adb} shell am start -n {appPackage}/{boss_appActivity}")
    print(f"start app event => start {appPackage}")

def stop_app(appPackage):
    os.system(f"{adb} shell am force-stop {appPackage}")
    print(f"stop app event => stop app {appPackage}")

def center_scroll(y,slow_down=False,duration=500):
    # 向上滑动y为负数，向下滑动y为正数，即模拟手指上滑为负，手指下滑为正
    x1 = resolution[0] / 2
    y1 = resolution[1] / 2
    if slow_down: y += y1
    os.system(f"{adb} shell input swipe {x1} {y1} {x1} {y} {duration}")
    print(f"center scroll event => scroll to {x1} {y1+y}")

def press(x,y,duration):
    os.system(f"{adb} shell input swipe {x} {y} {x} {y} {duration}")
    print(f"press event => {x},{y}")

def image_match(img_path):
    os.system(f'{adb} exec-out screencap -p > ./screenshot.png')
    current_image = cv2.imread('./screenshot.png')
    target_image = cv2.imread(img_path)

    target_img_h, target_img_w = target_image.shape[0], target_image.shape[1]

    os.system(f'{adb} exec-out screencap -p > ./screenshot.png')
    current_image = cv2.imread('./screenshot.png')
    target_image = cv2.imread(img_path)

    b_current, g_current, r_current = cv2.split(current_image)
    b_target, g_target, r_target = cv2.split(target_image)

    # 分别进行模板匹配
    res_b = cv2.matchTemplate(b_current, b_target, cv2.TM_CCOEFF_NORMED)
    res_g = cv2.matchTemplate(g_current, g_target, cv2.TM_CCOEFF_NORMED)
    res_r = cv2.matchTemplate(r_current, r_target, cv2.TM_CCOEFF_NORMED)

    # 结合匹配结果（例如取平均）
    res_combined = (res_b + res_g + res_r) / 3

    # 查找最佳匹配位置
    _, max_val, _, max_loc = cv2.minMaxLoc(res_combined)

    if max_val < 0.8: return [-1,-1]

    return [max_loc[0] + target_img_w / 2, max_loc[1] + target_img_h / 2]