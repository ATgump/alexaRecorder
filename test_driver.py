from xml.etree.ElementPath import find
import find_marker
import os
import librosa
import pickle
full_set = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_padded"
test_set = "C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_alexa_padded"
test_noise_reduce_dump = "C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_noise_reduce"
trim_path ="C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_trimmed"
exact_trim_path = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_trimmed_exact"
#find_marker.pad(clip="C:\\Users\\avery\\OneDrive\\Desktop\\test\\testing_tones\\ae_MSE_trial_1_candidate_0.wav",padding="C:\\Users\\avery\\OneDrive\\Desktop\\3000hz_p08_amp_p5_time.wav",export_path="C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_padded\\ae_MSE_trial_1_candidate_0.wav")

# for audio in os.listdir("C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_alexa_padded"):
#     ta,md,ma,l = find_marker.trim_time("C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_alexa_padded\\"+audio)
#     print(md)
#     print(ta)
#     print(ma)
#     print(l)

# # Check if tone not found
# for audio in os.listdir("C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_padded"):
#     ta,md,ma = find_marker.trim_time_data("C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_padded\\"+audio)
#     rereq = []
#     if ma == 0 or ma[2] < 2900 or ma[2] > 3100:
#         rereq.append(audio)
#         try:
#             print(audio+"  freq = "+str(ma[2]))
#         except:
#             print(audio+"  freq = "+str(ma))


# ## Check the tone is after a little bit of white noise
# for audio in os.listdir(full_set):
#     ta,md,ma = find_marker.trim_time_data(full_set+"\\"+audio)
#     if (ta[0] < (.008)*10) or (ta[0]+.4 > librosa.get_duration(filename=full_set+"\\"+audio)-4):
#         print(librosa.get_duration(filename=full_set+"\\"+audio)-4)
#         print(ta[0])

# for audio in os.listdir(full_set):
#     find_marker.trim_clip(clip_path=full_set+"\\"+audio,export_path=exact_trim_path+"\\"+audio)



##check if the clips are less than 4 secs
num_of_less_than_4 = 0
num = 0
min = (100,"")
files = []
for audio in os.listdir(trim_path):
    aud_dur = librosa.get_duration(filename=trim_path+"\\"+audio)
    if aud_dur < 4:
        files.append(audio)
        if aud_dur < min[0]:
            min = (aud_dur,audio)
        num_of_less_than_4 = num_of_less_than_4+aud_dur
        num = num+1
print(files)
print(len(files))
print(num_of_less_than_4/num)
print(num)
print(min)
# with open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\needs_redo","wb") as f:
#     pickle.dump(files,f)

# padd="C:\\Users\\avery\\OneDrive\\Desktop\\3000hz_p02_amp_p017_time.wav"
# ep="C:\\Users\\avery\\OneDrive\\Documents\\aaps_redo_pad"
# aap_set = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery"
# for file in files:
#     find_marker.pad(export_path= (ep+"\\"+file),padding= padd,clip= (aap_set+"\\"+file))




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

# for file in to_redo:
#     try:
#         os.remove(full_set+"\\"+file)
#     except:
#         pass