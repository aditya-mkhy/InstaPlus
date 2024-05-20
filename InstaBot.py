import webbrowser as web
import os
import pathlib
import pyautogui
from time import sleep
import random
from PIL import Image
from humancursor import SystemCursor
import images
from util import locate, decision, is_video, positioned_like_button, is_mute, mute, un_mute, click_on, next_feed
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

    def reels_window(self):
        #chek if reels winow is already opend
        location = locate(images.reels.on_reels_btn)
        if location:
            log("Reels window is already open..")
            return True
        
        location = locate(images.reels.reels_btn)
        if not location:
            raise ValueError("Reels Icon not found....")
        
        x = random.randint(1, 8)
        y = random.randint(1, 10)
        self.cursor.move_to([location[0]-x, location[1]+y])

        sleep(random.uniform(0.1, 0.4))
        click_on(click_duration = random.uniform(0.1, 0.2))

        x = location[0] + random.randint(80, 200)
        y = location[1] + random.randint(20, 60)
        sleep(random.uniform(0.3, 0.8))

        self.cursor.move_to([x, y])
        return True
    
    def send_reel(self, name = None):
        direct_button = locate(images.reels.direct_btn)
        if not direct_button:
            print("Direct Button not found")
            return
        x = direct_button[0] - random.randint(1, 10)
        y = direct_button[1] + random.randint(1, 10)

        self.cursor.move_to([x, y])

        sleep(random.uniform(0.1, 0.5))
        pyautogui.click()
        sleep(random.uniform(1, 1.5))

        suggested_label = locate(images.reels.suggest_lbl)
        if not suggested_label:
            sleep(random.uniform(1, 2))
            suggested_label = locate(images.reels.suggest_lbl)
            if not suggested_label:
                print("suggested_label not found")
                return
        
        if name:
            pyautogui.write(name, interval=0.321)
            sleep(random.uniform(1, 2))
            y = suggested_label[1] + random.randint(8, 60)

        else:
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

                log(f"Post liked")
                liked += 1

                if True:
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
                log("reel skipped randomly..")
                if decision():
                    watch_time = random.randrange(8, 25, 2)
                else:
                    watch_time = random.uniform(2, 5)
                    if decision(): #pause the reel
                        if is_cursor_on_reel: # pause by left click
                            pyautogui.click()
                            print(f"Pause by click")
                        else:
                            print(f"Pause by pause button")
                            pyautogui.press('playpause')

                log(f" Watching reel for {convert_time(watch_time)} (Not liking)")
                sleep(watch_time)



        log(f"Task Completed : Like reels")
        log(f"Number of reels liked = {liked}")



    def like_feed(self, amount = 5):
        liked = 0
        # self.open_instagram()

        while True:
            scroll = random.randrange(140,260, 10)
            pyautogui.scroll(-abs(scroll))
            sleep(random.uniform(0.2, 0.8))

            location = locate(images.home.like, region=(200, 0, self.width, self.height))
            if not location:
                print("Like-button-not-found...")
                continue

            video = is_video(location)
            
            if not decision():#like or not
                positioned_like_button(location[1], self.height)
                if video:
                    print(f"This is a video....")
                    view_time = random.randrange(4, 20, 1)
                    if is_mute():
                        print("Video is muted")
                        un_mute()
                        print("Now it is un_muted")

                else:
                    print(f"This is a photo")
                    view_time = random.randrange(2, 10, 1)
                    
                sleep(view_time)

                location = locate(images.home.like, region=(200, 0, self.width, self.height))

                if not location:
                    print("error ==> location not found", location)
                    continue


                x = random.randint(2,10)
                y = random.randint(2,10)

                self.cursor.move_to([location[0] + x, location[1] + y])

                click_on(click_duration = random.uniform(0.1, 0.3))

                print(f"Post liked")
                liked += 1

                x = location[0] + random.randint(80, 300)
                y = location[1] - random.randint(150, 300)

                self.cursor.move_to([x, y])

                liked += 1

            else:
                print("skipping the post...")
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
                print(f"Task completed")
                print(f"Number of post liked = {liked}")
                break



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
        location = locate(images.home.logo)
        if location:
            return True
        
        return False


if __name__ == "__main__":
    insta = InstaBot()
    insta.like_feed(5)
    sleep(68)
    insta.like_reels(20)
    