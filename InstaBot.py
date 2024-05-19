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

        #humazine mouse 
        self.cursor = SystemCursor()


    def like_feed(self, amount = 5):
        liked = 0
        self.open_instagram()

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
    insta.like_feed(40)
    
