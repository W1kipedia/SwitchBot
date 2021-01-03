import os
import sys
import time

#it's a very simple way of restarting the bot entirely without user interrupting the bot in terminal
try:
    seconds = int(sys.argv[1])
except:
    print("no amount of seconds were provided so going by 15 seconds by default")
    seconds = 15
print(f"restarting...this will take {seconds} seconds")
time.sleep(seconds)
print("starting switch-bot\n\n")
#note: if you're thinking of using this idea the code line below me should be edited in accordance with your computer and directed to the main file
os.system("main.py")