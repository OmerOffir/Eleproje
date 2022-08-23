import pyautogui as pg
import random
import time

time.sleep(5)

for i in range(20):
    pg.write(" Do you want to play? ")
    time.sleep(0.5)
    pg.press("Enter")