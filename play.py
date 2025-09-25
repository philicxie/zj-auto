import subprocess
import time
import pyautogui
import logging
import time, pyautogui, cv2, numpy as np, aircv as ac

from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID

logger = logging.getLogger(__name__)

# 获取窗口信息
def get_window_position(app_name):
    options = kCGWindowListOptionOnScreenOnly
    window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for window in window_list:
        name = window.get("kCGWindowOwnerName", "")
        if app_name.lower() in name.lower():
            x = window["kCGWindowBounds"]["X"]
            y = window["kCGWindowBounds"]["Y"]
            return (x, y)
    return None


app_name = "PlayCover"
# 打开 App（例如：Notes）


# init_pos = get_window_position(app_name)
# if init_pos:
#     print(f"窗口左上角坐标：{init_pos}")
# else:
#     print("未找到窗口")
# 
# print(init_pos[0], init_pos[1])
# pyautogui.click(x=init_pos[0]+230, y=init_pos[1]+130, clicks=2, interval=0.2)
#
# time.sleep(2)
#
# game_pos = get_window_position("杖剑传说")
# if game_pos:
#     print(f"<UNK>{game_pos}")

def find_touch(template_path, threshold=0.85, timeout=10, interval=0.5, double=False):
    """模板匹配→点击中心，找到返回True，超时返回False"""
    start = time.time()
    tpl = ac.imread(template_path)
    while True:
        screen = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        match = ac.find_template(screen, tpl, threshold)
        if match:
            x, y = match['result']
            if double:
                pyautogui.click(x=x//2, y=y//2, clicks=2, interval=0.15)
            else:
                pyautogui.click(x=x//2, y=y//2)
            return True
        if time.time() - start > timeout:
            return False
        time.sleep(interval)

def wait_for(template_path, timeout=10, interval=0.5):
    start = time.time()
    while time.time() - start < timeout:
        loc = pyautogui.locateCenterOnScreen(template_path, confidence=0.8)
        if loc is not None:
            return loc  # 立即返回 (x, y)
        time.sleep(interval)
    return None

def open_game():
    subprocess.run(["open", "-a", app_name + ".app"])
    time.sleep(1)
    find_touch('assets/zj_icon.png', double=True)

def enter_main():
    logger.info("Try enter main")
    if wait_for('assets/gonggao.png', timeout=30):
        logger.info("Enter main successfully")
    else:
        logger.error("Enter main failed")


if '__main__' == __name__:
    logging.basicConfig(level=logging.INFO)
    open_game()
    enter_main()

