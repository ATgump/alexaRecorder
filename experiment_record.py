from pickletools import read_unicodestring1
from playsound import playsound
from experiment_scrape import experiment_scrape
import os
import time
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import sys
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
from sre_parse import fix_flags
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

fixed_tess_path = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess" ## For recording the trials, in case the tess is the rerecorded version
alexa_open_prompt_tones = "C:\\Users\\avery\\OneDrive\\Desktop\\echo_open_tones.wav"
alexa_open_prompt_tess = "C:\\Users\\avery\\OneDrive\\Desktop\\echoOpen.wav"
devices = [('"Speakers"',"2"),('"Headphones"',"0")] ### 0 - USB, 1- Bluetooth

def data_set_prep(import_path,export_path,name,merge = False):
    if merge == True:
        actors = os.listdir(import_path)
        for actor in actors:
            AAP_files += os.listdir(os.path.join(import_path,actor))
    else:
        AAP_files = os.listdir(import_path)
    AAP_keys = dict()
    for file in AAP_files:
        AAP_keys[file] = os.path.join(import_path,file)

    # (10s pad up front + (4s audio + 1s pad) * <audio file count>) * 10000 Hz sample rate 

    num_of_AAPS = len(AAP_files)
    big_wav_data = np.zeros(10000*(10 + (5 * num_of_AAPS)))
    indx = 100000

    for audio_key in sorted(AAP_keys.keys()):
        x, _ = librosa.load(AAP_keys[audio_key], duration=4, sr=10000)
        length = len(x)
        big_wav_data[indx:indx+length] = x
        indx += 50000
    try:
        os.mkdir(os.path.join(export_path,"padded_long"))
    except:
        pass
    ep = os.path.join(export_path,"padded_long",name)    
    sf.write(ep, big_wav_data, 10000)
    return AAP_keys


def play_audio(data,samplerate,device,rec,dur,name,usb_ep):
    if not rec: 
        sd.play(data=data,samplerate=samplerate,device=device)
    elif rec:
        recording = sd.rec(frames =(int((dur+1)*samplerate)),samplerate=samplerate, device=device,channels=1)
    sd.wait()
    if rec:
        write(filename =os.path.join(usb_ep,name),data=recording,rate=samplerate)
    return 0

def make_threads(tone_path,tess_path,name,usb_ep):
    tone,fs = librosa.load(tone_path, sr=None)
    tess,fx = librosa.load(tess_path, sr = None)
    dur = librosa.get_duration(y= tess,sr=fx)
    name = name+".wav"
    thread1 = threading.Thread(target=play_audio,kwargs = {'name':name,'rec':False,'dur':dur,'data':tess,'samplerate':fx,'device':("Headphones (Baby Boom XL), Windows DirectSound"),'usb_ep': usb_ep})
    thread2 = threading.Thread(target=play_audio, kwargs = {'name':name,'rec':False,'dur':dur,'data':tone,'samplerate':fs,'device':"Speakers (USB Audio), Windows DirectSound",'usb_ep': usb_ep})
    thread3 = threading.Thread(target=play_audio, kwargs = {'name':name,'rec':True,'data':tess,'dur':dur,'samplerate':fx,'device':"Microphone (USB audio CODEC), Windows DirectSound",'usb_ep': usb_ep})
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    return 0



def create_volume_sets(tess_import,export_path,AAPS):
    volume_sets =[]
    for AAP in AAPS:
        trial_num = "trial"+str(AAP[2])
        to_do = []
        for actor in os.listdir(os.path.join(tess_import[trial_num])):
            for audio in os.listdir(os.path.join(tess_import[trial_num],actor)):
                audio_name = trial_num+"_"+AAP[1][:-4]+"_"+AAP[0]+"_"+audio
                if audio_name not in os.listdir(os.path.join(export_path,trial_num,"Alexa")):
                    to_do.append((audio,AAP[0],AAP[1],AAP[2]))
        volume_sets.append((AAP[0],to_do))
        return volume_sets








def experiment_record(method,file_list,import_directory_TESS,import_directory_tones,export_directory):
    ## Recording tones from Alexa
    if method == "alexa_record_tones":
        for volume in file_list[1]:
            os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume)
            for audio_file in file_list[0]:
                if audio_file not in os.listdir(export_directory):
                    i = 0
                    while True:
                        audioName = volume+"_"+audio_file[:-4]
                        if (i == 10):
                            sys.exit("10 try fails")
                        try:
                            playsound(alexa_open_prompt_tones)
                            playsound(os.path.join(import_directory_tones,audio_file))
                        except:
                            print("file: "+audio_file+" couldnt be played.")
                            break
                        time.sleep(20)
                        try:
                            code,transcript = experiment_scrape(scrape_type="index",index = 1, name=audioName,export_path=export_directory)
                            if (code == 225):
                                i = i+1
                                continue
                            elif (code == 10):
                                recoding_audio= sf.SoundFile(export_directory+"\\"+audio_file)
                                length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                                recoding_audio.close()
                                if (4 - length_of_recorder) > 0 or (4-length_of_recorder) < -2:
                                    os.remove(export_directory+"\\"+audio_file)
                                    i = i+1
                                    continue
                                break
                        except:
                            print("scraper didnt return 225 exception line 41")
                            i=i+1
                            continue

    ## Recording TESS from Alexa
    # File_list = (files[],volume)
    elif method == "alexa_record_tess":
        os.system('C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume '+file_list[1]+' "Headphones" 0')
        for audio_file in file_list[0]:
            i = 0
            actor = audio_file[-7:-4]
            if audio_file not in os.listdir(export_directory):
                while True:
                    audioName = audio_file[:-4]
                    if (i == 10):
                        break
                    try:
                        playsound(alexa_open_prompt_tess)
                        playsound(os.path.join(import_directory_TESS,actor,audio_file))
                    except:
                        print("file: "+audio_file+" couldnt be played.")
                        break
                    time.sleep(20)
                    try:
                        code,transcript = experiment_scrape(scrape_type = "TESS", name = audioName, export_path=export_directory)
                        if (code == 225):
                            i = i+1
                            continue
                        elif (code == 10):
                            tess_audio = sf.SoundFile(os.path.join(import_directory_TESS,actor,audio_file))
                            recoding_audio= sf.SoundFile(os.path.join(export_directory,audio_file))
                            length_of_tess = tess_audio.frames/tess_audio.samplerate
                            length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                            tess_audio.close()
                            recoding_audio.close()
                            if (length_of_tess - length_of_recorder) > .75:
                                os.remove(export_directory+"\\"+audioName+".wav")
                                continue
                            with open (os.path.join(export_directory,"Transcripts",(audioName+".txt")),'w') as f:
                                f.write(transcript)
                            break
                    except:
                        print("sraper didnt return 225 exception line 41")
                        i=i+1
                        continue
    
    ## Recording from the USB mic    
    elif method == "USB_record_TESS" or method == "USB_record_tones":
        time.sleep(30)
        n = method+"_padded_long"
        if method == "USB_record_TESS":
            AAP_k = data_set_prep(import_directory_TESS, export_directory,n,merge=True)
        else:
            AAP_k = data_set_prep(import_directory_tones, export_directory,n)
        long_aap,fs = librosa.load(os.path.join(export_directory,"padded_long",n), sr=10000)
        os.mkdir(export_directory,"long_records")
        os.mkdir(export_directory,"")
        for volume in file_list:
            os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume+' "Speakers" '+"2")
            if method == "USB_record_tones":
                sd.default.device = ("Microphone (USB audio CODEC), Windows DirectSound","Speakers (USB Audio), Windows DirectSound")
            else:
                sd.default.device = ("Microphone (USB audio CODEC), Windows DirectSound","Headphones (Baby Boom XL), Windows DirectSound")
            myrecording = sd.playrec(long_aap, samplerate=fs, channels=1)
            sd.wait()  # Wait until recording is finished
            p = os.path.join(export_directory,"long_records",(volume+"_padded_long.wav"))
            write(p, fs, myrecording)  # Save as WAV file 
            os.mkdir(export_directory,"individual_AAPS",volume)

        # Split the files
        for AAPS in os.listdir(os.path.join(export_directory,"long_records")):
            starting_index = 100000
            x, _ = librosa.load(os.path.join(os.path.join(export_directory,"long_records"),AAPS), sr=10000)
            # Write the recorded files into a new directory

            dest = os.path.join(export_directory,"individual_AAPS",volume)
            # Parse them out; key is filename with no path info
            indx = starting_index
            for audio_key in sorted(AAP_k.keys()):
                data = x[indx:indx+40000]
                indx = indx + 50000
                sf.write(os.path.join(dest, audio_key), data, 10000)
##########################################################################################################
## File list is a list of tuples in this case [(volume,tone,trial)]
## import_directory_tess is multiple tess directories for different trials dicts d["trial1"] = trial 1 import directory

    elif method == "eval_record":
        os.system('C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume 64226 "Headphones" 0')
        for trial in file_list:
            trial_num = "trial"+str(trial[2])
            try:
                os.makedirs(os.path.join(export_directory,trial_num,"USB"))
                os.makedirs(os.path.join(export_directory,trial_num,"Alexa","transcripts"))
            except:
                pass
        volume_sets = create_volume_sets(import_directory_TESS,export_directory,file_list)
        for volume_set in volume_sets:
            #print("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume_set[0]+" "+devices[0][0]+" "+devices[0][1])
            os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume_set[0]+" "+devices[0][0]+" "+devices[0][1])
            time.sleep(2)
            new_export = os.path.join(export_directory,("trial"+str(volume_set[1][0][3])))
            alexa_export_path = os.path.join(new_export,"Alexa")
            usb_mic_export_path = os.path.join(new_export,"USB")
            transcript_folder = os.path.join(alexa_export_path,"transcripts")
            for combo in volume_set[1]:
                i = 0
                audio_file = combo[0]
                actor = "Actor_" + combo[0][-7:-4]
                while True:
                    audio_name = "trial"+str(combo[3])+"_"+combo[2][:-4]+"_"+combo[1]+"_"+audio_file[:-4]
                    if(i == 10):
                        break

                    ## TRY THIS METHOD FIRST (BETTER TRIM ON FILES)
                    if(i<5):
                        try:
                            d,f = librosa.load(alexa_open_prompt_tess,sr=None)
                            sd.play(data = d, samplerate= f,device = "Speakers (USB Audio), Windows DirectSound")
                            sd.wait()
                            make_threads(name= audio_name,tone_path=os.path.join(import_directory_tones,combo[2]), tess_path=os.path.join(fixed_tess_path,actor,combo[0]), usb_ep=usb_mic_export_path)
                        except:
                            print("file: "+audio_file+" couldnt be played.")
                            break
                        time.sleep(20)
                        try:
                            code,transcript = experiment_scrape(name = audio_name, export_path=alexa_export_path,scrape_type="TESS")
                            if (code == 225):
                                i = i+1
                                continue
                            elif (code == 10):
                                tess_audio = sf.SoundFile(os.path.join(fixed_tess_path,actor,audio_file))
                                recoding_audio= sf.SoundFile(os.path.join(alexa_export_path,audio_name+".wav"))
                                length_of_tess = tess_audio.frames/tess_audio.samplerate
                                length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                                tess_audio.close()
                                recoding_audio.close()
                                if (length_of_tess - length_of_recorder) > .75:
                                    i = i+1
                                    os.remove(os.path.join(alexa_export_path,audio_name+".wav"))
                                    os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                                    continue
                                with open(os.path.join(transcript_folder,audio_name+".txt"),'w') as f:
                                    f.write(transcript)
                                break
                        except:
                            print("scraper didnt return 225 - some other exception")
                            i=i+1
                            try:
                                os.remove(os.path.join(alexa_export_path,audio_name+".wav"))
                                os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                            except:
                                pass
                            continue
                        
                    ### IF FIRST RECORD METHOD FAILS FOR SOME REASON
                    elif(i >= 5):
                        try:
                            d,f = librosa.load(alexa_open_prompt_tones)
                            sd.play(data = d, samplerate= f,device = "Speakers (USB Audio), Windows DirectSound")
                            sd.wait()
                            make_threads(name= audio_name,tone_path=os.path.join(import_directory_tones,combo[2]), tess_path=os.path.join(fixed_tess_path,actor,combo[0]),usb_ep=usb_mic_export_path)
                        except:
                            print("file: "+audio_file+" couldnt be played.")
                            break
                        time.sleep(20)
                        try:
                            code,transcript =  experiment_scrape(name = audio_name, export_path=alexa_export_path,scrape_type="index")
                            if (code == 225):
                                i = i+1
                                continue
                            elif (code == 10):
                                try:
                                    recoding_audio = sf.SoundFile(os.path.join(alexa_export_path,audio_name+".wav"))
                                except:
                                    i = i+1
                                    os.remove(os.path.join(alexa_export_path,audio_name+".wav"))
                                    os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                                    continue
                                if recoding_audio.samplerate > 0:
                                    length_of_recorder = recoding_audio.frames/recoding_audio.samplerate
                                else:
                                    length_of_recorder = 0
                                recoding_audio.close()
                                if (4.035 - length_of_recorder) > 0 or (4-length_of_recorder) < -2:
                                    os.remove(os.path.join(alexa_export_path,audio_name+".wav"))
                                    os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                                    i = i+1
                                    continue
                                break
                        except:
                            print("scraper didnt return 225 exception line 41")
                            i=i+1
                            try:
                                os.remove(os.path.join(alexa_export_path,audio_name+".wav"))
                                os.remove(os.path.join(usb_mic_export_path,audio_name+".wav"))
                            except:
                                pass
                            continue


