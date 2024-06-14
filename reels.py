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


Friends_List = [ "Lakshay Saini", "ik"]
def reels_window():
    on_reels_btn = locate(images.reels.on_reels_btn, confidence= 0.8)
    if not on_reels_btn:
        # reel button
        reels_btn = locate(images.reels.reels_btn, confidence= 0.8)
        if not reels_btn:
            raise ValueError("Reels Icon not found....")
        click_btn(reels_btn, 1, 8, 1, 8)

    else:
        log("Reels window is already open....")

    like_btn, index = locate_multi(images=[images.reels.like, images.reels.liked], region=(200, 0, WIDTH, HEIGHT), confidence= 0.9, timeout=15)
    print(like_btn, index)
    if not like_btn:
        return False
    
    sleep_uniform(0.8, 1.2)
    click_btn(like_btn, 50, 100, 10, 150, x_opr="+")

    return True


def like_by_reel(amount = 5, do_comments = True, do_like_comments = False, do_share = False, randomize = True,  save_post = False):
    liked = 0
    already_liked = 0
    total_comment = 0
    comment_liked = 0
    reels_window()
    sleep_uniform(1.5, 3)

    while liked < amount:
        #scroll reel
        scroll = random.randrange(60, 200, 20)
        pyautogui.scroll(-abs(scroll))
        sleep_uniform(1, 3)

        like_btn = locate(images.reels.like, region=(200, 0, WIDTH - 200, WIDTH),  confidence= 0.85)
        if not like_btn:

            liked_btn = locate(images.reels.liked, region=(200, 0, WIDTH - 200, WIDTH),  confidence= 0.85)
            if not liked_btn:
                log("Somethis is not right, please check... Like button not found..")
            else:
                log("Reel is already visited....")
                already_liked += 1
            #next reel
            continue

        if decision(most=True): # like or not
            #watching the reel
            watch_time = random.randrange(10, 26, 1)
            log(f"Watching reel for {convert_time(watch_time)}")
            sleep(watch_time)

            # random location on like button
            click_btn(like_btn, 1, 6, 1, 6)
            liked += 1
            log(f"Reel liked [{liked}/{amount}]")

            if (decision(most=True) and do_comments)  or (not randomize and do_comments):# comments or not 
                commnet_like_amout = random.randint(1, 2)
                is_like_comment =  (decision(most=False) and do_like_comments) or (not randomize and do_like_comments)


                no_comment_liked, commented_emoji = like_comments(amount=commnet_like_amout, do_comments = True, do_like=is_like_comment)
                comment_liked += no_comment_liked

                log(f"Total comment liked -> {no_comment_liked} ")

                if commented_emoji == {}:
                    log("No emoji is found in comments..")
                    is_closed = False
                else:
                    log("Try to comment on post")
                    commented, is_closed = make_comment(commented_emoji)
                    total_comment += 1
                    log(f"Commented : {' '.join(commented)}")

                # close the ccomment popup
                if not is_closed:
                    close_btn = locate(images.reels.comment_close_btn, region=(200, 100, WIDTH - 200, HEIGHT - 100),  confidence= 0.93)
                
                    if decision() and close_btn:
                        click_btn(close_btn, 1, 6, 1, 6)

                    else:
                        liked_btn = locate(images.reels.liked, region=(200, 0, WIDTH - 200, WIDTH),  confidence= 0.85)
                        if liked_btn:
                            log("just aoue the like utoon")
                            click_btn(liked_btn, 1, 4, 30, 50, y_opr="-")
                            log("Pop closed")

                        else:
                            log("LIke button not found...")
                            move_to(like_btn, 40, 200, 20, 250, x_opr="+")
                else:
                    move_to(like_btn, 40, 200, 20, 250, x_opr="+")

            else:
                if decision():
                    move_to(like_btn, 40, 200, 20, 150)         



            if decision(most=True) and do_share:
                name = random.choice(Friends_List)
                st = send_reel(name=name)
                if st:
                    log(f"Reel sendt to  --> {name}")

            # move cursor from like button
            # move_to(like_btn, 40, 200, 20, 250, x_opr="+")
            sleep(random.uniform(0.5, 1.2))


        else:
            log("Reel skipped randomly..")
            if decision():
                watch_time = random.randrange(8, 20, 2)
            else:
                watch_time = random.uniform(2, 5)

                # if decision(): #pause the reel
                #     if is_cursor_on_reel: # pause by left click
                #         pyautogui.click()
                #         # print(f"Pause by click")
                #     else:
                #         # print(f"Pause by pause button")
                #         pyautogui.press('playpause')

            log(f"Watching reel for {convert_time(watch_time)} (Not liking)")
            sleep(watch_time)

    return {"liked" : liked, "already_liked" : already_liked, "total_comment" : total_comment, "comment_liked": comment_liked}



def like_comments(amount = 5, do_comments = True, do_like = True):
    liked = 0
    ignore_y = 0 
    is_crolled = True
    commented_emoji = {}

    not_found_after = 0
    comments_not_found = 0

    comment_btn = locate(images.reels.comment_btn, region=(200, 0, WIDTH - 200, HEIGHT),  confidence= 0.85)
    if not comment_btn:
        log("Comment button not found...")
    click_btn(comment_btn, 1, 6, 1, 6)

    #comment label pos
    comment_label = locate_until(images.reels.comment_label, region=(200, 0, WIDTH - 200, HEIGHT),  confidence= 0.85, timeout=8)
    if not comment_label:
        raise ValueError("Comment window didn't open due to some error")
    
    close_btn = locate(images.reels.comment_close_btn, region=(200, 0, WIDTH, HEIGHT),  confidence= 0.93)
    if not close_btn:
        log("Close button not found....")
        close_btn = (300, 400)
    else:
        close_btn = (int(close_btn[0]), int(close_btn[1]))

    
    ignore_y = int(comment_label[1])
    sleep_uniform(0.2, 0.4)
    move_to(comment_label, 100, 170, 70, 170, y_opr="+", x_opr="+")

    sleep_uniform(0.2, 0.4)

    while liked <  amount:

        region = (int(comment_label[0]), ignore_y, WIDTH - int(comment_label[0]), HEIGHT - ignore_y)

        cmnt_like_btn = locate(images.reels.comment_like, region = region, confidence= 0.9)


        if not cmnt_like_btn:# if not found
            
            if not_found_after > 6:
                log("No more comments exits...")
                #if cmnt_like_btn not found after eight time scrolling, then  break
                break

            not_found_after += 1
            log(f"--> Scrolling")
            units = random.randrange(80, 200)

            ignore_y -= units
            if ignore_y < comment_label[1]:
                ignore_y = comment_label[1]

            pyautogui.scroll(-(units))
            sleep_uniform(0.7, 0.9)
            is_crolled = True # to read new comments
            continue

        #  not_found_after
        not_found_after = 0

        # find comments...
        if is_crolled and do_comments:
            found_commented_emoji = read_comments(close_btn, emoji = images.get_read_emoji(commented_emoji.items()))
            commented_emoji.update(found_commented_emoji)
            is_crolled = False # to stop for searching emoji until scroll


            if not do_like:
                # break while loop if ccomments noot found after 6 times scrolling
                if len(found_commented_emoji) == 0:
                    comments_not_found += 1

                if len(commented_emoji) > 0 or comments_not_found > 6:
                    #stop comment like
                    break

        if decision() and do_like:
            click_btn(cmnt_like_btn, 0, 3, 0, 3)
            liked += 1
            log(f"Comment liked [{liked}/{amount}]")
            
            sleep(random.uniform(0.2, 0.6))

            if decision(): #move away fro comment_like button
                log("------> moving away from like button")
                move_x = cmnt_like_btn[0] - random.randint(20, 80)

                if (comment_label[1] + 120) < cmnt_like_btn[1]:
                    move_y = comment_label[1] + random.randint(5, 50) + 70
                    
                else:
                    move_y = cmnt_like_btn[1] + random.randint(10, 80)

                cursor.move_to([move_x, move_y])
                sleep_uniform(0.1, 0.5)

        else:
            sleep_uniform(0.4, 0.5)

        ignore_y = cmnt_like_btn[1] + 80

    return (liked, commented_emoji)


def read_comments(close_btn, emoji):
    from_x = close_btn[0]
    from_y = close_btn[1]
    to_x = 500
    to_y = 500

    found = {}

    for img in emoji:
        emoji_loc = locate(emoji[img], confidence= 0.93, region=(from_x, from_y, to_x, to_y))

        if not emoji_loc:
            continue

        if found.get(img):
            found[img] += 1
        else:
            found[img]  = 1

    return found


def emoji_btn_click(comment_emoji, input = False):
    if input:
        move_to(comment_emoji, 120, 121, 0, 1, x_opr = "+", y_opr = "+")
    else:
        move_to(comment_emoji, 1, 8, 1, 8)

    comment_emoji2 = locate(images.carousel.comment_emoji, confidence= 0.8)
    if not comment_emoji2:
        move_to(comment_emoji, 200, 300, 150, 200,  x_opr = "+", y_opr = "-")
        sleep_uniform(0.8, 1.2)

        comment_emoji2 = locate(images.carousel.comment_emoji, confidence= 0.8)
        if not comment_emoji2:
            log("-------> Still not found Comment emoji....")
            return 
        
        if input:
            move_to_unhumaize(comment_emoji2, 120, 121, 0, 1, x_opr = "+", y_opr = "+")
        else:
            move_to_unhumaize(comment_emoji, 1, 10, 1, 10)

    sleep_uniform(0.1, 0.4)
    pyautogui.click()
    return True

def make_comment(commented_emoji: dict):
    emoji_btn = images.EMOJI_BTN.copy()
                 
    no_of_emoji = 2

    comment_emoji = locate(images.carousel.comment_emoji, confidence= 0.8)
    if not comment_emoji:
        log("-------> Comment emoji not found....")
        return ([], False)
    

    st = emoji_btn_click(comment_emoji, input=False)# clicck ccomment input box
    if not st:
        return ([], False)
    sleep(random.uniform(0.4, 1))


    is_emoji_loaded = locate(images.carousel.emoji_most_popular_lbl, confidence= 0.9)
    if not is_emoji_loaded:
        pyautogui.click()

    is_emoji_loaded = locate_until(images.carousel.emoji_most_popular_lbl, confidence= 0.9, timeout = 8)

    if not is_emoji_loaded:
        log("-------> Emoji is not loaded")
        return ([], False)
    
    log("Emoji is loaded")


    commented = []
    emoji_count = 0
    for emoji in commented_emoji:

        if emoji_count == no_of_emoji:
            break

        emoji_loc = locate(emoji_btn[emoji], confidence= 0.92)
        if not emoji_loc:
            log(f"Emoji is not present on the screen : {emoji}")
            continue

        move_to(emoji_loc, 1, 10, 1, 10)
        sleep(random.uniform(0.1, 0.3))

        count = random.randint(2, 4)
        emoji_count += 1

        for i in range(count):
            pyautogui.click()
            sleep(random.uniform(0.1, 0.2))


        sleep(random.uniform(0.5, 1.5))
        commented.append(emoji)

    print("sleeping")


    # entr key
    sleep(random.uniform(0.3, 0.6))
    pyautogui.press('enter') 
    sleep(random.uniform(0.8, 2))

    is_closed = False

    close_btn = locate(images.reels.comment_close_btn, region=(200, 100, WIDTH - 200, HEIGHT - 100),  confidence= 0.93)
    if not close_btn:
        log("Close button not found...")


    if decision() and  close_btn:
        # move away from emoji popup and click to close it
        click_btn(close_btn, 1, 6, 1, 6)
        is_closed = True
        sleep_uniform(0.4, 0.9)

    else:
        # use emoji button to close emoji popup
        click_btn(comment_emoji, 1, 8, 1, 8)
        sleep_uniform(0.2, 0.4)


    return (commented,  is_closed) 
        


def send_reel(name):
    return True

if __name__ == "__main__":
    sleep(2)

    # make_comment(images.EMOJI_BTN)


    # # btn = locate(images.reels.comment_close_btn, region=(200, 0, WIDTH, WIDTH),  confidence= 0.93)
    # # if btn:

    # #     x = btn[0] + 0
    # #     y = btn[1] + 0#70
    # #     cursor.move_to([x, y])

    # # else:
    # #     print("not founfd")
    # # exit()


    # info = like_comments(amount=5, do_comments=True)

    info = like_by_reel(amount=5, do_comments=False, do_like_comments=False, do_share=True, randomize=False)
    print(info)
