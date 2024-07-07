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
from time import sleep
import os

cursor = SystemCursor()
from pathlib import Path


WIDTH, HEIGHT =  pyautogui.size()
LOG_PATH = f"{Path.home().as_posix()}/Desktop/log.txt"
if not os.path.exists(LOG_PATH):
    LOG_PATH = None


def log(*args, **kwargs):
    print(f" INFO [{datetime.now().strftime('%d-%m-%Y  %H:%M:%S')}] ", *args, **kwargs)
    if LOG_PATH:
        try:
            with open(LOG_PATH, "a") as tf:
                tf.write(f" INFO [{datetime.now().strftime('%d-%m-%Y  %H:%M:%S')}] { ' '.join(args)}\n")
        except Exception as e:
            print(f"Error[log] ---> {e}")
        


def decision(most = None):
    if most == True:
        return random.choice([True, True, False, True, True, False, True, True, False, True])
    
    if most == False:
        return random.choice([False, False, True, False, False, True, False, False, True, False])

    return random.choice([True, False])

def sleep_uniform(x, y):
    sleep(random.uniform(x, y))

def randomize_point(loc, x_start = 0, x_end = 0, y_start = 0, y_end = 0, x_opr= None, y_opr = None) -> tuple:
    if not x_opr:
        if decision(): x_opr = "+"
        else: x_opr = "-"

    if not y_opr:
        if decision(): y_opr = "+"
        else: y_opr = "-"

    x = eval(f"{loc[0]} {x_opr} {random.randint(x_start, x_end)}")
    y = eval(f"{loc[1]} {y_opr} {random.randint(y_start, y_end)}")

    return (x, y)
    


def move_to_unhumaize(loc, x_start = 0, x_end = 0, y_start = 0, y_end = 0, x_opr = None, y_opr = None, duration = 1.5):
    point = randomize_point(loc, x_start, x_end, y_start, y_end, x_opr, y_opr)
    pyautogui.moveTo(point[0], point[1], duration=duration)
    return point

def move_to(loc, x_start=0, x_end=2, y_start=0, y_end=1, x_opr = None, y_opr = None):
    point = randomize_point(loc, x_start, x_end, y_start, y_end, x_opr, y_opr)
    cursor.move_to(point)
    return point

def click_btn(loc, x_start = 0, x_end = 2, y_start = 0, y_end = 1, x_opr = None, y_opr = None):
    point = move_to(loc, x_start, x_end, y_start, y_end, x_opr, y_opr)
    sleep_uniform(0.1, 0.7)
    pyautogui.click()
    return point



def locate(*args, **kwargs):
    try:
        location = pyautogui.locateCenterOnScreen(*args, **kwargs)
        return location
    except:
        return None
    
def locate_until(*args, timeout = 1, **kwargs):
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            return 
        
        location = locate(*args, **kwargs)
        if location:
            return location
        
        time.sleep(0.5)

def locate_multi(images: list = None,  timeout = 1, **kwargs):
    start_time = time.time()
    if images == None:
        return

    while True:
        if time.time() - start_time > timeout:
            return 
        
        for image in images:
            location = locate(image, **kwargs)
            if location:
                return [location, images.index(image)]
            time.sleep(0.001)
        
        time.sleep(0.5)

        
def click_on(click_duration):
    #click
    pyautogui.mouseDown()
    time.sleep(click_duration)
    pyautogui.mouseUp()
    time.sleep(random.uniform(0.170, 0.280))





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
    
def update_info(info, data):
    for key in data:
        if key in info:
            info[key] = info[key] + data[key]
        else:
            info[key] = data[key]
    
    return info



if __name__ == "__main__":
    info = {"like": 0, "c": 0}

    data = {"like": 5, "c": 2}
    print(f"info-> {info}")
    update_info(info, data)
    print(f"info_adter-> {info}")

    data =  {"like": 10, "dis": 2}
    update_info(info, data)
    print(f"info_end-> {info}")
  