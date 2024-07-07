import os
import time

mint = input("Enter the time : ")
try:
    mint = int(mint)
except:
    raise ValueError("The time shoube in number form.")
time.sleep(60*mint)
os.system("shutdown /h")