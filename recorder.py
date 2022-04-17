from playsound import playsound
import os
import time
from scrape import scraper
tess_path = 'C:/Users/avery/OneDrive/Desktop/TessAudio/TESS_Toronto_emotional_speech_set_data/OAF_angry/'

tess_folder = os.listdir(tess_path)
i = 0
#s = scraper
alexa_open_prompt = "C:/Users/avery/OneDrive/Desktop/alexaOpen.mp3"
for filename in tess_folder:
    playsound(alexa_open_prompt)
    p = tess_path+filename
    playsound(p)
    #s.scrapeAudio("PATH",filename)
    time.sleep(5)
    i = i+1
    if i == 20:
        break