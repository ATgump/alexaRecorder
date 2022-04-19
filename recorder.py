from playsound import playsound
import os
import time
from scrape import scrapeAudio
audio_data_path = "C:\\Users\\avery\\Documents\\alexaExperimentAudioFilesTEST"
start_time = time.time()
experiment_audio_folder = os.listdir(audio_data_path)
i = 0
alexa_open_prompt = "C:/Users/avery/OneDrive/Desktop/echoOpen.mp3"
for folder in experiment_audio_folder:
    """     if folder == "audio_speech_actors_01-24":
        need_name = True
    else:
        need_name = False """
    p = audio_data_path+"\\"+folder
    audio_folders = os.listdir(p)
    for data_folder in audio_folders:
        for audio_file in os.listdir(p+"\\"+data_folder):
            playsound(alexa_open_prompt)
            playsound(p+"\\"+data_folder+"\\"+audio_file)
            time.sleep(15)
            scrapeAudio(data_folder+"_"+audio_file+"_ALEXA")
end_time = time.time()
time_taken = str(end_time-start_time)
with open ("C:\\Users\\avery\\OneDrive\\Desktop\\TIME_TAKEN_TO_RUN_24.txt",'w') as f:
    f.write(time_taken)
