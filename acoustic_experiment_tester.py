from copyreg import pickle
import soundfile as sf
import os
import numpy as np
import librosa
import playsound
import pickle
import sounddevice as sd
import threading
import multiprocessing
from scipy.io.wavfile import write
import time
import ctypes
#print(sd.check_output_settings())
test_tone = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery\\ae_MSE_trial_1_candidate_0.wav"
test_tess = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess\\Actor_026\\003-001-001-001-003-001-026.wav"
tess_fixed = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess"
export_path = "C:\\Users\\avery\\OneDrive\\Desktop\\TEST_DUAL_REC.wav"
#playsound.playsound(test_tess)



tone,fs = librosa.load(test_tone, sr=None)
tess,fx = librosa.load(test_tess, sr = None)


tess_length = librosa.get_duration(y= tess,sr =fx)
print(tess_length)
seconds = max(tess_length,4)  # Duration of recording
volume_tess = .98 * 65536


def test_play(data,samplerate,device,rec,dur):
    if not rec: 
        sd.play(data=data,samplerate=samplerate,device=device)
    elif rec:
        recording = sd.rec(frames =(int((dur+1.5)*samplerate)),samplerate=samplerate, device=device,channels=1)
    sd.wait()
    if rec:
        write(filename =export_path,data=recording,rate=samplerate)
    return 0




#     ## "Speakers" 2         <-- USB SPEAKER INDEX
#     ## "Headphones" 0       <-- BLUETOOTH

#     os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+str(65536/4)+" "+'"Speakers" '+str(2))
#     os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+str(65536/2)+' "Headphones" '+str(0))

def daemon_threading_magic():
    dur = librosa.get_duration(y= tess,sr=fx)
    #recording = sd.rec(int(dur * fx), samplerate=fx, channels=2,device="Microphone (USB audio CODEC), Windows DirectSound")

    thread1 = threading.Thread(target=test_play,kwargs = {'rec':False,'dur':dur,'data':tess,'samplerate':fx,'device':("Headphones (Baby Boom XL), Windows DirectSound")})
    thread2 = threading.Thread(target=test_play, kwargs = {'rec':False,'dur':dur,'data':tone,'samplerate':fs,'device':"Speakers (USB Audio), Windows DirectSound"})
    thread3 = threading.Thread(target=test_play, kwargs = {'rec':True,'data':tess,'dur':dur,'samplerate':fx,'device':"Microphone (USB audio CODEC), Windows DirectSound"})
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    #sd.wait()
    #librosa.output.write_wav(path =export_path,y=recording,sr=fx)
    return 0

    #thread2.join()

i = 0

while i <1:
    daemon_threading_magic()
    print(i)
    time.sleep(5)
    i = i+1




























#FIND THE INDEX

# i = 0
# for devices in sd.query_devices():
#     os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+str(65536/2)+' "Headphones" '+str(i))
#     print(i)
#     i = i+1

# # os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+str(655)+" "+'13')
# # time.sleep(2)


#     def test_play(data,samplerate,device):
#         sd.play(data=data,samplerate=samplerate,device=device)
#         sd.wait()



#     thread1 = threading.Thread(target=test_play,kwargs = {'data':tess,'samplerate':fx,'device':"Headphones (Baby Boom XL), MME"}) 
#     thread2 = threading.Thread(target=test_play, kwargs = {'data':tess,'samplerate':fx,'device':"Speakers (USB Audio), MME"})

#     #sd.play(data=tess,samplerate=fx,device="Headphones (Baby Boom XL), MME")
#     #sd.wait()
#     #test_play(tess,fx,"Headphones (Baby Boom XL), MME")
#     thread1.start()
#     #thread2.start()
#     thread1.join()
#     #thread2.join()


#     #write("C:\\Users\\avery\\OneDrive\\Desktop"+"test_two_volumes.wav", fx, )



### LONGEST LENGTH IN TESS 

# # length = 0
# # file_name = ""
# # for folder in os.listdir(tess_fixed):
# #     actors = os.path.join(tess_fixed,folder)
# #     for file in os.listdir(actors):
# #         audio_clip,sample = librosa.load(os.path.join(actors,file))
# #         if librosa.get_duration(y= audio_clip, sr = sample) > length:
# #             length = librosa.get_duration(y= audio_clip, sr = sample)
# #             file_name = file


# # print(length)
# # print(file_name)


