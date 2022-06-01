from playsound import playsound
import os
import time
import soundfile as sf
from scraper_tones import scrapeAudio_tones
import pickle
import sounddevice as sd
import sys
from scrape import scrapeAudio
import threading
import librosa
from scipy.io.wavfile import write
AAP_path = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery"
fixed_tess_path = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess"
devices = [('"Speakers"',"2"),('"Headphones"',"0")] ### 0 - USB, 1- Bluetooth
AAPS_to_test = [("655","ae_PURE_trial_3_candidate_8.wav"),("9831","ae_MSE_trial_3_candidate_5.wav"),("655","ae_MSE-FFT_trial_3_candidate_3.wav")]
alexa_open_prompt_tone_skill = "C:\\Users\\avery\\OneDrive\\Desktop\\echo_open_tones.wav"
alexa_open_prompt_tess_skill = "C:\\Users\\avery\\OneDrive\\Desktop\\echoOpen.wav"
#export_path = "C:\\Users\\avery\\OneDrive\\Documents\\acoustic_experiment_alexa_recordings"
transcript_folder = "C:\\Users\\avery\\OneDrive\\Documents\\acoustic_experiment_alexa_recordings\\Transcripts"
usb_mic_export_path = "C:\\Users\\avery\\OneDrive\\Documents\\acoustic_experiment_USB_recordings"
export_path = "C:\\Users\\avery\\OneDrive\\Documents\\eval_two_autoE_trained\\Alexa"
AAPS_to_test = [("655","trial_0_individual_13_ae_MSE-FFT.wav",1)]
trial_1_tess = "C:\\Users\\avery\\OneDrive\\Documents\\trial1"

volume_sets =[]
for AAP in AAPS_to_test:
    to_do = []
    if AAP[2] == 1:
        for actor in os.listdir(trial_1_tess):
            for audio in os.listdir(os.path.join(trial_1_tess,actor)):
                audio_name = "trial1_"+AAP[1][:-4]+"_"+AAP[0]+"_"+audio
                #if audio_name not in os.listdir(export_path):
                to_do.append((audio,AAP[0],AAP[1],AAP[2]))
    # elif AAP[2] == 2:
    #     for actor in os.listdir(trial_2_tess):
    #         for audio in os.listdir(os.path.join(trial_2_tess,actor)):
    #             audio_name = "trial2_"+AAP[1][:-4]+"_"+AAP[0]+"_"+audio
    #             if audio_name not in os.listdir(export_path):
    #                 to_do.append((audio,AAP[0],AAP[1],AAP[2]))
    volume_sets.append((AAP[0],to_do))

names = []
for vs in volume_sets:
    for combo in vs[1]:
        audio_file = combo[0]
        names.append("trial1_"+combo[2][:-4]+"_"+combo[1]+"_"+audio_file)


for file in os.listdir(export_path):
    if file not in names:
        print(file)
for file in names:
    if file not in os.listdir(export_path):
        print(file)

print(names[:1])
print(len(names))

# all_combos = []
# for AAP in AAPS_to_test:
#     to_do = []
#     for actor in os.listdir(fixed_tess_path):
#         for audio in os.listdir(os.path.join(fixed_tess_path,actor)):
#             audio_name = AAP[1][:-4]+"_"+AAP[0]+"_"+audio
#             all_combos.append(audio_name)

# print(len(all_combos))

#print(len(os.listdir(export_path)))
# to_rem = []
# for file in os.listdir(export_path):
#     if file not in all_combos and file != "Transcripts":
#         #to_rem.append(file)
#         print(file)

# for file in all_combos:
#     if file not in os.listdir(export_path):
#         print(file)

# print(to_rem)

# for d in to_rem:
#     os.remove(os.path.join(export_path,d))
    




# volume_sets =[]
# for AAP in AAPS_to_test:
#     to_do = []
#     for actor in os.listdir(fixed_tess_path):
#         for audio in os.listdir(os.path.join(fixed_tess_path,actor)):
#             audio_name = AAP[1][:-4]+"_"+AAP[0]+"_"+audio
#             if audio_name not in os.listdir(export_path):
#                 to_do.append((audio,AAP[0],AAP[1]))
#     volume_sets.append((AAP[0],to_do))




# # for file in os.listdir(usb_mic_export_path):
# #     if file not in os.listdir(export_path):
# #         os.remove(os.path.join(usb_mic_export_path,file))


# volume_sets =[]
# for AAP in AAPS_to_test:
#     to_do = []
#     for actor in os.listdir(fixed_tess_path):
#         for audio in os.listdir(os.path.join(fixed_tess_path,actor)):
#             #print(len(os.listdir(os.path.join(fixed_tess_path,actor))))
#             audio_name = AAP[1][:-4]+"_"+AAP[0]+"_"+audio
#             to_do.append(AAP[1][:-4]+"_"+AAP[0]+"_"+audio[:-4]+".txt")
#     volume_sets.append((to_do))
# # actor = "Actor_" + (volume_sets[0][1].pop())[0][-7:-4]
# #print(volume_sets)

# i = 0
# j = 0

# start_remove = False
# while j < len(volume_sets):
#     while i < len(volume_sets[j]):
#         if (volume_sets[j][i] == "ae_MSE_trial_3_candidate_5_9831_003-001-004-001-155-001-026.txt"):
#             start_remove = True
#         if start_remove == True:
#             # try:
#             #     os.remove(os.path.join(export_path,volume_sets[j][i]))
#             # except:
#             #     pass
#             # try:
#             #     os.remove(os.path.join(usb_mic_export_path,volume_sets[j][i]))
#             # except:
#             #     pass
#             try:
#                 os.remove(os.path.join(export_path,"Transcripts",volume_sets[j][i]))
#             except:
#                 pass
#         i = i+1
#     j = j+1

# #print(volume_sets[0][0])
# # print(len(volume_sets))
# # print(actor)