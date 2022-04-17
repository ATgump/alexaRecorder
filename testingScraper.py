from email.mime import audio
from lib2to3.pgen2 import driver
from random import randint
from wsgiref import headers
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common import proxy
import requests
from bs4 import BeautifulSoup
import pyautogui
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.chrome.service import Service
import json
from selenium.webdriver.common.keys import Keys
import random
import pychrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from proxiesTest import get_proxies
    # function to extract html document from given url
def getHTMLdocument(url):
    head = {
    'Host': 'www.amazon.fr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
}
    # request for HTML document of given url
    response = requests.get(url,headers=head)  
    # response will be provided in JSON format
    return response.text
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
def output_on_start(**kwargs):
    print ("STARTED", kwargs)

def output_on_end(**kwargs):
    print ("FINISHED", kwargs)

def scrapeAudio(direc, name):
    history_url = "https://www.amazon.com/"
    service_object = Service(binary_path)
    option = webdriver.ChromeOptions()
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    ## Create new profile if you want to have other browser windows open
    option.add_argument("user-data-dir=C:\\Users\\avery\\AppData\\Local\\Google\\Chrome\\User Data")
    option.add_argument("profile-directory=Profile 1")
    option.add_experimental_option("detach",True)
    #port = random.randint(10000,60000)
    #option.add_argument("--remote-debugging-port="+str(port))
    driver = webdriver.Chrome(service=service_object,options=option,desired_capabilities=capabilities)
    #dev_tools = pychrome.Browser(url = "http://localhost:"+str(port))
    driver.get("https://www.amazon.com/alexa-privacy/apd/rvh?")
    randSleepTime(2,12)
    boxes = driver.find_elements_by_class_name("apd-content-box")
    for box in boxes:
        test = box.find_element_by_class_name("record-summary-preview.customer-transcript").text
        print(test.startswith('"open'))
        print(repr(box.find_element_by_class_name("record-summary-preview.customer-transcript").text))
        #print(repr(box.find_element_by_class_name("record-summary-preview.customer-transcript").text.startswith("open")))
        if box.find_element_by_class_name("record-summary-preview.customer-transcript").text.startswith('"alexa'):
            expandButton = box.find_element_by_class_name("apd-expand-toggle-button.button-clear")
            expandButton.click()
            randSleepTime(2,12)
            delBox = box.find_element_by_class_name("record-delete-banner.clickable")
            delButton = delBox.find_element_by_class_name("button-clear.apd-icon-button-round.record-delete-button")
            delButton.click()
            randSleepTime(2,12)
        if box.find_element_by_class_name("record-summary-preview.customer-transcript").text.startswith('"open'):
            expandButton = box.find_element_by_class_name("apd-expand-toggle-button.button-clear")
            expandButton.click()
            randSleepTime(2,12)
            delBox = box.find_element_by_class_name("record-delete-banner.clickable")
            delButton = delBox.find_element_by_class_name("button-clear.apd-icon-button-round.record-delete-button")
            delButton.click()
            randSleepTime(2,12)
        else:
            expandButton = box.find_element_by_class_name("apd-expand-toggle-button.button-clear")
            expandButton.click()
            randSleepTime(2,12)
            recBox = box.find_element_by_class_name("record-item")
            recButton = recBox.find_element_by_class_name("apd-icon-button-round.play-audio-button.button-clear.fa.fa-play-circle")
            recButton.click()
            randSleepTime(2,12)
            #tab = dev_tools.list_tab()[0]
            #tab.start()
            #tab.call_method("Network.enable", _timeout=20)
            #tab.set_listener("Network.requestWillBeSent",output_on_start)
            #tab.set_listener("Network.responseRecieved",output_on_end)
            perf = driver.get_log("performance")
            events = process_browser_logs_for_network_events(perf)
            audio_url = "didnt get updated"
            for event in events:
                try:
                    #d = event["params"]["request"]["headers"]
                    #for k,v in d.items():
                        #print(k)
                    tt = event["params"]["request"]["url"]
                    if tt.startswith("https://www.amazon.com/alexa-privacy/apd/rvh/audio?uid"):
                        audio_url = tt
                except:
                    continue
            #delBox = box.find_element_by_class_name("record-delete-banner.clickable")
            #delButton = delBox.find_element_by_class_name("button-clear.apd-icon-button-round.record-delete-button")
            #delButton.click()
            #randSleepTime(2,12)
            
    print(audio_url)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(audio_url)
    #webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("s").perform()
    pyautogui.keyDown("ctrl")
    pyautogui.press("s")
    pyautogui.keyUp("ctrl")
    time.sleep(2)
    pyautogui.write("this_is_my_test_save",interval=.25)
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(100)
    driver.quit()
    time.sleep(2)
    #driver2 = webdriver.Chrome(service=service_object,options=option,desired_capabilities=capabilities)
    #driver2.get(audio_url)
    time.sleep(100)
    #driver2.quit()
    return 0
    





"""
SEEMS LIKE LOGIN NOT NECESSARY BUT THIS IS CODE FOR IT JUST IN CASE

    proxyList = get_proxies()
    randProxy = proxyList[random.randint(0,(len(proxyList)-1))]
    #option.add_argument('--proxy-server=%s' % randProxy)
    ## Will need to add your own Amazon Credentials here for UN and PW
    f = open("C:/Users/avery/OneDrive/Desktop/Python Programs/alexaAutomatedRecording/alexa_automated_recording/creds.json")
    creds = json.load(f)
    UN = creds["Username"]
    PW = creds["Password"]
    randSleepTime(5,13)
    email = driver.find_element_by_id("ap_email")
    password = driver.find_element_by_id("ap_password")
    signInButton = driver.find_element_by_id("signInSubmit")
    email.send_keys(UN)
    randSleepTime(5,12)
    password.send_keys(PW)
    randSleepTime(5,10)
    signInButton.click()


"""

    #for ii in ids:
        #print(ii.tag_name)
        #print (ii.get_attribute('id'))
    #html_resp = getHTMLdocument(history_url)
    #soup = BeautifulSoup(html_resp, 'html.parser')
    #print(soup.prettify())

scrapeAudio("abc","dfg")