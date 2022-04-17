
from lxml.html import fromstring
def get_proxies():
    f = open("C:/Users/avery/OneDrive/Desktop/Python Programs/alexaAutomatedRecording/alexa_automated_recording/proxy_list.txt")
    stringRead = f.read()
    lst = stringRead.split('\n')
    f.close()
    return lst