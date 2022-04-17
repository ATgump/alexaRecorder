import selenium
import requests
from bs4 import BeautifulSoup
    # function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)  
    # response will be provided in JSON format
    return response.text


class scraper():
    def scrapeAudio(direc, name):
        history_url = "https://www.amazon.com/alexa-privacy/apd/rvh?"
        html_resp = getHTMLdocument(history_url)
        soup = BeautifulSoup(html_resp, 'html.parser')
        print(soup.prettify)
        return 0