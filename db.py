import json
from datetime import datetime
import os

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
        return self.get(today(), self.__base_data)

    def write(self, refresh = False) -> dict:
        if refresh:
            self.update({
                today() : self.__base_data})

        with open(self.file, "w") as tf:
            tf.write(json.dumps(self))

    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.write()

if __name__ == "__main__":
    d = DB()
    # d["20-01-2025"] = 10
    print(d)