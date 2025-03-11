import webbrowser as web
import os
import pathlib
import pyautogui
import random
from PIL import Image
from humancursor import SystemCursor #pip install HumanCursor
import images
from util import *
from text_comments import TextComments



def reload_page(img):
    reload_button = locate(images.home.reload, confidence= 0.9)
    if not reload_button or decision(most=False):
        pyautogui.press('f5')
        sleep_uniform(0.8, 1.5)

    else:
        click_btn(reload_button, 1, 3, 1, 3)
        close_btn = locate_until(images.home.reload_close, confidence= 0.92, timeout=6)
        if not close_btn:
            log("reload close button not found ")
            sleep_uniform(6, 10)
        else:
            log("Close button found...........")

    reload_button = locate_until(images.home.reload, confidence= 0.9, timeout=10)
    confirm_img = locate(img, confidence= 0.95) 

    if not reload_button and not confirm_img:
        log("Reload button not found...")
        sleep_uniform(14, 20)

    confirm_img = locate_until(img, confidence= 0.95, timeout= 20) 
    if not confirm_img:
        raise ValueError("Error : Error in reloading the page.. ")
    sleep_uniform(0.8, 1.5)
    return True


def open_explore():
    #chek if explore window is already opend
    #to verify that carousal is opend
    save_btn = locate_until(images.carousel.save_btn, confidence= 0.93, timeout= 10)
    if save_btn:
        log("Explore is already opend...")
        return True
    
    on_explore = locate(images.explore.on_explore_btn, confidence= 0.9)
    if not on_explore:
        #find explore utton
        explore_btn = locate(images.explore.explore_btn, confidence= 0.85)
        if not explore_btn:
            return False
        
        click_btn(explore_btn, 1, 8, 1, 8)
        sleep_uniform(3, 6)

    else:
        #if carousel is opend
        save_btn = locate_until(images.carousel.save_btn, confidence= 0.93, timeout= 2)
        if save_btn:
            return True
        
        # #close crousel
        # click_btn(on_explore, 1, 8, 1, 8)

        sleep_uniform(0.5, 2)
        explore_btn = on_explore
    

    click_btn(explore_btn, 550, 700, 150, 300, x_opr = "+", y_opr = "+")
    sleep_uniform(0.5, 1)

    #to verify that carousal is opend
    save_btn = locate_until(images.carousel.save_btn, confidence= 0.93, timeout= 10)
    if not save_btn:
        log("Save button not found. So, can't verify that it is a carousel.")
        return False
    
    return True


def search(query):
    search_btn = locate(images.search.search_btn, confidence= 0.93)
    if not search_btn:
        log("Search button not found..")
        search_on_btn = locate(images.search.search_on_btn, confidence= 0.93)
        if not search_on_btn:
            raise ValueError("Search button not found..")
        
        log("Already on search icon")
        close_btn = locate(images.search.close_btn, confidence= 0.95)
        if not close_btn:
            raise ValueError(f"Close button is also not found...")

        click_btn(close_btn, 100, 200, 1, 8, x_opr="-", y_opr="+")

        sleep_uniform(0.2, 0.6)
        search_btn = search_on_btn

    else:
        #click on search icon
        click_btn(search_btn, 1, 5, 1, 5)
        sleep_uniform(0.2, 0.5)

        #to check 
        close_btn = locate_until(images.search.close_btn, confidence= 0.95, timeout=8)
        print("clise btn found")
        if not close_btn:
            raise ValueError(f"Close button is also not found...")
        
        # move cursor to input box
        move_to(close_btn, 100, 200, 1, 8, x_opr="-", y_opr="+")
        sleep_uniform(0.3, 0.7)

        if decision(): # click or not
            pyautogui.click()
            sleep_uniform(0.3, 0.8)


    recent_label = locate_until(images.search.recent_label, confidence= 0.95, timeout=3)
    if not recent_label:
        raise ValueError("Recent label not found...")

    pyautogui.write(query, interval=random.uniform(0.100, 0.200))
    print("query written")

    close_btn = locate_until(images.search.close_btn, confidence= 0.95, timeout=5)
    if not close_btn:
        raise ValueError("Close button not found in search bar, may be it still searching..")

    sleep_uniform(0.3, 0.7)

    #  click on 1st result
    x = recent_label[0] + random.randint(30, 200)
    if decision():
        y = recent_label[1] - random.randint(1, 40)
    else:
        y = recent_label[1] + random.randint(1, 10)

    cursor.move_to((x, y))
    sleep_uniform(0.1, 0.5)
    pyautogui.click()

    print("Clicck on the 1st search...")

    return  True


def search_hashtag(query, refresh = False):
    #search
    search(query=query)

    refresh_btn = locate_until(images.home.reload_error, confidence= 0.95, timeout= 10)
    if refresh_btn:
        print("Refreshing the page................")
        click_btn(refresh_btn, 1, 10, 1, 10)
        sleep(10)


    close_btn = locate_until(images.search.close_btn, confidence= 0.9, timeout=5)
    if  close_btn:
        print("Close Button Found...This means searh window is still there...")
        search_on_btn = locate(images.search.search_on_btn, confidence= 0.8)
        if not search_on_btn:
            raise ValueError("Searh btn not found....")
        click_btn(search_on_btn, 1, 5, 1, 5)
        sleep_uniform(2, 3)


    top_post = locate_until(images.search.hash_tag, confidence= 0.8, timeout= 20)
    if not top_post:
        raise ValueError("TopMost hashtag is not found....")

    
    # #referesh
    # if refresh:
    #     st = reload_page(images.search.hash_tag)
    #     if st:
    #         log("Page refreshed sucessfullly...")
    #     sleep_uniform(0.5, 1)

    #click on 1st item to open carsousel

    print(top_post)
    click_btn(top_post, 50, 250, 100, 300, x_opr="+", y_opr="+")

    save_btn = locate_until(images.carousel.save_btn, confidence= 0.93, timeout= 10)

    if not save_btn:
        raise ValueError("Save button not found.So, can't verify that it is a carousel.")
    

def scroll(units):
    while units:
        
        if units < 100:
            one_unit = units
            units = 0
        else:
            one_unit = random.randint(100, units)
            units -= one_unit
            
        log(f"scrool ==> {one_unit}")
        pyautogui.scroll(int( -one_unit ))
        sleep_uniform(0.2, 0.6)

    

def search_user(query):
    search(query=query)

    posts_label = locate_until(images.search.posts_label, confidence= 0.85, timeout= 8)
    if not posts_label:
        search_on_btn = locate(images.search.search_on_btn, confidence= 0.93)
        if not search_on_btn:
            raise ValueError("POSTS label not found....")
        
        click_btn(search_on_btn, 1, 5, 1, 5)
        sleep_uniform(0.5, 1)

        posts_label = locate(images.search.posts_label, confidence= 0.85)
        if not posts_label:
            raise ValueError("TOP POST label not found....")
        
    # check if "no post yet"
    no_post_label = locate(images.search.no_post_yet_label, confidence= 0.85)
    if no_post_label:
        return "no_post"

    #srcoll the post 

    if posts_label[1] > 500:
        sleep_uniform(1.5, 3)
        need_y = random.randint(300, 450)
        scroll_unit = posts_label[1] - need_y
        scroll(scroll_unit)

    posts_label = locate(images.search.posts_label, confidence= 0.85)
    if not posts_label:
        raise ValueError("Scrolling hides the POSsT label")
    
    #click on 1st item to open carsousel
    if decision(): # 1st post
        click_btn(posts_label, 150, 250, 100, 300, x_opr="-", y_opr="+")
    else:
        click_btn(posts_label, 150, 250, 100, 300, x_opr="+", y_opr="+")

    comment_emoji = locate_until(images.carousel.comment_emoji, confidence= 0.85, timeout=5)
    if comment_emoji:
        return True
    
    return False

def shuffle(lst:  list):
    new_lst = []
    
    while lst:
        elmt = random.choice(lst)

        if decision(most=True):
            new_lst.append(elmt)

        lst.remove(elmt)
    
    return new_lst



        


if __name__ == "__main__":

    l = [1,2,3,4,5]
    s = shuffle(l)
    print(s)
    exit()


    sleep(2)

    refresh_btn = locate_until(images.carousel.save_btn, confidence= 0.93, timeout= 10)
    move_to(refresh_btn, 1, 10, 1, 10)


    # comment_emoji = locate(images.home.reload_error, confidence= 0.85)
    # print(comment_emoji)

    # move_to(comment_emoji, 1, 10, 1, 10)
    
