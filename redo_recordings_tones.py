from playsound import playsound
import os
import time
import soundfile as sf
from scraper_tones import scrapeAudio
import pickle
import sys
audio_data_path = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_redo_pad"
alexa_open_prompt = "C:\\Users\\avery\\OneDrive\\Desktop\\echo_open_tones_loud.wav"
quiet_set_aap_padd = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_quiet_set_pad"
to_redo = []
volumes = ["16384","9831","3277","655"]

# for volume in volumes:
#     for aaps in os.listdir(quiet_set_aap_padd):
#         to_redo.append(volume+"_"+aaps)
# for done in os.listdir("C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_s3_quiet_ranges"):
#     to_redo.remove(done)


with open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\needs_redo_quiet_set","rb") as f:
    to_redo=pickle.load(f)

# for done in os.listdir("C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_s3_quiet_ranges"):
#     to_redo.remove(done)
print(len(to_redo))
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
    skipped = False
    while True:
        if (i == 3):
            with open ("C:\\Users\\avery\\OneDrive\\Desktop\\TONES_REDO_SKIPPED.txt",'a+') as f:
                f.write(file+"\n")
            skipped = True
            break
        if file.startswith("9831"):
            volume = file[:4]
            name = file[5:]
        elif file.startswith("16384"):
            volume = file[:5]
            name = file[6:]
        elif file.startswith("3277"):
            volume = file[:4]
            name = file[5:]
        elif file.startswith("655"):
            volume = file[:3]
            name = file[4:]
        os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+str(volume))
        time.sleep(4)
        playsound(alexa_open_prompt)
        playsound(quiet_set_aap_padd+"\\"+name)
        time.sleep(20)
        try:
            code,transcript = scrapeAudio(file,volume)
            if (code == 225):
                i = i+1
                continue
            elif (code == 10):
                try:
                    recoding_audio= sf.SoundFile("C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_s3_quiet_ranges"+"\\"+file)
                except:
                    i = i+1
                    os.remove("C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_s3_quiet_ranges"+"\\"+file)
                    continue
                if recoding_audio.samplerate > 0:
                    length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                else:
                    length_of_recorder = 0
                recoding_audio.close()
                print("exception below here")
                if (4.035 - length_of_recorder) > 0 or (4-length_of_recorder) < -2:
                    i = i+1
                    os.remove("C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_s3_quiet_ranges"+"\\"+file)
                    continue
                break
        except:
            print("scraper didnt return 225 exception line 41")
            i = i+1
            try:
                os.remove(quiet_set_aap_padd+"\\"+name)
            except:
                pass
            continue
    if not skipped:
        with open ("C:\\Users\\avery\\OneDrive\\Desktop\\TONES_REDO_COMPLETED.txt",'a+') as f:
            f.write(file+"\n")
            