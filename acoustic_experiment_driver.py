from copyreg import pickle
import soundfile as sf
import os
import numpy as np
import librosa
import playsound
import pickle
import sounddevice as sd
import threading
from scipy.io.wavfile import write
import time
#    65536
#    61440
#    53248
#    45056
#    32768
test_tone = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery\\ae_MSE_trial_1_candidate_0.wav"
test_tess = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess\\Actor_026\\003-001-001-001-003-001-026.wav"
tess_fixed = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess"
# "C:\\Users\\avery\\OneDrive\\Documents\\one_file_long_AAPs.wav"

tone,fs = librosa.load(test_tone, sr=10000)
tess,fx = librosa.load(test_tess)
tess_length = librosa.get_duration(y= tess,sr =fx)

seconds = max(tess_length,4)  # Duration of recording
volume_tess = .98 * 65536




os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+"655"+" "+"Headphones (Baby Boom XL), MME")
os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+str(655)+" "+"Speakers (USB Audio), MME")
time.sleep(2)


def test_play(data,samplerate,device):
    sd.play(data=data,samplerate=samplerate,device=device)
    sd.wait()



#thread1 = threading.Thread(target=test_play,kwargs = {'data':tess,'samplerate':fx,'device':"Headphones (Baby Boom XL), MME"}) 
#thread2 = threading.Thread(target=test_play, kwargs = {'data':tone,'samplerate':fs,'device':"Speakers (USB Audio), MME"})

test_play(tess,fx,"Headphones (Baby Boom XL), MME")
#thread1.start()
#thread2.start()
#thread1.join()
#thread2.join()


#write("C:\\Users\\avery\\OneDrive\\Desktop"+"test_two_volumes.wav", fx, )





# length = 0
# file_name = ""
# for folder in os.listdir(tess_fixed):
#     actors = os.path.join(tess_fixed,folder)
#     for file in os.listdir(actors):
#         audio_clip,sample = librosa.load(os.path.join(actors,file))
#         if librosa.get_duration(y= audio_clip, sr = sample) > length:
#             length = librosa.get_duration(y= audio_clip, sr = sample)
#             file_name = file


# print(length)
# print(file_name)


