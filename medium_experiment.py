from copyreg import pickle
from hashlib import new
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
#test = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery\\ae_MSE_trial_1_candidate_0.wav"
# "C:\\Users\\avery\\OneDrive\\Documents\\one_file_long_AAPs.wav"

# auto_encoder_training_export = "C:\\Users\\avery\\OneDrive\\Documents\\auto_encoder_training_output"
# auto_encoder_training_import = "C:\\Users\\avery\\OneDrive\\Documents\\autoencoder_training_input.wav"

#new_AAPS = "C:\\Users\\avery\\OneDrive\\Documents\\avery_new_ae"
new_AAPS = "C:\\Users\\avery\\OneDrive\\Documents\\trial3_aaps"  #### EDIIITT THISS
new_padded_file = "C:\\Users\\avery\\OneDrive\\Documents\\avery_new_ae\\padded_long\\one_large_AAP(trial3).wav"
new_export_location = "C:\\Users\\avery\\OneDrive\\Documents\\avery_new_ae\\padded_long\\recordings\\trial3"

## RECORD
# time.sleep(30)
# long_aap,fs = librosa.load(new_padded_file, sr=10000)
# volumes = ["65536","61440","53248","45056","32768","16384","9831","3277","655"] #["32768","16384"]
# for volume in volumes:
#     os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume+' "Speakers" '+"2")
#     seconds = 10810  # Duration of recording
#     sd.default.device = ("Microphone (USB audio CODEC), Windows DirectSound","Speakers (USB Audio), Windows DirectSound")
#     myrecording = sd.playrec(long_aap, samplerate=fs, channels=1)
#     sd.wait()  # Wait until recording is finished
#     write(new_export_location+"\\"+volume+"_padded_long.wav", fs, myrecording)  # Save as WAV file 








# # # This is how I prep a dataset to record

# AAP_files = os.listdir(new_AAPS)
# AAP_keys = dict()
# for file in AAP_files:
#     if file != "padded_long":
#         AAP_keys[file] = os.path.join(new_AAPS,file)


# # (10s pad up front + (4s audio + 1s pad) * <audio file count>) * 10000 Hz sample rate 

# num_of_AAPS = len(AAP_files)
# big_wav_data = np.zeros(10000*(10 + (5 * num_of_AAPS)))
# indx = 100000

# #print(AAP_keys.keys())

# for audio_key in sorted(AAP_keys.keys()):
#     x, _ = librosa.load(AAP_keys[audio_key], duration=4, sr=10000)
#     length = len(x)
#     big_wav_data[indx:indx+length] = x
#     indx += 50000
# ep = os.path.join("C:\\Users\\avery\\OneDrive\\Documents\\avery_new_ae","padded_long","one_large_AAP(trial3).wav")    
# sf.write(ep, big_wav_data, 10000)
# with open ("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\AAP_keys_USB_record_three.p","wb") as f:
#     pickle.dump(AAP_keys,f)



#For parsing files out

f = open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\AAP_keys_USB_record_three.p","rb")
AAP_keys = pickle.load(f)

#["65536","61440","53248","45056","32768","16384","9831","3277","655"]



for AAPS in os.listdir(new_export_location):
    if AAPS == "individual_AAPS":
        continue
    starting_index = 100000
    x, _ = librosa.load(os.path.join(new_export_location,AAPS), sr=10000)
    # Write the recorded files into a new directory
    volume = ""
    for c in AAPS:
        if c == "_":
            break
        else:
            volume = volume + c
    dest = os.path.join(new_export_location,"individual_AAPS",volume)
    os.mkdir(dest)
    # Parse them out; key is filename with no path info
    indx = starting_index
    for audio_key in sorted(AAP_keys.keys()):
        data = x[indx:indx+40000]
        indx = indx + 50000
        sf.write(os.path.join(dest, audio_key), data, 10000)

f.close()
