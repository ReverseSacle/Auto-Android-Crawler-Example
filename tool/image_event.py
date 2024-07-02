from tool.adb_event import screenshot

import cv2

def element_match(img_path,y_bias=0):
    screenshot()
    current_image = cv2.imread('./screenshot.png')
    target_image = cv2.imread(img_path)
    target_img_h, target_img_w = target_image.shape[0], target_image.shape[1]

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

    if max_val < 0.7: return [-1,-1,max_val]

    if 0 == y_bias: y_bias = max_loc[1] + target_img_h / 2
    else: y_bias += max_loc[1] + target_img_h
    return [max_loc[0] + target_img_w / 2, y_bias,max_val]

def element_check(img_path):
    return False if element_match(img_path)[2] < 0.7 else True