from pickletools import read_unicodestring1
from playsound import playsound
import os
import time
import soundfile as sf
from scrape import scrapeAudio
import sys
audio_data_path = "C:\\Users\\avery\\Documents\\fixed_tess"
experiment_audio_folder = os.listdir(audio_data_path)
alexa_open_prompt = "C:\\Users\\avery\\OneDrive\\Desktop\\echoOpen.mp3"
for data_folder in experiment_audio_folder:
    try:
        os.mkdir("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+data_folder+"_Transcripts")
    except:
        pass
    for audio_file in os.listdir(audio_data_path+"\\"+data_folder):
        i = 0
        while True:
            audioName = audio_file[:-4]
            if (i == 10):
                sys.exit("10 try fails")
            try:
                playsound(alexa_open_prompt)
                playsound(audio_data_path+"\\"+data_folder+"\\"+audio_file)
            except:
                print("file: "+audio_file+" couldnt be played was deleted.")
                with open ("C:\\Users\\avery\\OneDrive\\Desktop\\CORRUPTED FILES.txt",'a+') as f:
                    f.write("\n"+audioName)
            time.sleep(20)
            try:
                code,transcript = scrapeAudio(audioName)
                if (code == 225):
                    i = i+1
                    continue
                elif (code == 10):
                    tess_audio = sf.SoundFile(audio_data_path+"\\"+data_folder+"\\"+audio_file)
                    recoding_audio= sf.SoundFile("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+audioName+".wav")
                    length_of_tess = tess_audio.frames/tess_audio.samplerate
                    length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                    tess_audio.close()
                    recoding_audio.close()
                    if (length_of_tess - length_of_recorder) > .75:
                        os.remove("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+audioName+".wav")
                        continue
                    with open ("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+data_folder+"_Transcripts\\"+audioName+".txt",'w') as f:
                        f.write(transcript)
                    break
            except:
                print("sraper didnt return 225 exception line 41")
                i=i+1
                try:
                    os.remove("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+audioName+".wav")
                except:
                    pass
                continue
        with open ("C:\\Users\\avery\\OneDrive\\Desktop\\FOLDERS_COMPLETED.txt",'a+') as f:
            f.write(audioName+"\n")
    # os.mkdir("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+data_folder)
    # for file in os.listdir("C:\\Users\\avery\\Documents\\alexa_recorded_tess"):
    #     if not file.startswith("Actor"):
    #         os.replace("C:\\Users\\avery\\Documents\\alexa_recorded_tess" + "\\" + file,"C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+data_folder+"\\"+file)
    with open ("C:\\Users\\avery\\OneDrive\\Desktop\\FOLDERS_COMPLETED.txt",'a+') as f:
        f.write("\t\t"+data_folder+"\n")