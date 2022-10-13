import random
from selenium import webdriver
import pyautogui
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.chrome.service import Service
import json
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


## sleep for a random time between x and y
def randSleepTime(x,y):
    n = random.randint(x,y)
    time.sleep(n)
    return 0

## return logs for network events to get audio URL for alexa recording.    
def process_browser_logs_for_network_events(logs):
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
            "Network.response" in log["method"]
            or "Network.request" in log["method"]
            or "Network.webSocket" in log["method"]
        ):
            yield log

## Delete the alexa Recordings
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


## Scraper:
    # scrape_type: type of the file that is being scraped "TESS" or "index" (index doesnt work for any index yet just for the tones)
    # name: name of the audio file to scrape
    # index: not working yet, will update index scraper to work for any index (may need to add seperate tones scraper because the index could be either 1 or 0)
def experiment_scrape(scrape_type = None,name = "", index = 0):
    ## Scrape for TESS file
    what = ""
    if scrape_type == "TESS":
        try:
            ## Setup chrome-driver settings and open alexa history page
            transcript = "audio not found"
            service_object = Service(binary_path)
            what="1"
            option = webdriver.ChromeOptions()
            what="2"
            capabilities = DesiredCapabilities.CHROME
            what="3"
            capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
            option.add_argument("user-data-dir=C:\\Users\\avery\\AppData\\Local\\Google\\Chrome\\User Data")
            option.add_argument("profile-directory=Profile 1")
            option.add_experimental_option("detach",True)
            what = "4"
            driver = webdriver.Chrome(service=service_object,options=option,desired_capabilities=capabilities)
            what="5"
            time.sleep(2)
            driver.get("https://www.amazon.com/alexa-privacy/apd/rvh?")
            time.sleep(8)

            ## mute because audio needs to be played to get URL
            pyautogui.press('volumemute')
            time.sleep(2)
            boxes = driver.find_elements_by_class_name("apd-content-box")
        except:
            print("driver failed to load history or content box not found")
            print(what)
            try:
                driver.quit()
            except:
                pass
            return 225
        audio_url = "didnt get updated"
        
        
        ## find the right element in Alexa History list (this entry will contain the audio recording we need)
        for box in boxes:
            try:
                ## Look for a transcript that begins with a word that is similar to the start of the TESS files (also the RAVDESS set)
                transcript = box.find_element_by_class_name("record-summary-preview.customer-transcript").text
                if transcript.startswith('"say') or transcript.startswith('"kids') or transcript.startswith('"dogs') or transcript.startswith('"see') or transcript.startswith('"saw') or transcript.startswith('"sew') or transcript.startswith('"seen') or transcript.startswith('"seek') or transcript.startswith('"save') or transcript.startswith('"savior') or transcript.startswith('"sap') or transcript.startswith('"sav') or transcript.startswith('"sa') or transcript.startswith('"sow') or (transcript.startswith('"so') and not transcript.startswith('"sorry')) or transcript.startswith('"play') or transcript.startswith('"hay') or transcript.startswith('"day') or transcript.startswith('"way') or transcript.startswith('"stay') or transcript.startswith('"may') or transcript.startswith('"gay') or transcript.startswith('"lay') or transcript.startswith('"ray') or transcript.startswith('"neigh') or transcript.startswith('"way') or transcript.startswith('"fae'):
                    trans_out = transcript[1:-1]
                    expandButton = box.find_element_by_class_name("apd-expand-toggle-button.button-clear")
                    expandButton.click()
                    randSleepTime(2,6)

                    ## Play the audio to get the URL from network logs
                    recBox = box.find_element_by_class_name("record-item")
                    recButton = recBox.find_element_by_class_name("apd-icon-button-round.play-audio-button.button-clear.fa.fa-play-circle")
                    recButton.click()
                    randSleepTime(2,6)
                    perf = driver.get_log("performance")

                    ## Look through network logs to find the audio URL
                    events = process_browser_logs_for_network_events(perf)
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
                    break
            except:
                continue

        ## if the audio file couldnt be scraped the audio_url wont change so return a 225 code (error with scraping)
        if audio_url == "didnt get updated":
            delAudio(driver)
            driver.quit()
            time.sleep(2)
            print("error 225")
            pyautogui.press('volumemute')
            return (225,transcript)

        ## If the audio file was found, save it to the default download location with the name provided  
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(audio_url)
        pyautogui.keyDown("ctrl")
        pyautogui.press("s")
        pyautogui.keyUp("ctrl")
        time.sleep(2)
        pyautogui.write(name,interval=.1)

        ## Close the browser window and unmute the speaker
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(4)
        delAudio(driver)
        driver.quit()
        pyautogui.press('volumemute')
        transcript = transcript[1:-1]
        return (10,trans_out)
    elif scrape_type == "index":
        try:
            ## Setup chrome-driver settings and open alexa history page
            transcript = "audio not found"
            service_object = Service(binary_path)
            option = webdriver.ChromeOptions()
            capabilities = DesiredCapabilities.CHROME
            capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
            option.add_argument("user-data-dir=C:\\Users\\avery\\AppData\\Local\\Google\\Chrome\\User Data")
            option.add_argument("profile-directory=Profile 1")
            option.add_experimental_option("detach",True)
            driver = webdriver.Chrome(service=service_object,options=option,desired_capabilities=capabilities)
            time.sleep(2)
            driver.get("https://www.amazon.com/alexa-privacy/apd/rvh?")
            time.sleep(8)

            ## mute because audio needs to be played to get URL
            pyautogui.press('volumemute')
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
        number_of_ts = 0

        ## find the right element in Alexa History list (this entry will contain the audio recording we need)
        for box in boxes:
            try:
                transcript = box.find_element_by_class_name("record-summary-preview.data-warning-message").text
                if transcript.startswith("Audio"):
                    number_of_ts = number_of_ts+1
            except:
                continue
        ## get the number of entries in the alexa history list 
        # (sometimes the "Alexa open..." doesn't get uploaded, 
        # this checks this so that the right index recording gets saved)
        if number_of_ts == 2:
            j = 0
        elif number_of_ts == 1:
            j=1

        ## Similar to above but dont use transcripts to find the right file just use the index
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
        time.sleep(2)
        pyautogui.press("volumemute")
        time.sleep(2)
        transcript = transcript[1:-1]
        return (10,trans_out)


    