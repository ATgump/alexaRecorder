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
#transcript_folder = "C:\\Users\\avery\\OneDrive\\Documents\\acoustic_experiment_alexa_recordings\\Transcripts"
transcript_folder = "C:\\Users\\avery\\OneDrive\\Documents\\new_trials_5_20_22\\Alexa - Recordings\\Transcripts"
#usb_mic_export_path = "C:\\Users\\avery\\OneDrive\\Documents\\acoustic_experiment_USB_recordings"
export_path = "C:\\Users\\avery\\OneDrive\\Documents\\new_trials_5_20_22\\Alexa - Recordings"
usb_mic_export_path= "C:\\Users\\avery\\OneDrive\\Documents\\new_trials_5_20_22\\USB - Recordings"

volume_sets =[]
for AAP in AAPS_to_test:
    to_do = []
    for actor in os.listdir(fixed_tess_path):
        for audio in os.listdir(os.path.join(fixed_tess_path,actor)):
            audio_name = AAP[1][:-4]+"_"+AAP[0]+"_"+audio
            if audio_name not in os.listdir(export_path):
                to_do.append((audio,AAP[0],AAP[1]))
    volume_sets.append((AAP[0],to_do))








def play_audio(data,samplerate,device,rec,dur,name):
    if not rec: 
        sd.play(data=data,samplerate=samplerate,device=device)
    elif rec:
        recording = sd.rec(frames =(int((dur+1)*samplerate)),samplerate=samplerate, device=device,channels=1)
    sd.wait()
    if rec:
        write(filename =os.path.join(usb_mic_export_path,name),data=recording,rate=samplerate)
    return 0

def make_threads(tone_path,tess_path,name):
    tone,fs = librosa.load(tone_path, sr=None)
    tess,fx = librosa.load(tess_path, sr = None)
    dur = librosa.get_duration(y= tess,sr=fx)
    name = name+".wav"
    thread1 = threading.Thread(target=play_audio,kwargs = {'name':name,'rec':False,'dur':dur,'data':tess,'samplerate':fx,'device':("Headphones (Baby Boom XL), Windows DirectSound")})
    thread2 = threading.Thread(target=play_audio, kwargs = {'name':name,'rec':False,'dur':dur,'data':tone,'samplerate':fs,'device':"Speakers (USB Audio), Windows DirectSound"})
    thread3 = threading.Thread(target=play_audio, kwargs = {'name':name,'rec':True,'data':tess,'dur':dur,'samplerate':fx,'device':"Microphone (USB audio CODEC), Windows DirectSound"})
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    return 0


os.system('C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume 64226 "Headphones" 0')
for volume_set in volume_sets:
    os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume_set[0]+" "+devices[0][0]+" "+devices[0][1])
    time.sleep(2)
    for combo in volume_set[1]:
        i = 0
        audio_file = combo[0]
        skipped = False
        actor = "Actor_" + combo[0][-7:-4]
        while True:
            audio_name = combo[2][:-4]+"_"+combo[1]+"_"+audio_file[:-4]
            if(i == 10):
                with open("C:\\Users\\avery\\OneDrive\\Desktop\\ACOUSTIC_FILES_SKIPPED.txt",'a+') as f:
                    f.write(audio_name+"\n")
                skipped = True
                break

            ## TRY THIS METHOD FIRST (BETTER TRIM ON FILES)
            if(i<5):
                try:
                    d,f = librosa.load(alexa_open_prompt_tess_skill,sr=None)
                    sd.play(data = d, samplerate= f,device = "Speakers (USB Audio), Windows DirectSound")
                    sd.wait()
                    make_threads(name= audio_name,tone_path=os.path.join(AAP_path,combo[2]), tess_path=os.path.join(fixed_tess_path,actor,combo[0]))
                except:
                    print("file: "+audio_file+" couldnt be played was deleted.")
                    #os.remove(os.path.join(fixed_tess_path,actor,audio_file))
                    with open("C:\\Users\\avery\\OneDrive\\Desktop\\CORRUPTED FILES ACOUSTIC.txt",'a+') as f:
                        f.write("\n"+audio_file)
                    break
                time.sleep(20)
                try:
                    code,transcript = scrapeAudio(audio_name)
                    if (code == 225):
                        i = i+1
                        continue
                    elif (code == 10):
                        tess_audio = sf.SoundFile(os.path.join(fixed_tess_path,actor,audio_file))
                        recoding_audio= sf.SoundFile(os.path.join(export_path,audio_name+".wav"))
                        length_of_tess = tess_audio.frames/tess_audio.samplerate
                        length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                        tess_audio.close()
                        recoding_audio.close()
                        if (length_of_tess - length_of_recorder) > .75:
                            i = i+1
                            os.remove(os.path.join(export_path,audio_name+".wav"))
                            os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                            continue
                        print(3)
                        with open(os.path.join(transcript_folder,audio_name+".txt"),'w') as f:
                            f.write(transcript)
                        break
                except:
                    print("scraper didnt return 225 exception line 41")
                    i=i+1
                    try:
                        os.remove(os.path.join(export_path,audio_name+".wav"))
                        os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                    except:
                        pass
                    continue
            
            
            
            ### IF FIRST RECORD METHOD FAILS FOR SOME REASON
            elif(i >= 5):
                try:
                    d,f = librosa.load(alexa_open_prompt_tone_skill)
                    sd.play(data = d, samplerate= f,device = "Speakers (USB Audio), Windows DirectSound")
                    sd.wait()
                    make_threads(name= audio_name,tone_path=os.path.join(AAP_path,combo[2]), tess_path=os.path.join(fixed_tess_path,actor,combo[0]))
                except:
                    print("file: "+audio_file+" couldnt be played was deleted.")
                    #os.remove(os.path.join(fixed_tess_path,actor,audio_file))
                    with open("C:\\Users\\avery\\OneDrive\\Desktop\\CORRUPTED FILES ACOUSTIC.txt",'a+') as f:
                        f.write("\n"+audio_file)
                    break
                time.sleep(20)
                try:
                    code,transcript = scrapeAudio_tones(audio_name)
                    if (code == 225):
                        i = i+1
                        continue
                    elif (code == 10):
                        try:
                            recoding_audio= sf.SoundFile(os.path.join(export_path,audio_name+".wav"))
                        except:
                            i = i+1
                            os.remove(os.path.join(export_path,audio_name+".wav"))
                            os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                            continue
                        if recoding_audio.samplerate > 0:
                            length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                        else:
                            length_of_recorder = 0
                        recoding_audio.close()
                        if (4.035 - length_of_recorder) > 0 or (4-length_of_recorder) < -2:
                            os.remove(os.path.join(export_path,audio_name+".wav"))
                            os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                            i = i+1
                            continue
                        break
                except:
                    print("scraper didnt return 225 exception line 41")
                    i=i+1
                    try:
                        os.remove(os.path.join(export_path,audio_name+".wav"))
                        os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                    except:
                        pass
                    continue
        if not skipped:
            with open("C:\\Users\\avery\\OneDrive\\Desktop\\ACOUSTIC_FILES_COMPLETED.txt",'a+') as f:
                f.write(audio_name+"\n")

















# for AAP in AAPS_to_test:
#     os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+AAP[0]+" "+devices[0][0]+" "+devices[0][1])
#     time.sleep(2)
#     for actor in os.listdir(fixed_tess_path):
#         for audio_file in os.listdir(os.path.join(fixed_tess_path,actor)):
#             i = 0
#             skipped = False
#             while True:
#                 audio_name = AAP[1][:-4]+"_"+AAP[0]+"_"+audio_file[:-4]
#                 if(i == 10):
#                     with open("C:\\Users\\avery\\OneDrive\\Desktop\\ACOUSTIC_FILES_SKIPPED.txt",'a+') as f:
#                         f.write(audio_name+"\n")
#                     skipped = True
#                     break

#                 ## TRY THIS METHOD FIRST (BETTER TRIM ON FILES)
#                 if(i<5):
#                     try:
#                         d,f = librosa.load(alexa_open_prompt_tess_skill,sr=None)
#                         sd.play(data = d, samplerate= f)
#                         sd.wait()
#                         make_threads(name= audio_name,tone_path=os.path.join(AAP_path,AAP[1]), tess_path=os.path.join(fixed_tess_path,actor,audio_file))
#                     except:
#                         print("file: "+audio_file+" couldnt be played was deleted.")
#                         #os.remove(os.path.join(fixed_tess_path,actor,audio_file))
#                         with open("C:\\Users\\avery\\OneDrive\\Desktop\\CORRUPTED FILES ACOUSTIC.txt",'a+') as f:
#                             f.write("\n"+audio_file)
#                         break
#                     time.sleep(20)
#                     try:
#                         code,transcript = scrapeAudio(audio_name)
#                         if (code == 225):
#                             i = i+1
#                             continue
#                         elif (code == 10):
#                             tess_audio = sf.SoundFile(os.path.join(fixed_tess_path,actor,audio_file))
#                             recoding_audio= sf.SoundFile(os.path.join(export_path,audio_name+".wav"))
#                             length_of_tess = tess_audio.frames/tess_audio.samplerate
#                             length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
#                             tess_audio.close()
#                             recoding_audio.close()
#                             if (length_of_tess - length_of_recorder) > .75:
#                                 i = i+1
#                                 os.remove(os.path.join(export_path,audio_name+".wav"))
#                                 os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
#                                 continue
#                             print(3)
#                             with open(os.path.join(transcript_folder,audio_name+".txt"),'w') as f:
#                                 f.write(transcript)
#                             break
#                     except:
#                         print("scraper didnt return 225 exception line 41")
#                         i=i+1
#                         try:
#                             os.remove(os.path.join(export_path,audio_name+".wav"))
#                             os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
#                         except:
#                             pass
#                         continue
                
                
                
#                 ### IF FIRST RECORD METHOD FAILS FOR SOME REASON
#                 elif(i >= 5):
#                     try:
#                         d,f = librosa.load(alexa_open_prompt_tone_skill)
#                         sd.play(data = d, samplerate= f)
#                         sd.wait()
#                         make_threads(name= audio_name,tone_path=os.path.join(AAP_path,AAP[1]), tess_path=os.path.join(fixed_tess_path,actor,audio_file))
#                     except:
#                         print("file: "+audio_file+" couldnt be played was deleted.")
#                         #os.remove(os.path.join(fixed_tess_path,actor,audio_file))
#                         with open("C:\\Users\\avery\\OneDrive\\Desktop\\CORRUPTED FILES ACOUSTIC.txt",'a+') as f:
#                             f.write("\n"+audio_file)
#                         break
#                     time.sleep(20)
#                     try:
#                         code,transcript = scrapeAudio_tones(audio_name)
#                         if (code == 225):
#                             i = i+1
#                             continue
#                         elif (code == 10):
#                             try:
#                                 recoding_audio= sf.SoundFile(os.path.join(export_path,audio_name+".wav"))
#                             except:
#                                 i = i+1
#                                 os.remove(os.path.join(export_path,audio_name+".wav"))
#                                 os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
#                                 continue
#                             if recoding_audio.samplerate > 0:
#                                 length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
#                             else:
#                                 length_of_recorder = 0
#                             recoding_audio.close()
#                             if (4.035 - length_of_recorder) > 0 or (4-length_of_recorder) < -2:
#                                 os.remove(os.path.join(export_path,audio_name+".wav"))
#                                 os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
#                                 i = i+1
#                                 continue
#                             break
#                     except:
#                         print("scraper didnt return 225 exception line 41")
#                         i=i+1
#                         try:
#                             os.remove(os.path.join(export_path,audio_name+".wav"))
#                             os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
#                         except:
#                             pass
#                         continue
#             if not skipped:
#                 with open("C:\\Users\\avery\\OneDrive\\Desktop\\ACOUSTIC_FILES_COMPLETED.txt",'a+') as f:
#                     f.write(audio_name+"\n")


