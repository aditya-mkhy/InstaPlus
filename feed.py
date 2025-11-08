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
from carousel import close_carousel,  like_comments, make_comment
from db import DB

def home_window():
    #chek if reels winow is already opend
    location = locate(images.home.on_home_btn, confidence= 0.85)
    if location:
        log("Home window is already open..")
        return True
    
    location = locate(images.home.home_btn, confidence= 0.85)
    if not location:
        raise ValueError("Home Icon not found....")
    
    click_btn(location, 1, 8, 1, 10)
    sleep_uniform(0.8, 1.5)
    move_to(location, 350, 550, 80, 160, x_opr="+", y_opr="+")
    return True

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

    
def like_feed(amount = 5, do_comments = True, do_like_comments = False, randomize = True,  save_post = False, db: DB = None):
    liked = 0
    total_comment = 0
    comment_liked = 0
    #open feed window
    home_window()

    while True:
        scroll = random.randrange(140,260, 10)
        pyautogui.scroll(-abs(scroll))
        sleep_uniform(0.2, 0.8)

        like_btn = locate(images.home.like, region=(200, 0, WIDTH, HEIGHT), confidence= 0.85)
        if not like_btn:
            log("----> Like button is not found....")
            continue

        is_video = content_type(like_btn[0]+ 200, like_btn[1] - 200)
        
        if decision(most=True):#like or not
            positioned_like_button(like_btn[1], HEIGHT)
            if is_video:
                log(f"-----> This is a video....")
                watch_time = random.randrange(4, 20, 1)
                if is_mute():
                    log("-----> Video is muted")
                    un_mute()
                    log("-----> Now it is un_muted")

            else:
                log(f"-----> This is a photo")
                watch_time = random.randrange(2, 10, 1)
                
            log(f"Watching post for {convert_time(watch_time)}")
            sleep(watch_time)
            like_btn = locate(images.home.like, region=(200, 0, WIDTH, HEIGHT), confidence= 0.85)
            if not like_btn:
                log("Error-----> like_btn not found", like_btn)
                continue


            comment_btn = locate(images.home.comment, region=(200, 0, WIDTH, HEIGHT), confidence= 0.85)
            if not comment_btn:
                log("Comment button not found....")

     
            # like post
            click_btn(like_btn, 2, 10, 2, 10)
            sleep_uniform(0.3, 0.8)

            if comment_btn and  ((do_comments and decision()) or (do_comments and not randomize)):
                click_btn(comment_btn, 1, 10, 1, 10)
                sleep_uniform(0.8, 2)
                feed_comment(do_like_comments=do_like_comments, randomize=randomize, db=db)

            liked += 1
            db.add_like()
            log(f"Post liked [{liked}/{amount}]")
            move_to(like_btn, 80, 300, 150, 300, x_opr="+", y_opr="-")

        else:
            log("Feed skipped randomly..")
            if decision(): # viewing the post 
                positioned_like_button(like_btn[1], HEIGHT)

                if is_video:
                    watch_time = random.randrange(1, 10, 1)
                else:
                    watch_time = random.randrange(1, 3, 1  )

                log(f"Watching post for {convert_time(watch_time)} (not liking)")
                sleep(watch_time)


            next_feed(like_btn[1]) # scrolling to next feed
            sleep(1)

        if liked >= amount:
            break

    return {"liked": liked, "comment" : total_comment, "comment_liked": comment_liked}



def feed_comment(do_like_comments = True, randomize = True,  save_post = False, db: DB = None):
    comments_liked = 0
    text_comments_obj = None
    commented = []


    like_btn = locate(images.home.like, region=(200, 0, WIDTH - 200, HEIGHT), confidence= 0.85)

    if  like_btn:
        # move to like button
        move_to(like_btn, 0, 6, 0, 6)
        like_btn2 = locate(images.home.like, region=(200, 0, WIDTH - 200, HEIGHT), confidence= 0.85)

        if not like_btn2:
            log("Some Popup cover the like button")
            # moving cursor on post
            move_to(like_btn, 140, 180, 10, 15, x_opr = "-", y_opr = "-")
            sleep_uniform(0.8, 1.5)

            like_btn2 = locate(images.home.like, region=(200, 0, WIDTH - 200, HEIGHT), confidence= 0.85)
            if not like_btn2:
                raise ValueError("Still not find the like Button")
            
            move_to_unhumaize(like_btn2, 0, 6, 0, 6)


        sleep_uniform(0.1, 0.4)
        pyautogui.click()
        db.add_like()
        log(f"Post liked")

    else:
        liked_btn = locate(images.home.liked, region=(200, 0, WIDTH - 200, HEIGHT), confidence= 0.85)
        if liked_btn:
            log("Post is already Liked...")
            like_btn = liked_btn
            db.add_already_liked()

        else:
            log("-------> Like button not found...")
            return
        
        sleep_uniform(0.1, 0.4)

    # like comment or not
    is_like_comment =  (decision() and do_like_comments) or (not randomize and do_like_comments)
    commnet_like_amout = random.randint(2, 5)

    #Like ccommets
    commented_emoji = like_comments(like_btn, amount=commnet_like_amout, do_like=is_like_comment, db=db)
    log(f"Comments liked -> {comments_liked} ")
    if commented_emoji == {}:
        log("No emoji is found in comments..")
        commented = []

    else:
        log("Try to comment on post")
        commented, is_comment_box_focus = make_comment(commented_emoji, text_comments_obj)
        if commented:
            db.add_comment()
            log(f"Commented : {' '.join(commented)}")

    close_carousel()



if __name__ == "__main__":
    sleep(2)
    info = like_feed(20, do_comments=True, do_like_comments=True, randomize=False)
    print(f"Info ==> {info}")