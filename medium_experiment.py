from copyreg import pickle
import soundfile as sf
import os
import numpy as np
import librosa
import playsound
import pickle
import sounddevice as sd
from scipy.io.wavfile import write
import time
#    65536
#    61440
#    53248
#    45056
#    32768
# "C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery\\ae_MSE_trial_1_candidate_0.wav"
# "C:\\Users\\avery\\OneDrive\\Documents\\one_file_long_AAPs.wav"

# time.sleep(30)
# long_aap,fs = librosa.load("C:\\Users\\avery\\OneDrive\\Documents\\one_file_long_AAPs.wav", sr=10000)
# volumes = ["65536","61440","53248","45056","32768","16384","9831","3277","655"]
# for volume in volumes:
#     os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume)
#     seconds = 1210  # Duration of recording
#     sd.default.device = ("Microphone (USB audio CODEC), MME","Speakers (USB Audio), MME")
#     myrecording = sd.playrec(long_aap, samplerate=fs, channels=1)
#     sd.wait()  # Wait until recording is finished
#     write("C:\\Users\\avery\\OneDrive\\Documents\\long_aap_90_degree_alexa_medium_records\\"+volume+"_long_file.wav", fs, myrecording)  # Save as WAV file 








# # # This is how I prep a dataset to record
# AAP_files = os.listdir("C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery")
# AAP_keys = dict()
# for file in AAP_files:
#     AAP_keys[file] = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery\\"+file


# # (10s pad up front + (4s audio + 1s pad) * <audio file count>) * 10000 Hz sample rate 
# big_wav_data = np.zeros(10000*(10 + (5 * len(AAP_files))))
# indx = 100000

# for audio_key in sorted(AAP_keys.keys()):
#     x, _ = librosa.load(AAP_keys[audio_key], duration=4, sr=10000)
#     length = len(x)
#     big_wav_data[indx:indx+length] = x
#     indx += 50000
    
# sf.write("C:\\Users\\avery\\OneDrive\\Documents\\one_file_long_AAPs.wav", big_wav_data, 10000)
# with open ("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\AAP_keys.p","wb") as f:
#     pickle.dump(AAP_keys,f)

# f = open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\AAP_keys.p","rb")
# AAP_keys = pickle.load(f)

# #["65536","61440","53248","45056","32768","16384","9831","3277","655"]

# for AAPS in os.listdir("C:\\Users\\avery\\OneDrive\\Documents\\long_aap_90_degree_alexa_medium_records"):
#     starting_index = 100000
#     x, _ = librosa.load("C:\\Users\\avery\\OneDrive\\Documents\\long_aap_90_degree_alexa_medium_records\\"+AAPS, sr=10000)
#     # Write the recorded files into a new directory
#     volume = ""
#     for c in AAPS:
#         if c == "_":
#             break
#         else:
#             volume = volume + c
#     dest = "C:\\Users\\avery\\OneDrive\\Documents\\long_aap_alex_med_cut\\"+volume
#     os.mkdir(dest)
#     # Parse them out; key is filename with no path info
#     indx = starting_index
#     for audio_key in sorted(AAP_keys.keys()):
#         data = x[indx:indx+40000]
#         indx = indx + 50000
#         sf.write(os.path.join(dest, audio_key), data, 10000)

# f.close()
