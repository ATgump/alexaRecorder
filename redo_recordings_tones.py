from playsound import playsound
import os
import time
import soundfile as sf
from scraper_tones import scrapeAudio
import pickle
import sys
audio_data_path = "C:\\Users\\avery\\OneDrive\\Documents\\padded_aaps_for_avery"
alexa_open_prompt = "C:\\Users\\avery\\OneDrive\\Desktop\\echo_open_tones.wav"
with open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\needs_redo","rb") as f:
    to_redo=pickle.load(f)

# to_redo = [
# "45056_ae_PURE_trial_3_candidate_5.wav",
# "65536_ae_MSE_trial_2_candidate_13.wav",
# "32768_ae_MSE_trial_2_candidate_12.wav",
# "45056_ae_MSE-FFT_trial_4_candidate_2.wav",
# "61440_ae_MSE-FFT_trial_1_candidate_8.wav",
# "61440_ae_MSE-FFT_trial_2_candidate_0.wav",
# "61440_ae_PURE_trial_1_candidate_12.wav",
# "65536_ae_PURE_trial_1_candidate_14.wav",
# "65536_ae_PURE_trial_3_candidate_6.wav",
# "65536_ae_PURE_trial_3_candidate_8.wav",
# ]


for file in to_redo:
    i = 0
    while True:
        if (i == 10):
            sys.exit("10 try fails")
        volume = file[:5]
        name = file[6:]
        time.sleep(2)
        os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+str(volume))
        time.sleep(2)
        playsound(alexa_open_prompt)
        playsound(audio_data_path+"\\"+name)
        time.sleep(20)
        try:
            code,transcript = scrapeAudio(file,volume)
            if (code == 225):
                i = i+1
                continue
            elif (code == 10):
                recoding_audio= sf.SoundFile(audio_data_path+"\\"+name)
                length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                recoding_audio.close()
                if (4.035 - length_of_recorder) > 0 or (4-length_of_recorder) < -2:
                    i = i+1
                    os.remove(audio_data_path+"\\"+name)
                    continue
                break
        except:
            print("scraper didnt return 225 exception line 41")
            i = i+1
            try:
                os.remove(audio_data_path+"\\"+name)
            except:
                pass
            continue