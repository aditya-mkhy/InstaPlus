import json
from datetime import datetime
import os
from util import log

def today():
    return datetime.now().strftime('%d-%m-%Y')

class DB(dict):
    def __init__(self, file: str = None):
        self.file = file

        if not file:
            self.file = "./data/db.txt"

        self.__base_data = {"liked" : 0, "already_liked" : 0, "comment" : 0, "comment_liked" : 0, "followed": 0}


        if not os.path.exists(self.file):
            #if file not exits, create new one
            self.write(refresh = True)

        self.read()
        
    def read(self) -> dict:
        with open(self.file, "r") as ff:
            try:
                self.update(json.loads(ff.read()))
                return self
            except:
                print("ErrorInDataBase: Can't read it..")
                return self.write(refresh = True)
            
    def get_today(self) -> dict:
        return self.get(today())
    
    def create_today(self) -> dict:
        self[today()] = self.__base_data
        return self[today()]

    def write(self, refresh = False) -> dict:
        if refresh:
            self.update({
                today() : self.__base_data})

        with open(self.file, "w") as tf:
            tf.write(json.dumps(self))

    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.write()

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except:
            return self.create_today()
            

    def add_(self, action, value = 1):
        print(f"Actions => {action}")

        if action == "like":
            action = "liked"

        elif action == "comment" or action == "cmnt":
            action = "comment"

        elif action == "already_liked":
            action = "already_liked"

        elif action == "comment_like":
            action = "comment_liked"

        elif action == "follow":
            action = "followed"

        else:
            raise AttributeError(f"'DB' object has no attribute 'add_{action}'")
            
        
        data = self.get_today()
        data[action] += value
        self[today()] = data
        

    def __getattr__(self, name:str, value: int = 1):
        if name.startswith("add_"):
            action = name.split("add_")[1]
            return lambda: self.add_(action=action, value = value)
        
        raise AttributeError(f"'DB' object has no attribute '{name}'")
    
    def display(self, day = today(), title = ""):
        info = self[today()]

        log(f"-------- {title} -------------------------------")
        log(f"Liked  --------: {info['liked']}")
        log(f"Already liked -: {info['already_liked']}")
        log(f"Comments ------: {info['comment']}")
        log(f"Comments liked : {info['comment_liked']}")
        log(f"Following -----: {info['followed']}")
        log("---------------------------------------------------")


if __name__ == "__main__":
    d = DB()
    d.add_like()