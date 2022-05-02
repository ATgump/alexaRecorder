from ipaddress import collapse_addresses
import random
from turtle import screensize
from selenium import webdriver
import pyautogui
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.chrome.service import Service
import json
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os


def randSleepTime(x,y):
    n = random.randint(x,y)
    time.sleep(n)
    return 0
def process_browser_logs_for_network_events(logs):
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
            "Network.response" in log["method"]
            or "Network.request" in log["method"]
            or "Network.webSocket" in log["method"]
        ):
            yield log
def delAudio(drive):
    try:
        if len(drive.find_elements_by_class_name("delete-displayed-recordings-text.clickable.enabled")) > 0:
            delete_button = drive.find_element_by_class_name("delete-displayed-recordings-text.clickable.enabled")
            delete_button.click()
            randSleepTime(2,4)
            delete_button_big_red =drive.find_element_by_class_name("apd-large-block-button.button-red")
            delete_button_big_red.click()
            randSleepTime(2,4)
            return 0
    except:
        print("no audio to delete")
        return 0



def scrapeAudio(name,volume):
    try:
        transcript = "audio not found"
        service_object = Service(binary_path)
        option = webdriver.ChromeOptions()
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        option.add_argument("user-data-dir=C:\\Users\\avery\\AppData\\Local\\Google\\Chrome\\User Data")
        option.add_argument("profile-directory=Profile 1")
        option.add_argument("exit_type=Normal")
        option.add_argument("exited_cleanly=true")
        option.add_experimental_option("detach",True)
        driver = webdriver.Chrome(service=service_object,options=option,desired_capabilities=capabilities)
        time.sleep(2)
        driver.get("https://www.amazon.com/alexa-privacy/apd/rvh?")
        time.sleep(8)
        os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume 0")
        time.sleep(2)
        pyautogui.press("volumemute")
        time.sleep(2)

        boxes = driver.find_elements_by_class_name("apd-content-box")
    except:
        print("driver failed to load history or content box not found")
        try:
            driver.quit()
        except:
            pass
        return 225
    audio_url = "didnt get updated"
    j = 0
    for box in boxes:
        try:
            transcript = box.find_element_by_class_name("record-summary-preview.data-warning-message").text
            if transcript.startswith("Audio") and j == 1:
                trans_out = transcript[1:-1]
                expandButton = box.find_element_by_class_name("apd-expand-toggle-button.button-clear")
                expandButton.click()
                randSleepTime(2,6)
                recBox = box.find_elements_by_class_name("record-item")
                recButton = recBox[1].find_element_by_class_name("apd-icon-button-round.play-audio-button.button-clear.fa.fa-play-circle")
                recButton.click()
                randSleepTime(2,6)
                perf = driver.get_log("performance")
                events = process_browser_logs_for_network_events(perf)
                print("events captured")
                for event in events:
                    try:
                        tt = event["params"]["request"]["url"]
                        if tt.startswith("https://www.amazon.com/alexa-privacy/apd/rvh/audio?uid"):
                            audio_url = tt
                    except:
                        continue
                collapse_button = box.find_element_by_class_name("apd-expand-toggle-button.button-clear.fa.fa-chevron-up")
                collapse_button.click()
                randSleepTime(2,6)
            elif transcript.startswith("Audio") and j != 1:
                print("j++")
                j = j+1
        except:
            continue
    if audio_url == "didnt get updated":
        delAudio(driver)
        driver.quit()
        time.sleep(2)
        print("error 225")
        os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume)
        time.sleep(2)
        pyautogui.press("volumemute")
        time.sleep(2)
        return (225,transcript)       
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(audio_url)
    pyautogui.keyDown("ctrl")
    pyautogui.press("s")
    pyautogui.keyUp("ctrl")
    time.sleep(2)
    pyautogui.write(name,interval=.1)
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(4)
    delAudio(driver)
    driver.quit()
    time.sleep(2)
    os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume)
    time.sleep(2)
    pyautogui.press("volumemute")
    time.sleep(2)
    transcript = transcript[1:-1]
    return (10,trans_out)

