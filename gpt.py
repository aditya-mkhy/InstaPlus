# linkedin_bot.py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
import time

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


from datetime import datetime
from pathlib import Path
import random
from time import sleep


def log(*args, **kwargs):
    print(f" INFO [{datetime.now().strftime('%d-%m-%Y  %H:%M:%S')}] ", *args, **kwargs)


def rsleep(min: float, max: float = None):
    """
    Pause for a random number of seconds between WAIT_TIME_RANGE.
    """
    if not max:
        max = min
    delay = random.uniform(min, max)
    log(f"Sleeping for {delay:.1f} seconds...")
    sleep(delay)

def write(path, word):
    for w in word:
        if w == " ":
            sleep(random.uniform(0.2, 0.9))
        else:
            sleep(random.uniform(0.03, 0.09))
        path.send_keys(w)

        

class Gpt:
    def __init__(self):
        self.url = "https://chatgpt.com/"
        self.count = 0
        self.headless = False
        self.new_msg_timeout = 180

        # init drivers
        self.driver_init()

        self.max_wait = WebDriverWait(self.driver, 90)
        self.min_wait = WebDriverWait(self.driver, 30)

        self.sec_wait = WebDriverWait(self.driver, 1)

        # open the link
        self.open_url()

    def send_image(self, image_path):
        timeout = 20

        # Count existing markdowns
        old_count = len(self.driver.find_elements(By.CLASS_NAME, "markdown"))
        log(f"Old count : {old_count}")


        # Upload the image file
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        file_input.send_keys(os.path.abspath(image_path))
        log("file is send...")

        # Wait for image preview to show up (upload complete)
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.h-full"))
            )
            
# 
            log("file is uploaded...")
        except TimeoutException:
            log("Failed to upload image")
            return "Image upload timed out"

        # Step 4: Press Enter to send the image
        textbox = self.driver.find_element(By.ID, "prompt-textarea")
        write(textbox, "write a comment")
        rsleep(0.4, 1.5)
        textbox.send_keys(Keys.ENTER)
        log("Promt send to execute")

        # Step 5: Wait for new response markdown to appear
        start_time = time.time()
        while time.time() - start_time < timeout:
            messages = self.driver.find_elements(By.CLASS_NAME, "markdown")
            if len(messages) > old_count:
                try:
                    # Wait until reply is fully generated
                    WebDriverWait(self.driver, 2).until_not(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Stop generating')]"))
                    )
                    # Refresh messages to avoid stale reference
                    messages = self.driver.find_elements(By.CLASS_NAME, "markdown")
                    return messages[-1].text
                except (TimeoutException, StaleElementReferenceException):
                    pass
            time.sleep(1)

        return "No response detected after upload"


    def send_prompt(self, prompt):
    
        # Count current markdown messages
        old_msgs = self.driver.find_elements(By.CLASS_NAME, "markdown")
        old_count = len(old_msgs)

        log(f"OldMessage : {old_count}")

        # Send the prompt
        textbox = self.driver.find_element(By.ID, "prompt-textarea")
        textbox.send_keys(prompt)
        rsleep(0.4, 1.5)
        textbox.send_keys(Keys.ENTER)
        log("Promt send to execute")

        # Wait until new markdown is added
        start_time = time.time()
        new_msg = None

        while time.time() - start_time < self.new_msg_timeout:
            messages = self.driver.find_elements(By.CLASS_NAME, "markdown")
            log(f"New Messagecount : {len(messages)}")
            if len(messages) > old_count:

                log(f"message is generating.. ")
                # Check if it's still typing (streaming animation shows up)
                try:
                    # wait for the "Stop generating" button to disappear (means done)
                    self.sec_wait.until_not(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Stop generating')]")))

                     # Re-fetch the messages to avoid stale reference
                    messages = self.driver.find_elements(By.CLASS_NAME, "markdown")
                    return messages[-1].text  #

                except TimeoutException:
                    log("Still generating....")
                    pass  # still generating

            time.sleep(1)

        return "no"
    
    def init_conversation(self):
        msg = """
Hi, 
From now this chat is used to generate the comments for instagram post.
I will give the other users comments on the post..
By observing that comments.. U generate a most approproate comment for that post..
And remeber, Just give the comment.. nothing extra..cause it goes directly in the post
Thank You."""
        reply = self.send_prompt(msg)
        print(f"ReplyFromChatGPT => {reply}")


    def open_url(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        log("wait completed...")

        try:
            textbox = self.max_wait.until(EC.element_to_be_clickable((By.ID, "prompt-textarea")))
            # textbox.send_keys("hi.. this is test")
            # rsleep(1, 2)
            # textbox.send_keys(Keys.ENTER)

            log("Everything is ready... let's rock and roll.....")
            time.sleep(5)
            self.init_conversation()
            time.sleep(2)
            return True

        except:
            log("Failed to open cht-gpt... please check")
            self.close()
            return False

    def close(self):
        log("===> Closing the browser....")
        self.driver.quit()


    def driver_init(self):
        log("Initializing the driver....")
        self.profile_path = "C:\\Users\\lostw\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\3bfxtj8s.default-release"

        self.firefox_options = Firefox_Options()
        self.firefox_options.set_preference("profile", self.profile_path)

        # Optional preferences to reduce detection
        self.firefox_options.set_preference("intl.accept_languages", "en-US")
        self.firefox_options.set_preference("media.volume_scale", "0.0")
        self.firefox_options.set_preference("dom.webdriver.enabled", False)
        self.firefox_options.set_preference("useAutomationExtension", False)
        # self.firefox_options.set_preference("general.platform.override", "iPhone")

        if self.headless:
            self.firefox_options.add_argument("--headless")
            self.firefox_options.add_argument("--width=1920")
            self.firefox_options.add_argument("--height=1080")

        # Set profile directory properly
        self.firefox_options.profile = self.profile_path

        # Start Firefox browser
        self.driver = webdriver.Firefox(options = self.firefox_options)
        log("Driver is ready to go...")

 

if __name__ == "__main__":
    ai = Gpt()

    m = """

the best place to be with uuuuu ⛺️🏔️✨🥰
Vous avez les mêmes passions avec votre acolyte ??

#bivouac
5 w
Awesome 😍😍
3 w4 likesReply
😍
3 w1 likeReply
C'est Magnifique 😍🔥c
4 w3 likesReply
👏
3 w1 likeReply
👏👏👏😍
3 w1 likeReply
😍
4 w2 likesReply
Magique 😍
3 w1 likeReply
Çok güzel👏👏👏
4 w3 likesReply
❤️
3 w1 likeReply
❤️
3 w1 likeReply
🙏🏼🙏🏼🙏🏼
3 w1 likeReply
❤️
4 w2 likesReply
Faut qu’on s’organise une randonnée 😍
5 w4 likesReply
🙌
4 w2 likesReply
😍😍
4 w1 likeReply
😍
4 w2 likesReply
❤️❤️
4 w2 likesReply
😍😍🙌🙌🙌
4 w1 likeReply
Le spot parfait en rando😍
4 w1 likeReply
😍
5 w1 likeReply
😍😍😍
4 w1 likeReply
😍
4 w1 likeReply
👏❤️
4 w1 likeReply
❤️❤️❤️❤️❤️
5 w1 likeReply
❤️❤️❤️
5 w3 likesReply
Such beautiful plans! Love it!
4 w3 likesReply
Beautiful 😍
4 w3 likesReply
Le reeeeeve absolu 😍
4 w1 likeReply
🙆🏻😎
4 w1 likeReply
😍
4 w2 likesReply
"""

    msg = ai.send_prompt(m)
    # path = "C:\\Users\\atoma\\Pictures\\Screenshots\\sd.png"
    # msg = ai.send_image(path)
    print(f"message ==> {msg}")
