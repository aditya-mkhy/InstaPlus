import pyautogui
import webbrowser as web
import pathlib
import pyautogui
import time
import random
from PIL import Image
from humancursor import SystemCursor
import images
from datetime import datetime

cursor = SystemCursor()

def log(*args):
    print(f" INFO [{datetime.now().strftime('%d-%m-%Y  %H:%M:%S')}] ", end="")
    for arg in args:
        print(arg, end=" ")
    print("")

def locate(*args, **kwargs):
    try:
        location = pyautogui.locateCenterOnScreen(*args, **kwargs)
        return location
    except:
        return None
        
def click_on(click_duration):
    #click
    pyautogui.mouseDown()
    time.sleep(click_duration)
    pyautogui.mouseUp()
    time.sleep(random.uniform(0.170, 0.280))


def positioned_like_button(loc_y, height):
    
    min_height = height - 250
    max_height = height - 190

    on_height = random.randrange(min_height, max_height, 5)

    scroll_unit = on_height - loc_y
    # print(f"Scroll => {scroll_unit} and on_height={on_height}  and y={loc_y}")

    while  scroll_unit > 0:
        if scroll_unit < 40:
            new_unit = scroll_unit
        
        else:
            new_unit = random.randrange(20, scroll_unit, 5)

        scroll_unit -= new_unit

        pyautogui.scroll(int(new_unit))
        time.sleep(random.uniform(0.1, 0.4))


def mute_un_mute(location, check = False):
    if location:
        if not check:
            cursor.move_to([location[0], location[1]])
            time.sleep(random.uniform(0.1, 0.6))
            click_on(click_duration=random.uniform(0.1, 0.3))
        return True
    
    return False

def mute(check = False):
    location = locate(images.home.mute, confidence= 0.75)
    return mute_un_mute(location, check)


def un_mute(check = False):
    location = locate(images.home.un_mute, confidence= 0.75)
    return mute_un_mute(location, check)

def is_mute():
    # mute, if un_mute button found
    if un_mute(check=True):
        return True
    
    # un_mute, if mute button found
    if mute(check=True):
        return False # means un_mute
    
    #button not found
    return None

def decision():
    return random.choice([True, False])


def content_type(x, y):
    x2 = x + 15
    y2 = y + 15

    region = (int(x), int(y), int(x2), int(y2))
    img = pyautogui.screenshot(region = region)
    time.sleep(1)
    img2 = pyautogui.screenshot(region = region)

    difference = 0
    for pixel_a, pixel_b in zip(img.getdata(), img2.getdata()):
        if pixel_a != pixel_b:
            difference += 1

    if difference > 10:
        return True
    return False

def next_feed(scroll_unit):
    while  scroll_unit > 0:
        if scroll_unit < 100:
            new_unit = scroll_unit
        
        else:
            new_unit = random.randrange(100, scroll_unit, 20)

        scroll_unit -= new_unit
        # print(f"New==> {-abs(new_unit)}")
        pyautogui.scroll(int(-abs(new_unit)))
        sleep_second = f"0.{random.randrange(1,9)}"
        time.sleep(float(sleep_second))


def convert_time(sec: int):
    if sec < 60:
        return f"{sec} Sec"
    elif sec < 3600:
        return f"{sec//60}:{ str(sec%60)[:2]} Mint"
    elif sec < 216000:
        return f"{sec//3600}:{ str(sec%3600)[:2]} Hrs"
    elif sec < 12960000:
        return f"{sec//216000}:{ str(sec%216000)[:2]} Days"
    else:
        return "Error"

if __name__ == "__main__":
    # un_mute()
    log("Heyk",435, "jdfke", log)

