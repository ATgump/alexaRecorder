import imp
from xml.etree.ElementPath import find
import find_marker
import os
import librosa
import pickle
full_set = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_padded"
redo_set = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_s2_fix_repad"
test_set = "C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_alexa_padded"
test_noise_reduce_dump = "C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_noise_reduce"
trim_path ="C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_trimmed"
exact_trim_path = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_trimmed_exact"
redo_trim = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set2_redo_trimmed"
quiet_set_aap_padd = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_quiet_set_pad"
quiet_set_alexa_records = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_s3_quiet_ranges"
#find_marker.pad(clip="C:\\Users\\avery\\OneDrive\\Desktop\\test\\testing_tones\\ae_MSE_trial_1_candidate_0.wav",padding="C:\\Users\\avery\\OneDrive\\Desktop\\3000hz_p08_amp_p5_time.wav",export_path="C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_padded\\ae_MSE_trial_1_candidate_0.wav")

# for audio in os.listdir("C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_alexa_padded"):
#     ta,md,ma,l = find_marker.trim_time("C:\\Users\\avery\\OneDrive\\Desktop\\test\\test_tones_alexa_padded\\"+audio)
#     print(md)
#     print(ta)
#     print(ma)
#     print(l)


# bad_tones = set()
# # # Check if tone not found
# for audio in os.listdir(quiet_set_alexa_records):
#     ta,md,ma = find_marker.trim_time_data(quiet_set_alexa_records+"\\"+audio)
#     if ma == 0 or ma[2] < 2800 or ma[2] > 3200:
#         bad_tones.add(audio)
#         try:
#             print(audio+"  freq = "+str(ma[2]))
#         except:
#             print(audio+"  freq = "+str(ma))


# ## Check the tone is after a little bit of white noise

# for audio in os.listdir(quiet_set_alexa_records):
#     ta,md,ma = find_marker.trim_time_data(quiet_set_alexa_records+"\\"+audio)
#     try:
#         if (ta[0] < (.008)*70):
#             print("tone too early")
#             print(audio)
#             bad_tones.add(audio)
#             # print(librosa.get_duration(filename=full_set+"\\"+audio)-4)
#             # print(ta[0])
#         elif (ta[0]+.2 > librosa.get_duration(filename=quiet_set_alexa_records+"\\"+audio)-4):
#             print("tone too late")
#             print(audio)
#             bad_tones.add(audio)

#     except:
#         print("tone not found")
#         print(audio)
#         bad_tones.add(audio)
# print(len(bad_tones))

# with open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\needs_redo_quiet_set","wb") as f:
#     pickle.dump(bad_tones,f)

# for file in bad_tones:
#     os.remove(quiet_set_alexa_records+"\\"+file)



