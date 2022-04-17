from lib2to3.pgen2 import driver
from random import randint
from wsgiref import headers
from selenium import webdriver
from selenium.webdriver.common import proxy
import requests
from bs4 import BeautifulSoup
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.chrome.service import Service
import json
import random
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


def scrapeAudio(direc, name):
    history_url = "https://www.amazon.com/"
    service_object = Service(binary_path)
    option = webdriver.ChromeOptions()
    ## Create new profile if you want to have other browser windows open
    option.add_argument("user-data-dir=C:\\Users\\avery\\AppData\\Local\\Google\\Chrome\\User Data")
    option.add_experimental_option("detach",True)
    driver = webdriver.Chrome(service=service_object,options=option)
    driver.get("https://www.amazon.com/alexa-privacy/apd/rvh?")
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