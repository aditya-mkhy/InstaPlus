import webbrowser as web
import os
import pathlib
import pyautogui
from PIL import Image
from util import *
from carousel import carousel
from tools import open_explore, search_hashtag, search_user
from feed import like_feed


class InstaPlus:
    def __init__(self, browser_path = None) -> None:
        
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

        # self.friends = [ "Lakshay Saini", "ik"]
        #to store profile
        self.reels_share_profile = {}

    def like_by_feed(self, amount = 5, do_comments = True, do_like_comments = False, randomize = True,  save_post = False ):
        info = {"liked" : 0, "comment" : 0, "comment_liked" : 0}
        try:
            info = like_feed(amount, do_comments, do_like_comments, randomize, save_post)
        except Exception as e:
            log(f"Error[001] : {e}")

        if info:
            sleep_uniform(0.1, 0.2)
            log("--------Like_by_feed task finished-----------------")
            log(f"Post Liked : {info['liked']}")
            log(f"Numer of Comments : {info['comment']}")
            log(f"Comments liked  : {info['comment_liked']}")
            log("---------------------------------------------------")
        else:
            log("An error occured during Like_by_feed task.")


    def explore(self, amount = 5, do_comments = True, do_like_comments = False, randomize = True,  save_post = False ):
        info = {"liked" : 0, "already_liked" : 0, "comment" : 0, "comment_liked" : 0}

        st = open_explore()
        if not st:
            log("Not able to open explore window, please check the error..")
            return

        try:
            info = carousel(amount=amount, do_comments=do_comments, do_like_comments=do_like_comments, 
                            randomize=randomize, save_post=save_post )
            
        except Exception as e:
            log(f"Error[002] : {e}")
        
        if info:
            sleep_uniform(0.1, 0.2)
            log("--------Explore task finished----------------------")
            log(f"Post Liked : {info['liked']}")
            log(f"Post Already Liked  : {info['already_liked']}")
            log(f"Numer of Comments : {info['comment']}")
            log(f"Comments liked  : {info['comment_liked']}")
            log("---------------------------------------------------")
        else:
            log("An error occured during Explore task.")

    
    def like_by_hashtag(self, tags = list, amount = 5, do_comments = True, do_like_comments = False, randomize = True,  save_post = False ):
        log("Task : Like post by Hashtag..")
        info = {"liked" : 0, "already_liked" : 0, "comment" : 0, "comment_liked" : 0}

        for tag in tags:
            if tags.index(tag) == 0:
                refresh = False
            else:
                refresh = True
                
            try:
                search_hashtag(tag, refresh=refresh)
            except Exception as e:
                log(f"Hashtag [{tag}] Search Error : {e}")
                continue

            try:
                tag_info = carousel(amount=amount, do_comments=do_comments, do_like_comments=do_like_comments, 
                                        randomize=randomize, save_post=save_post)
                if not tag_info:
                    log("An error occured during like by hashtag task.")

                else:
                    update_info(info, tag_info)
                    log(f"Like by hashtag is completed for hashtag : {tag}")
            except Exception as e:
                log(f"Hashtag [{tag}] Search Error : {e}")

            sleep_uniform(30, 80)

        # information
        sleep_uniform(0.1, 0.2)
        log("--------Hashtags task finished----------------------")
        log(f"Post Liked : {info['liked']}")
        log(f"Post Already Liked  : {info['already_liked']}")
        log(f"Numer of Comments : {info['comment']}")
        log(f"Comments liked  : {info['comment_liked']}")
        log("----------------------------------------------------")



    def like_by_user(self, users = [], amount = 5, do_comments = True, do_like_comments = False, randomize = True,  save_post = False ):
        log("Task : Like post by Usernames..")
        info = {"liked" : 0, "already_liked" : 0, "comment" : 0, "comment_liked" : 0}

        for user in users:

            st = search_user(user)
            if not st:
                log("An error occured during searching for User.")
                continue

            if st == "no_post":
                log(f"{user} hasn't posted anything yet...")
                sleep_uniform(2, 5)
                continue

            user_info = carousel(amount=amount, do_comments=do_comments, do_like_comments=do_like_comments, 
                                    randomize=randomize, save_post=save_post)
            if not user_info:
                log("An error occured during like by User task.")

            else:
                info.update(user_info)
                log(f"Like by User is completed for hashtag : {user}")

        # information
        sleep_uniform(0.1, 0.2)
        log("--------Like by Users task finished----------------")
        log(f"Post Liked : {info['liked']}")
        log(f"Post Already Liked  : {info['already_liked']}")
        log(f"Numer of Comments : {info['comment']}")
        log(f"Comments liked  : {info['comment_liked']}")
        log("---------------------------------------------------")
        
        
        
if __name__ == "__main__":
    instaBot = InstaPlus()
    tags = ["#snow", "#ironman", "#waterfall",]

    hashtags = ["#adventure", "#naturelover", "#outdoors", "#animals", "#beach", 
                "#sky", "#wildlife", "#hiking", "#explore"]
    hashtags2 = ['#likes', '#followback', '#instagram', '#followme', '#love', '#instalike', '#photography', '#followforfollow', '#photooftheday', '#likeforlike', '#picoftheday', '#fashion', '#following']


    users = ["mbg148", "nanuqdogphotography", "signewenneberg", "foto_marek"]

    # # instaBot.like_by_feed(amount=2, do_comments=True, do_like_comments=True, randomize=True)

    # instaBot.like_by_hashtag(tags=hashtags, amount=50, do_comments=True, do_like_comments=False, randomize=False)
    # # sleep(60*1)

    instaBot.explore(amount=400, do_comments=True, do_like_comments=True, randomize=False)
    sleep(60*2)
    os.system("shutdown /h")
    # instaBot.like_by_hashtag(tags=hashtags2, amount=30, do_comments=True, do_like_comments=True, randomize=False)



    # try:

    #     instaBot.explore(amount=50, do_comments=True, do_like_comments=False, randomize=False)

    # except Exception as e:
    #     log(f"Error ==> {e}")

    # import os
    # os.system("shutdown /h")

    # instaBot.like_by_user(users=["heidikvam"], amount=1000, do_comments=True, do_like_comments=False, randomize=False)

