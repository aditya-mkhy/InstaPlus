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

def close_carousel():
    btn = locate(images.carousel.close_btn, confidence= 0.85)
    if not btn:
        log(f"-----> Close button not found...")
        return False
    click_btn(btn, 1, 10, 1, 10)
    log("-----> Carousel closed..")
    return True



def carousel(amount = 5, do_comments = True, do_like_comments = True, randomize = True,  save_post = False):
    liked = 0
    already_liked = 0
    total_comment = 0
    comment_liked = 0
    is_comment_box_focus = False
    text_comments_obj = TextComments()
    already_liked_continuity = 0

    while True:

        like_btn = locate(images.home.like, region=(200, 0, WIDTH - 200, HEIGHT))

        if  like_btn:
           
            x = like_btn[0] - 200
            y = like_btn[1] - 200
            sleep_uniform(0.5, 0.9)
            is_video = content_type(x, y)# if the post is photo or video
            already_liked_continuity = 0

            if decision(most=True) or not randomize:#like or not
                if is_video:
                    log(f"------> This is a video....")
                    watch_time = random.randrange(8, 20, 1)
                    if is_mute():
                        log(f"------> Video is muted")
                        s = un_mute()
                        log(f"------> Now, it is unmute")

                else:
                    log(f"------> This is a photo")
                    watch_time = random.randrange(2, 8, 1)
                    
                log(f"Watching post for {convert_time(watch_time)}")
                sleep(watch_time)

                #like the post

                move_to(like_btn, 0, 6, 0, 6)
                like_btn2 = locate(images.home.like, region=(200, 0, WIDTH - 200, HEIGHT))
                if not like_btn2:
                    log("Some Popup cover the like button")

                    # moving cursor on post
                    move_to(like_btn, 140, 180, 10, 15, x_opr = "-", y_opr = "-")
                    sleep_uniform(0.8, 1.5)

                    like_btn2 = locate(images.home.like, region=(200, 0, WIDTH - 200, HEIGHT))
                    if not like_btn2:
                        next_btn = locate(images.carousel.next, confidence= 0.8)
                        if not next_btn:
                            #error
                            log("Still not find Like or Next button, maybe this one is last.")
                            break

                        click_btn(next_btn, 1, 4, 1, 4)
                        sleep_uniform(1, 2)
                        continue
                    
                    move_to_unhumaize(like_btn2, 0, 6, 0, 6)


                sleep_uniform(0.1, 0.4)
                pyautogui.click()


                liked += 1
                log(f"Post liked [{liked}/{amount}]")

                # like comment or not
                is_like_comment = (decision(most=False) and do_like_comments) or (not randomize and do_like_comments)

                if (decision(most=True) and do_comments)  or (not randomize and do_comments):# comments or not 
                    log("Trying to comment...")
                    commnet_like_amout = random.randint(1, 2)

                    no_comment_liked, commented_emoji = like_comments(like_btn, amount=commnet_like_amout, do_like=is_like_comment)
                    comment_liked += no_comment_liked

                    log(f"Total comment liked -> {no_comment_liked} ")

                    if commented_emoji == {}:
                        log("No emoji is found in comments..")
                    else:
                        log("Try to comment on post")
                        commented, is_comment_box_focus = make_comment(commented_emoji, text_comments_obj)
                        total_comment += 1
                        log(f"Commented : {' '.join(commented)}")

                else:
                    log("Skipping commnets")
                    is_comment_box_focus = False

            
            else:
                if is_video:
                    log(f"------> This is a video....")
                    watch_time = random.randrange(3, 12, 1)
                    if watch_time > 8:
                        if decision():
                            s = mute()
                            if s:
                                log(f"------> Video muted")
                
                else:
                    log(f"------> This is a photo")
                    watch_time = random.randrange(2, 5, 1)

                log(f"Watching post for {convert_time(watch_time)} (not liking)")
                sleep(watch_time)

        else:
            liked_btn = locate(images.home.liked, region=(200, 0, WIDTH - 200, HEIGHT))
            if liked_btn:
                log("Post is already visited...")
                already_liked += 1
                already_liked_continuity += 1

                if already_liked_continuity > 10:
                    log("All the post in this carousel is already visited....")
                    close_carousel()
                    break

            else:
                log("Like button not found...")
                already_liked_continuity = 0
            sleep_uniform(0.1, 0.4)

        if liked >= amount:
            close_carousel()
            break

        # next post.........
        next_btn = locate(images.carousel.next, confidence= 0.8)
        if not next_btn:

            # check if the comment emoji is find, wich means this is slider post
            emoji_btn = locate(images.carousel.comment_emoji, confidence= 0.85)
            if not emoji_btn:
                save_btn = locate(images.carousel.save_btn, confidence= 0.92)
                if not save_btn:
                    #Error 
                    log("This is not a carousel that's why closing the task..")
                    break
            
            # to know if this this the last post
            prev_btn = locate(images.carousel.prev, confidence= 0.85)
            if prev_btn:
                move_to(emoji_btn)# beacuse some time while likeing comments tooltip appers on next button

                next_btn = locate(images.carousel.next, confidence= 0.8) #10 both
                if not next_btn:
                    log("All post are liked or visited...")
                    close_carousel()
                    break
            
            # next button not found but posts are available
            sleep_uniform(0.6, 1.5)
            pyautogui.press("right")
            sleep_uniform(0.6, 1.5)
            log("-----> Right key is pressed as next button not found...")
        
        else:
            
            if decision(most=False) and (not is_comment_box_focus):# press right key to get next post
                #if is_comment_box_focus in focus, there is no effect of pressing right key
                log("------> Right key is pressed...")
                pyautogui.press("right")
                sleep(random.uniform(0.6, 1.5))

            else:
                click_btn(next_btn, 1, 10, 1, 10) # next post
                sleep(random.uniform(0.6, 1.5))

    return {"liked" : liked, "already_liked" : already_liked,  "comment_liked" : comment_liked, "comment" : total_comment}


def like_comments(like_btn, amount = 5, do_like = True):
    liked = 0
    ignore_y = 0 # to ingnore skipped like
    not_found_after = 0
    comments_not_found = 0
    commented_emoji = {}
    is_crolled = True

    log(f"Comments to be liked : {amount}")
    sleep_uniform(0.5, 1)

    #move cursor to comments area
    x = like_btn[0] +  random.randint(200, 280)
    y = like_btn[1] - random.randint(100, 200)
    cursor.move_to([x, y]) 
    sleep(random.uniform(0.3, 1))

    while liked <  amount:
        region = (like_btn[0], ignore_y, WIDTH - like_btn[0], HEIGHT - ignore_y)
        cmnt_like_btn = locate(images.carousel.comment_like, region = region)

        if not cmnt_like_btn:# if not found
            if not_found_after > 6:
                log("No more comments exits...")
                #if cmnt_like_btn not found after eight time scrolling, then  break
                break

            not_found_after += 1
            # adding mode comments if add_cmnt_btn found
            add_cmnt_btn = locate(images.carousel.comment_add)

            if add_cmnt_btn:
                #add comments
                click_btn(add_cmnt_btn, 1, 5, 1, 5)
                sleep_uniform(1, 2)
                log(f"New comments loaded....")

       
            log(f"--> Scrolling")
            units = random.randrange(100, 300)

            ignore_y -= units
            if ignore_y < 0:
                ignore_y = 0

            pyautogui.scroll(-(units))
            sleep_uniform(0.2, 0.4)

            is_crolled = True # to read new comments
            continue

        #  not_found_after
        not_found_after = 0
        
        if decision():
            # find commented
            if is_crolled:
                found_commented_emoji = read_comments(like_btn, from_y=ignore_y)
                commented_emoji.update(found_commented_emoji)
                is_crolled = False # to stop for searching emoji until scroll


                if not do_like:
                    # break while loop if ccomments noot found after 6 times scrolling
                    if len(found_commented_emoji) == 0:
                        comments_not_found += 1

                    if len(commented_emoji) > 0 or comments_not_found > 6:
                        #stop comment like
                        break

            if do_like:
                click_btn(cmnt_like_btn, 0, 1, 0, 1)
                liked += 1
                log(f"Comment liked [{liked}/{amount}]")
                
                sleep(random.uniform(0.2, 0.8))

                if decision(): #move away fro comment_like button
                    log("------> moving away from like button")
                    move_x = cmnt_like_btn[0] - random.randint(20, 120)
                    
                    if (like_btn[1] - 220) > y:
                        #check if the like button near to like button
                        # if the cursor leave the comment area then further scrolling is not possible.
                        move_y = y + random.randint(50, 120)
                    else:
                        #it is near to the like button
                        move_y = y + random.randint(5, 10)

                    cursor.move_to([move_x, move_y])
                    sleep(random.uniform(0.1, 0.5))

        else:
            sleep_uniform(0.1, 0.5)
            
        ignore_y = cmnt_like_btn[1] + 60

    return (liked, commented_emoji)



def read_comments(like_pos, from_y):
    img = { "heart" : images.comments_read.heart, "fire" : images.comments_read.fire, "laugh" : images.comments_read.laugh,
           "heart_eye" : images.comments_read.heart_eye}

    from_x = like_pos[0]
    to_x = WIDTH - like_pos[0]
    to_y = HEIGHT - like_pos[1]

    found = {}

    while True:
        is_found = False

        for emoji in img:
            emoji_loc = locate(img[emoji], confidence= 0.93, region=(from_x, from_y, to_x, to_y))
            if not emoji_loc:
                continue
            
            if found.get("emoji"):
                found[emoji] += 1
            else:
                found[emoji]  = 1


            is_found = True
            from_y = emoji_loc[1] + 20


        if not is_found:
            log("------> No comments found....")
            break

    return found


def emoji_btn_click(comment_emoji, input = False):
    if input:
        move_to(comment_emoji, 120, 121, 0, 1, x_opr = "+", y_opr = "+")
    else:
        move_to(comment_emoji, 1, 10, 1, 10)

    comment_emoji2 = locate(images.carousel.comment_emoji, confidence= 0.8)
    if not comment_emoji2:
        move_to(comment_emoji, 120, 150, 5, 10,  x_opr = "-", y_opr = "-")
        sleep_uniform(0.6, 1.2)

        comment_emoji2 = locate(images.carousel.comment_emoji, confidence= 0.8)
        if not comment_emoji2:
            log("-------> Still not found Comment emoji....")
            return 
        
        if input:
            move_to_unhumaize(comment_emoji2, 120, 121, 0, 1, x_opr = "+", y_opr = "+")
        else:
            move_to_unhumaize(comment_emoji, 1, 10, 1, 10)

    sleep_uniform(0.1, 0.6)
    pyautogui.click()
    return True
    
    

def make_comment(commented_emoji: dict, text_comments_obj : TextComments):
    emoji_btn = { "heart" : images.comments_emoji.heart, "fire" : images.comments_emoji.fire, "laugh" : images.comments_emoji.laugh,
                 "heart_eye" : images.comments_emoji.heart_eye}
    
    no_of_emoji = 2
    

    comment_emoji = locate(images.carousel.comment_emoji, confidence= 0.8)
    if not comment_emoji:
        log("-------> Comment emoji not found....")
        return ([], False)
    #click on emoji butn

    # if decision(most=True): # write text comments

    #     st = emoji_btn_click(comment_emoji, input=True)# clicck ccomment input box
    #     if not st:
    #         log("Not ccomment emoji found...")
    #         return ([], False)

    #     sleep(random.uniform(0.2, 0.8))
    #     text_comment = f" {text_comments_obj.get_comment}  "
    #     pyautogui.write(text_comment, interval=random.uniform(0.10, 0.24))
    #     sleep_uniform(0.5, 1.2)
    #     no_of_emoji = 1


    st = emoji_btn_click(comment_emoji, input=False)# clicck ccomment input box
    if not st:
        return ([], False)
    sleep(random.uniform(0.4, 1.5))


    is_emoji_loaded = locate_until(images.carousel.emoji_most_popular_lbl, confidence= 0.9, timeout=10)
    if not is_emoji_loaded:
        log("-------> Emoji is not loaded")
        return ([], False)

    is_comment_box_focus = False

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

        count = random.randint(2, 5)
        emoji_count += 1

        for i in range(count):
            pyautogui.click()
            sleep(random.uniform(0.1, 0.2))


        sleep(random.uniform(0.5, 1.5))
        commented.append(emoji)

    print("sleeping")

    three_dot = locate(images.carousel.three_dot, confidence= 0.92)

    # entr key
    if True and three_dot: # to press enter key
        sleep(random.uniform(0.3, 0.8))
        pyautogui.press('enter') 
        sleep(random.uniform(0.6, 1))
        
        # move away from emoji popup and click to close it
        click_btn(three_dot, 40, 80, 5, 30, x_opr="-")
        sleep(random.uniform(0.5, 1.5))

    else:
        # use emoji button to close emoji popup
        click_btn(comment_emoji, 1, 10, 1, 10)
        sleep(random.uniform(0.4, 1))
        pyautogui.press('enter')

        # to press click button insted of right (->) button to get next post
        is_comment_box_focus = True

    sleep(random.uniform(1.2, 3))
    return (commented,  is_comment_box_focus ) 
        




if __name__ == "__main__":
    sleep(2)
    # comment_emoji = locate(images.carousel.comment_emoji, confidence= 0.8)
    # pyautogui.moveTo(comment_emoji[0], comment_emoji[1], duration=0.4)
    # exit()
    d = carousel(amount=60, do_comments=True, do_like_comments=True, save_post=False, randomize=False)
    print(d)

