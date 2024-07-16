import pyautogui
import time

id_zoom = "933 490 2569"
pass_zoom = "085076"

pyautogui.press("win")

time.sleep(1)

pyautogui.write("zoom" ,interval=0.3)

time.sleep(1)

pyautogui.press("enter")

time.sleep(2)

pyautogui.hotkey('win', 'up')


time.sleep(2)

img = pyautogui.locateCenterOnScreen('Capturar.png', confidence=0.7)

time.sleep(2)

pyautogui.click(img.x , img.y)

time.sleep(2)

pyautogui.write(id_zoom, interval=0.2)

pyautogui.press("enter")

time.sleep(1)

pyautogui.write(pass_zoom, interval=0.2)

pyautogui.press("enter")


