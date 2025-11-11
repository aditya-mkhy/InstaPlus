import webbrowser as web
import os
import pathlib
import pyautogui
from PIL import Image
from util import *
from carousel import carousel
from tools import open_explore, search_hashtag, search_user, shuffle
from feed import like_feed
from db import DB, today
from gpt import Gpt
import os

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
        self.db = DB()

        self.gpt = Gpt()

        


    def like_by_feed(self, amount = 5, do_comments = True, do_like_comments = False, randomize = True,  save_post = False ):
        self.db.display(title="Like_by_feed  task -> started")

        try:
            like_feed(amount, do_comments, do_like_comments, randomize, save_post, db = self.db)
        except Exception as e:
            log(f"Error[001] : {e}")

        self.db.display(title="Like_by_feed  task -> Finished")


    def explore(self, amount = 5, do_comments = True, do_like_comments = True, randomize = True, follow = True, save_post = False ):
        st = open_explore()
        if not st:
            log("Not able to open explore window, please check the error..")
            return
        
        self.db.display(title="Explore  task -> Started")
        try:
            carousel(amount=amount, do_comments=do_comments, do_like_comments=do_like_comments, 
                            randomize=randomize,follow=follow, save_post=save_post, gpt=self.gpt, db = self.db)
        
        except Exception as e:
            log(f"Error[002] : {e}")

        self.db.display(title="Explore task -> Finished")

    
    def like_by_hashtag(self, tags = list, amount = 5, do_comments = True, do_like_comments = True, randomize = True, follow = False, save_post = False ):
        self.db.display(title="Like By HashTag -> Started")
        
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
                carousel(amount=amount, do_comments=do_comments, do_like_comments=do_like_comments, 
                                        randomize=randomize,follow=follow, save_post=save_post, gpt=self.gpt, db = self.db)
               
            except Exception as e:
                log(f"Hashtag [{tag}] Search Error : {e}")
            
            sleep_uniform(30, 80)

        # information
        sleep_uniform(0.1, 0.2)
        self.db.display(title="Like By HashTag -> Finished")


    def like_by_user(self, users = [], amount = 5, do_comments = True, do_like_comments = False, randomize = True,  save_post = False ):
        self.db.display(title="Like By Users -> Started")

        for user in users:
            st = search_user(user)
            if not st:
                log("An error occured during searching for User.")
                continue

            if st == "no_post":
                log(f"{user} hasn't posted anything yet...")
                sleep_uniform(2, 5)
                continue

            carousel(amount=amount, do_comments=do_comments, do_like_comments=do_like_comments, 
                                randomize=randomize, save_post=save_post, gpt=self.gpt, db = self.db)

        # information
        sleep_uniform(0.1, 0.2)
        self.db.display(title="Like By Users -> Started")

        
if __name__ == "__main__":

    instaBot = InstaPlus()
    tags = [
        "#ironman", 
        "#waterfall"
    ] #45

    hashtags = [
        "#mahadev",
        "#triund",
        "#tree",
        "#nature",
        "#waterfall",
        "#tree",
        "#sky",
        "#northernlights",
        "#ocean",
        "#wildlife",
        "#birds",
        "#love",
        "#tracking",
        "#travel",
        "#exploring"
    ]

    hashtags = [
        "#InstaGood", "#InstaLike", "s#InstagramHub", "#InstaDaily", "#InstaPic",
        "#LifeStyle", "#Motivation", "#Wellness", "#Fitness", "#SelfCare",
        "#Fashionista", "#StreetStyle", "#StyleInspo", "#FashionAddict", "#InstaFashion",
        "#Foodie", "#FoodPorn", "#Yummy", "#FoodLover", "#HealthyEats",
        "#TravelGram", "#Wanderlust", "#TravelAddict", "#NomadLife", "#TravelDiaries",
        "#TechSavvy", "#Innovation", "#TechNews", "#GadgetGoals", "#AI",
        "#PhotographyLovers", "#PhotoArt", "#InstaArtist", "#CreativeShots", "#InstaPhoto",
        "#FollowMe", "#InstaFollow", "#LikeForFollow", "#Followers", "#FollowTrain"
    ]

   

    hashtags = shuffle(hashtags)


    instaBot.explore(amount=200, do_comments=True, do_like_comments=True, randomize=False, follow = True)

    instaBot.like_by_feed(amount=5, do_comments=False, do_like_comments=False, randomize=True)

    # sleep after every 5 hashtag
    for i in range(len(hashtags) // 5):
        use_tag = hashtags[:5]
        hashtags = hashtags[:5]
        instaBot.like_by_hashtag(tags=use_tag, amount=30, do_comments=True, do_like_comments=True, randomize=False, follow=False)

        sleep_uniform(300, 800)


    instaBot.like_by_feed(amount=10, do_comments=False, do_like_comments=False, randomize=True)

    sleep(10*1)
    user = []
    for i  in range(50):
        user.append("shrusti.music")
    instaBot.like_by_user( users = user, amount = 500, do_comments = True, do_like_comments = True, randomize = False,  save_post = False )


    instaBot.explore(amount=100, do_comments=True, do_like_comments=True, randomize=False, follow = False)

    log("Shutdown in two minutes....")
    sleep(60*2)
    os.system("shutdown /h")
    

