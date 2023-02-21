import cv2
import numpy as np
import pyautogui
import win32api
import pydirectinput
import win32gui
import time
import random
import winsound

image_bobr = cv2.imread("bobr.png") # Template image

threshold_bobr = 0.65 # Threshold for image matching
security_timer_seconds = 300 # Every 5 minutes, the program resets (casts the bober again) to prevent being stuck just in case that happens

has_played_start_sound = False
has_found_bobr = False
is_tracking_cursor_status = False
mouse_cursor_status = 0
last_security_action_time = time.time() # The initial time of the program is the "last security reset" since there hasn't been any yet
time_last_bobr_found = time.time()
max_time_bobr_found_without_action = 20

while(not win32api.GetKeyState(0x2E)<0):
    if (not has_played_start_sound):
        has_played_start_sound = True
        winsound.Beep(700, 250) # Plays a "beep" sound to notify the loop is ready to be executed
        print("ACTIVATED") 
    else:
        screenshot = np.array(pyautogui.screenshot()) # Take screenshot of the screen
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY) # Convert screenshot to grayscale

        # Perform template matching
        result_bobr = cv2.matchTemplate(gray_screenshot, cv2.cvtColor(image_bobr, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)

        # Get location of matched image
        min_val_bobr, max_val_bobr, min_loc_bobr, max_loc_bobr = cv2.minMaxLoc(result_bobr)
        
        # Check if image is found
        if (max_val_bobr >= threshold_bobr and not has_found_bobr):
            top_left_bobr = max_loc_bobr # Get coordinates of matched image (bobr)
            pyautogui.moveTo(top_left_bobr[0]+30, top_left_bobr[1]+78) # Move cursor to location of bobr
            has_found_bobr = True
            time_last_bobr_found = time.time()
            
        if (has_found_bobr):
            if (not is_tracking_cursor_status):
                mouse_cursor_status = win32gui.GetCursorInfo()
                is_tracking_cursor_status = True
            elif (is_tracking_cursor_status): 
                if (mouse_cursor_status != win32gui.GetCursorInfo()):
                    time.sleep(random.uniform(0.37, 0.58))
                    pydirectinput.click()
                    time.sleep(random.uniform(1.03, 2.29))
                    pyautogui.moveTo(random.randint(221,407), random.randint(262,371))
                    time.sleep(random.uniform(2.04, 3.12))
                    mouse_cursor_status = 0
                    is_tracking_cursor_status = False
                    has_found_bobr = False
                    pydirectinput.keyDown("f11")
                    pydirectinput.keyUp("f11")
                    time_last_bobr_found = time.time()
                    
        if (time.time() - time_last_bobr_found >= max_time_bobr_found_without_action):
            pyautogui.moveTo(random.randint(221,407), random.randint(262,371))
            time.sleep(random.uniform(1.04, 2.1))
            mouse_cursor_status = 0
            is_tracking_cursor_status = False
            has_found_bobr = False
            pydirectinput.keyDown("f11")
            pydirectinput.keyUp("f11")
            time.sleep(random.uniform(2.04, 4.1))
            
                    
        # time.time() is the current time and it substracts from the initial time (the first time we run the program)
        # then it compares the difference and if it is more or equal to 5 minutes, it will trigger the security reset + updates the last security action time to this moment
        if (time.time() - last_security_action_time >= security_timer_seconds):
            last_security_action_time = time.time()
            print("SECURITY RESET")
            
            pyautogui.moveTo(random.randint(221,407), random.randint(262,371))
            mouse_cursor_status = 0
            is_tracking_cursor_status = False
            has_found_bobr = False
            time.sleep(random.uniform(5.25, 8.50))
            pydirectinput.keyDown("f11")
            pydirectinput.keyUp("f11")
            
                    
winsound.Beep(400, 250) # Plays a sound to notify that the program has been terminated
print("----------------")
print("TERMINATED")