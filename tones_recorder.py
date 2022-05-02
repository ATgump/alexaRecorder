from pickletools import read_unicodestring1
from playsound import playsound
from scraper_tones import scrapeAudio
import os
import time
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import sys
# When I play these, I play at 5 different loudness using the following command to set the loudness:
#             amixer -D pulse cset name='Master Playback Volume' <VALUE>
# with the following values:
#    65536
#    61440
#    53248
#    45056
#    32768
volumes = ["65536","16384"]
audio_data_path = "C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_padded" ##TEST FOLDER
alexa_open_prompt = "C:\\Users\\avery\\OneDrive\\Desktop\\echo_open_tones.wav"
for volume in volumes:
    os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume)
    for audio_file in os.listdir(audio_data_path):
        i = 0
        while True:
            audioName = volume+"_"+audio_file[:-4]
            if (i == 10):
                sys.exit("10 try fails")
            try:
                # open_seg = AudioSegment.from_wav(alexa_open_prompt)
                # play(open_seg)
                # audio_clip = AudioSegment.from_wav(audio_data_path+"\\"+audio_file)
                # play(audio_clip)
                playsound(alexa_open_prompt)
                playsound(audio_data_path+"\\"+audio_file)
            except:
                print("file: "+audio_file+" couldnt be played was deleted.")
                os.remove(audio_data_path+"\\"+audioName+".wav")
                with open ("C:\\Users\\avery\\OneDrive\\Desktop\\CORRUPTED_FILES_TONES.txt",'a+') as f:
                    f.write("\n"+audioName)
                break
            time.sleep(20)
            try:
                code,transcript = scrapeAudio(audioName,volume)
                if (code == 225):
                    i = i+1
                    continue
                elif (code == 10):
                    recoding_audio= sf.SoundFile(audio_data_path+"\\"+audio_file)
                    length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                    recoding_audio.close()
                    if (4 - length_of_recorder) > 0 or (4-length_of_recorder) < -2:
                        os.remove(audio_data_path+"\\"+audio_file)
                        i = i+1
                        continue
                    break
            except:
                print("scraper didnt return 225 exception line 41")
                i=i+1
                try:
                    os.remove(audio_data_path+"\\"+audio_file)
                except:
                    pass
                continue
        with open ("C:\\Users\\avery\\OneDrive\\Desktop\\TONES_COMPLETED.txt",'a+') as f:
            f.write(audioName+"\n")
    with open ("C:\\Users\\avery\\OneDrive\\Desktop\\TONES_COMPLETED.txt",'a+') as f:
        f.write("\t"+volume+"\n")