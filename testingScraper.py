from lib2to3.pgen2 import driver
from wsgiref import headers
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.chrome.service import Service
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

def scrapeAudio(direc, name):
    history_url = "https://www.amazon.com/"
    service_object = Service(binary_path)
    driver = webdriver.Chrome(service=service_object)
    driver.get("https://www.amazon.com/alexa-privacy/apd/rvh?")
    ids = driver.find_elements(value='//*[@id]')
    for ii in ids:
        print(ii.tag_name)
        #print (ii.get_attribute('id'))
    #html_resp = getHTMLdocument(history_url)
    #soup = BeautifulSoup(html_resp, 'html.parser')
    #print(soup.prettify())
    return 0

scrapeAudio("abc","dfg")