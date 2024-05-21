import webbrowser as web
import os
import pathlib
import pyautogui
from time import sleep
import random
from PIL import Image
from humancursor import SystemCursor
import images
from util import locate, decision, content_type, positioned_like_button, is_mute, mute, un_mute, click_on, next_feed
from util import convert_time, log



class InstaBot:
    def __init__(self, browser_path = None) -> None:
        self.width, self.height = pyautogui.size() #screen width and height

        #select the browser where instagram is logged in
        self.browser_path = browser_path
        if self.browser_path == None:
            self.browser_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        
        if os.path.exists(self.browser_path):
            web.register('browser', None, web.BackgroundBrowser(self.browser_path))
            self.browser = web.get('browser')

        else:
            self.browser_path = None
            self.browser = web

        self.friends = [ "Lakshay Saini", "ik"]

        #humazine mouse 
        self.cursor = SystemCursor()

        #to store profile
        self.reels_share_profile = {}

    def close_instagram(self):
        pyautogui.hotkey('ctrl', 'w')


    def explore(self, amount = 5, do_comment = False, like_comments = True, do_share = False, save_post = False):
        liked = 0
        comment = 0
        comment_liked = 0
        followed = 0
        self.explore_window()
        

        while liked < amount:
            next_button = locate(images.explore.next, confidence= 0.8)
            if not next_button:
                raise ValueError("Next button not found...")

            x = next_button[0] + random.randint(2, 5)
            y = next_button[1] + random.randint(1, 5)
            self.cursor.move_to([x, y])
            sleep(random.uniform(0.1, 0.5))
            pyautogui.click(interval=random.uniform(0.1, 0.2))
            sleep(random.uniform(0.6, 1.5))

            
            

            like_btn = locate(images.home.like, region=(200, 0, self.width, self.height))
            if not like_btn:
                print("Like-button-not-found...")
                sleep(random.uniform(0.2, 0.8))
                continue
            x = like_btn[0] - 200
            y = like_btn[1] - 100
            is_video = content_type(x, y)
            
            if decision():#like or not
                if is_video:
                    log(f"This is a video....")
                    watch_time = random.randrange(8, 25, 1)
                    if is_mute():
                        log(f"---> Video is muted")
                        s = un_mute()
                        log(f"---> Now, it is unmute")

                else:
                    log(f"This is a photo")
                    watch_time = random.randrange(2, 10, 1)
                    
                log(f"Watching post for {convert_time(watch_time)}")
                sleep(watch_time)

                x = like_btn[0] + random.randint(2, 8)
                y = like_btn[1] + random.randint(2, 8)

                self.cursor.move_to([ x, y])

                click_on(click_duration = random.uniform(0.1, 0.3))

                liked += 1
                log(f"Post liked [{liked}/{amount}]")


                if decision() and like_comments:# like comments
                    commnet_like_amout = random.randint(2, 10)
                    comment_liked = self.like_comments(like_btn, amount=commnet_like_amout)
                    log(f"Total comment liked -> {comment_liked} ")

                else:
                    log("Skipping commnets like...")



            else:
                if is_video:
                    log(f"This is a video....")
                    watch_time = random.randrange(3, 12, 1)
                    if watch_time > 8:
                        if decision():
                            s = mute()
                            if s:
                                log(f"---> Video muted")
                
                else:
                    log(f"This is a photo")
                    watch_time = random.randrange(2, 5, 1)

                log(f"Watching post for {convert_time(watch_time)} (not liking)")
                sleep(watch_time)


                    
        
    def like_comments(self, like_btn, amount = 5):
        liked = 0
        ignore_y = 0 # to ingnore skipped like
        not_found_after = 0
        log(f"Number of comments to be liked is {amount}")


        sleep(random.uniform(0.5, 1))
        x = like_btn[0] +  random.randint(80, 200)
        y = like_btn[1] - random.randint(100, 200)
        self.cursor.move_to([x, y]) #move to like button
        sleep(random.uniform(0.3, 1))

        while liked <  amount:

            cmnt_like_btn = locate(images.explore.comment_like, region=(like_btn[0], ignore_y, self.width, self.height))

            if not cmnt_like_btn:
                if not_found_after > 5:
                    log("No more commnets to likes...")
                    return liked

                not_found_after += 1
                # adding mode comments if buttton found
                add_cmnt_btn = locate(images.explore.comment_add)
                if add_cmnt_btn:
                    x = add_cmnt_btn[0] + random.randint(1, 5)
                    y = add_cmnt_btn[1] - random.randint(1, 5)

                    sleep(random.uniform(0.8, 2))
                    self.cursor.move_to([x, y])

                    sleep(random.uniform(0.1, 0.3))
                    pyautogui.click(interval=random.uniform(0.1, 0.2))
                    sleep(random.uniform(1, 3))
                    log(f"New comments loaded....")

                else:
                    print("New Cmmnts not found")


                log(f"--> Scrolling")
                units = random.randrange(80, 300)
                ignore_y -= units
                if ignore_y < 0:
                    ignore_y = 0
                print(f"Subtract {units} from equation y and now its value = {ignore_y}")
                pyautogui.scroll(-(units))
                sleep(random.uniform(0.5, 1.3))
                continue

            not_found_after = 0 
            print(f"Location ==> {cmnt_like_btn}")

            if decision():

                x = cmnt_like_btn[0] 
                y = cmnt_like_btn[1]

                # reading ccomments
                sleep(random.uniform(1, 3))
                
                self.cursor.move_to([x, y]) #move to like button
                sleep(random.uniform(0.1, 0.7))
                pyautogui.click(interval = random.uniform(0.10, 0.3))
                liked += 1
                log(f"Comment liked [{liked}/{amount}]")

                sleep(random.uniform(0.5, 1.3))

                if decision(): #move away fro comment_like button
                    print("moving away from like button")
                    move_x = x - random.randint(80, 150)
                    
                    if (like_btn[1] - 220) > y:
                        #check if the like button near to like button
                        # if the cursor leave the comment area then further scrolling is not possible.
                        move_y = y + random.randint(50, 120)

                    else:
                        #it is near to the like button
                        move_y = y + random.randint(5, 10)

                    self.cursor.move_to([move_x, move_y])
                    sleep(random.uniform(0.2, 0.9))
            else:
                
                sleep(random.uniform(0.8, 1.3))
                
            ignore_y = cmnt_like_btn[1] + 60

        return liked  
    

    def reels_window(self):
        #chek if reels winow is already opend
        location = locate(images.reels.on_reels_btn, confidence= 0.8)
        if location:
            log("Reels window is already open....")
            return True
        
        location = locate(images.reels.reels_btn, confidence= 0.8)
        if not location:
            raise ValueError("Reels Icon not found....")
        
        x = random.randint(1, 8)
        y = random.randint(1, 10)
        self.cursor.move_to([location[0]-x, location[1]+y])

        sleep(random.uniform(0.1, 0.4))
        click_on(click_duration = random.uniform(0.1, 0.2))

        x = location[0] + random.randint(350, 550)
        y = location[1] + random.randint(80, 160)
        sleep(random.uniform(0.3, 0.8))

        self.cursor.move_to([x, y])
        return True
    
    def send_reel(self, name = None):
        direct_button = locate(images.reels.direct_btn)
        if not direct_button:
            log("Direct Button not found...")
            return
        x = direct_button[0] - random.randint(1, 10)
        y = direct_button[1] + random.randint(1, 10)

        self.cursor.move_to([x, y])

        sleep(random.uniform(0.1, 0.5))
        pyautogui.click()
        sleep(random.uniform(1, 1.5))

        suggested_label = locate(images.reels.suggest_lbl, confidence= 0.8)
        if not suggested_label:
            sleep(random.uniform(1, 2))
            suggested_label = locate(images.reels.suggest_lbl, confidence= 0.7)
            if not suggested_label:
                log("Suggested_label not found")
                return
        
        if name:

            profile = self.reels_share_profile.get(name)
            is_scrolled = False

            if profile:
                # print(f"Profile Found")
                x = suggested_label[0] + random.randint(50,250)
                y = suggested_label[1] - random.randint(1, 5)
                sleep(random.uniform(0.1, 0.6))
                self.cursor.move_to([x, y])
                sleep(random.uniform(0.1, 0.5))

                prof_location = None
                is_scrolled = True
                for i in range(5):
                    prof_location = locate(profile, confidence= 0.7)
                    if prof_location:
                        break
                        
                    pyautogui.scroll(-(random.randrange(60, 120)))
                    sleep(random.uniform(0.1, 0.7))
                
                if prof_location:
                    x = prof_location[0] + random.randint(10,100)
                    y = prof_location[1] + random.randint(1, 5)

                    sleep(random.uniform(0.1, 0.3))
                    self.cursor.move_to([x, y])

                else:
                    # print("can't find the profile after scrolling")
                    profile = None

            if not profile:
                # print("not profile")

                if is_scrolled:
                    # clicking on "To:" input box
                    x = suggested_label[0] + random.randint(1, 10)
                    y = suggested_label[1] + random.randint(48, 75)
                    sleep(random.uniform(0.1, 0.6))
                    self.cursor.move_to([x, y])
                    sleep(random.uniform(0.1, 0.3))
                    pyautogui.click()

                #enter name in input box
                pyautogui.write(name, interval=0.321)
                sleep(random.uniform(2, 3))

                x = suggested_label[0] - 45
                y = suggested_label[1] + 10
                x2 = 100
                y2 = 35

                region = (int(x), int(y), x2, y2)
                img = pyautogui.screenshot(region = region)

                self.reels_share_profile[name] = img
                log(f"---> {name}'s  profile pic saved")

                y = suggested_label[1] + random.randint(8, 60)
                x = suggested_label[0] + random.randint(10, 300)
                
        else:
            log("Reel sent to first person in list")
            y = suggested_label[1] + random.randint(40, 100)
            x = suggested_label[0] + random.randint(10, 300)

        self.cursor.move_to([x, y])
        sleep(random.uniform(0.1, 0.3))

        pyautogui.click()
        sleep(random.uniform(0.8, 2))

        write_msg_lbl = locate(images.reels.write_msg_lbl, confidence= 0.8 )
        if not write_msg_lbl:
            sleep(random.uniform(2, 3))
            write_msg_lbl = locate(images.reels.write_msg_lbl , confidence= 0.8)
            if not write_msg_lbl:
                print("Not found label")
                return 


        x = write_msg_lbl[0] + random.randint(10, 200)
        y = write_msg_lbl[1] + random.randint(50, 80)
        self.cursor.move_to([x, y])
        sleep(random.uniform(0.4, 0.9))
        pyautogui.click()

        return True

        
    def like_reels(self, amount = 5, do_comment = False, do_share = False, save_post = False):
        liked = 0
        is_cursor_on_reel = False
        sleep(5)
        self.reels_window()
        sleep(random.uniform(0.8, 3))


        while liked < amount:
            #scroll reels
            scroll = random.randrange(60,200, 10)
            pyautogui.scroll(-abs(scroll))
            sleep(random.uniform(1, 3))


            location = locate(images.reels.like, region=(200, 0, self.width, self.height))
            if not location:
                log("Like-button-not-found...")
                continue

            if decision(): #like or not reel

                #watching the reelk
                watch_time = random.randrange(10, 30, 1)
                log(f"Watching reel for {convert_time(watch_time)}")
                sleep(watch_time)

                # random location on like button
                x = random.randint(1, 8)
                y = random.randint(1,10)
                self.cursor.move_to([location[0]-x, location[1]+y])

                sleep(random.uniform(0.1, 0.9))

                click_on(click_duration = random.uniform(0.1, 0.3))

                liked += 1
                log(f"Post liked [{liked}/{amount}]")


                if decision():
                    name = random.choice(self.friends)
                    st = self.send_reel(name=name)
                    if st:
                        log(f"Reel sendt to -> {name}")

                # move cursor from like button
                if decision():# move on the reel
                    x = location[0] - random.randint(180, 400)
                    y = location[1] + random.randint(10, 200)
                    is_cursor_on_reel = True

                else:# movve away from the reel
                    x = location[0] + random.randint(40, 200)
                    y = location[1] + random.randint(20, 200)
                    is_cursor_on_reel = False

                self.cursor.move_to([x, y])
                sleep(random.uniform(0.5, 2))


            else:
                log("Reel skipped randomly..")
                if decision():
                    watch_time = random.randrange(8, 25, 2)
                else:
                    watch_time = random.uniform(2, 5)
                    if decision(): #pause the reel
                        if is_cursor_on_reel: # pause by left click
                            pyautogui.click()
                            # print(f"Pause by click")
                        else:
                            # print(f"Pause by pause button")
                            pyautogui.press('playpause')

                log(f" Watching reel for {convert_time(watch_time)} (Not liking)")
                sleep(watch_time)



        log(f"Task Completed : Like reels")
        log(f"Number of reels liked = {liked}")



    def like_feed(self, amount = 5):
        liked = 0
        self.home_window()

        while True:
            scroll = random.randrange(140,260, 10)
            pyautogui.scroll(-abs(scroll))
            sleep(random.uniform(0.2, 0.8))

            location = locate(images.home.like, region=(200, 0, self.width, self.height))
            if not location:
                print("Like-button-not-found...")
                continue

            is_video = content_type(location[0]+ 200, location[1] - 200)
            
            if not decision():#like or not
                positioned_like_button(location[1], self.height)
                if is_video:
                    log(f"This is a video....")
                    view_time = random.randrange(4, 20, 1)
                    if is_mute():
                        log("Video is muted")
                        un_mute()
                        log("Now it is un_muted")

                else:
                    log(f"This is a photo")
                    view_time = random.randrange(2, 10, 1)
                    
                sleep(view_time)

                location = locate(images.home.like, region=(200, 0, self.width, self.height))

                if not location:
                    log("error ==> location not found", location)
                    continue


                x = random.randint(2,10)
                y = random.randint(2,10)

                self.cursor.move_to([location[0] + x, location[1] + y])

                click_on(click_duration = random.uniform(0.1, 0.3))

                liked += 1
                log(f"Post liked [{liked}/{amount}]")

                x = location[0] + random.randint(80, 300)
                y = location[1] - random.randint(150, 300)

                self.cursor.move_to([x, y])

            else:
                log("Feed skipped randomly..")
                if decision(): # viewing the post 
                    positioned_like_button(location[1], self.height)
                    if is_video:
                        view_time = random.randrange(1, 10, 1)
                    else:
                        view_time = random.randrange(1, 3, 1  )
                    sleep(view_time)


                next_feed(location[1]) # scrolling to next feed
                sleep(1)


            if liked >= amount:
                log(f"Task Completed : Like reels")
                log(f"Number of reels liked = {liked}")
                break

    def explore_window(self):
        #chek if reels winow is already opend
        location = locate(images.explore.on_explore_btn, confidence= 0.8)
        if location:
            log("Home window is already open..")
            return True
        
        location = locate(images.explore.explore_btn, confidence= 0.8)
        if not location:
            raise ValueError("Home Icon not found....")
        
        x = random.randint(1, 8)
        y = random.randint(1, 10)
        self.cursor.move_to([location[0]-x, location[1]+y])

        sleep(random.uniform(0.1, 0.4))
        click_on(click_duration = random.uniform(0.1, 0.2))

        x = location[0] + random.randint(550, 700)
        y = location[1] + random.randint(150, 300)
        sleep(random.uniform(0.3, 0.8))

        self.cursor.move_to([x, y])
        sleep(random.uniform(0.1, 0.4))
        click_on(click_duration = random.uniform(0.1, 0.2))
        sleep(random.uniform(2, 5))
        return True

    def home_window(self):
        #chek if reels winow is already opend
        location = locate(images.home.on_home_btn, confidence= 0.8)
        if location:
            log("Home window is already open..")
            return True
        
        location = locate(images.home.home_btn, confidence= 0.8)
        if not location:
            raise ValueError("Home Icon not found....")
        
        x = random.randint(1, 8)
        y = random.randint(1, 10)
        self.cursor.move_to([location[0]-x, location[1]+y])

        sleep(random.uniform(0.1, 0.4))
        click_on(click_duration = random.uniform(0.1, 0.2))

        x = location[0] + random.randint(350, 550)
        y = location[1] + random.randint(80, 160)
        sleep(random.uniform(0.3, 0.8))

        self.cursor.move_to([x, y])
        return True
    
    def move_cursor_to_page(self, location):
        x = location[0] + random.randint(350, 550)
        y = location[1] + random.randint(80, 160)
        sleep(random.uniform(0.3, 0.8))
        self.cursor.move_to([x, y])

        return True
    

    def open_instagram(self) -> bool:
        already_open = self.is_instgram()
        if already_open:
            return True
        #open instgram
        self.browser.open("https://www.instagram.com", new=0, autoraise=True)
        sleep(10)
        already_open = self.is_instgram()
        if already_open:
            return True
        
        raise ValueError("Not able to open instagram, or may be not logged in.")
        


    def is_instgram(self) -> bool:
        #check the instagram logo on the screen
        #to make sure that instagram is open

        location = locate(images.home.logo_full, confidence= 0.8)
        if location:
            self.move_cursor_to_page(location)
            return True
        
        #minimized window logo
        location = locate(images.home.logo, confidence= 0.8)
        if location:
            self.move_cursor_to_page(location)
            return True
        
        return False


if __name__ == "__main__":
    insta = InstaBot()
    insta.open_instagram()

    sleep(4)

    insta.explore(amount=20)

    # for i in range(4):
    #     insta.open_instagram()
    #     sleep(random.uniform(1,3))

    #     insta.like_feed(random.randint(5, 20))
    #     insta.like_reels(random.randint(15, 30))

    #     insta.close_instagram()

    #     shutdown_time = random.randrange(20, 60) * 60
    #     log(f"======> Shutdown for {convert_time(shutdown_time)}")
    #     sleep(shutdown_time)
    
    # os.system("shutdown /h")

