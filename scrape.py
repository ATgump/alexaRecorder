from ipaddress import collapse_addresses
import random
from selenium import webdriver
from selenium.webdriver.common import proxy
import pyautogui
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.chrome.service import Service
import json
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


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
    boxes = drive.find_elements_by_class_name("apd-content-box")
    for box in boxes:
            expandButton = box.find_element_by_class_name("apd-expand-toggle-button.button-clear")
            expandButton.click()
            randSleepTime(2,12)
            delBox = box.find_element_by_class_name("record-delete-banner.clickable")
            delButton = delBox.find_element_by_class_name("button-clear.apd-icon-button-round.record-delete-button")
            delButton.click()
            randSleepTime(2,12)

def scrapeAudio(name):
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("shift")
    pyautogui.press("m")
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")
    service_object = Service(binary_path)
    option = webdriver.ChromeOptions()
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    option.add_argument("user-data-dir=C:\\Users\\avery\\AppData\\Local\\Google\\Chrome\\User Data")
    option.add_argument("profile-directory=Profile 1")
    option.add_experimental_option("detach",True)
    driver = webdriver.Chrome(service=service_object,options=option,desired_capabilities=capabilities)
    driver.get("https://www.amazon.com/alexa-privacy/apd/rvh?")
    randSleepTime(2,12)
    boxes = driver.find_elements_by_class_name("apd-content-box")
    for box in boxes:
        try:
            transcript = box.find_element_by_class_name("record-summary-preview.customer-transcript").text
            if transcript.startswith('"say') or transcript.startswith('"kids') or transcript.startswith('"dogs'):
                expandButton = box.find_element_by_class_name("apd-expand-toggle-button.button-clear")
                expandButton.click()
                randSleepTime(2,12)
                recBox = box.find_element_by_class_name("record-item")
                recButton = recBox.find_element_by_class_name("apd-icon-button-round.play-audio-button.button-clear.fa.fa-play-circle")
                recButton.click()
                randSleepTime(2,12)
                perf = driver.get_log("performance")
                events = process_browser_logs_for_network_events(perf)
                audio_url = "didnt get updated"
                for event in events:
                    try:
                        tt = event["params"]["request"]["url"]
                        if tt.startswith("https://www.amazon.com/alexa-privacy/apd/rvh/audio?uid"):
                            audio_url = tt
                    except:
                        continue
                collapse_button = box.find_element_by_class_name("apd-expand-toggle-button.button-clear.fa.fa-chevron-up")
                collapse_button.click()
                randSleepTime(2,12)
        except:
            continue
            
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(audio_url)
    pyautogui.keyDown("ctrl")
    pyautogui.press("s")
    pyautogui.keyUp("ctrl")
    time.sleep(2)
    pyautogui.write(name,interval=.25)
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(4)
    delAudio(driver)
    driver.close()
    driver.quit()
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("shift")
    pyautogui.press("m")
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")
    return 0
