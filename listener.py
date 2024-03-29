# Path to AAP file to play when we hear the prompt

# Volume to play
volume = 655

#### SHouldn't need to change after this


# Prompt to listen for when deciding whether or not to play the AAP
# Did this as a regexp in case the transcription service gets wonky
prompt_regexp = r'Alexa'

# Some imports
import speech_recognition as sr
import re
from experiment_scrape import experiment_scrape
import os
import time
import soundfile as sf
import sys
import numpy as np
import librosa
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import math

fixed_tess_path = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess" ## For recording the trials, in case the tess is the rerecorded version
alexa_open_prompt_tones = "C:\\Users\\avery\\OneDrive\\Desktop\\echo_open_tones.wav"
alexa_open_prompt_tess_alexa = "C:\\Users\\avery\\OneDrive\\Desktop\\echoOpen.wav"
#alexa_open_prompt_tess_dot = "C:\\Users\\avery\\OneDrive\\Desktop\\echoOpen_no_skill.wav"
alexa_open_prompt_tess_dot = r"C:\Users\avery\OneDrive\Desktop\alexa_wake_word_dot.wav"
#devices = [('"Speakers"',"2"),('"Headphones"',"0")] ### 0 - USB, 1- Bluetooth
alexa_record_path = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recording_fixed"


## Prep the data_set for USB recordings (pad and create the dictionary to use for splitting after recording)
# merge is true if it is a TESS file and has two actor folders
def data_set_prep(import_path,export_path,name,merge = False):
	AAP_keys = dict()
	AAP_files = []
	num_of_AAPS = 0
	if merge == True:
		actors = os.listdir(import_path)
		for actor in actors:
			AAP_files.append((actor,os.listdir(os.path.join(import_path,actor))))
			num_of_AAPS += len(os.listdir(os.path.join(import_path,actor)))
		for tup in AAP_files:
			for file in tup[1]:
				AAP_keys[file] = os.path.join(import_path,tup[0],file)
	else:
		AAP_files = os.listdir(import_path)
		num_of_AAPS = len(AAP_files)
		for file in AAP_files:
			AAP_keys[file] = os.path.join(import_path,file)

	# (10s pad up front + (4s audio + 1s pad) * <audio file count>) * 10000 Hz sample rate
	#print(AAP_keys["003-001-001-001-003-001-026.wav"])
	
	### CHANGED FOR TESS ONLY
	# total_seconds = 0
	# for audio_key in sorted(AAP_keys.keys()):
	#     x,f = librosa.load(AAP_keys[audio_key],sr=24414)
	#     total_seconds += (librosa.get_duration(y=x,sr=f)+1)
	
	# big_wav_data = np.zeros(24414*(10 + math.ceil(total_seconds)))
	# indx = 24414*10
	# num_of_AAPS = len(AAP_files)
	big_wav_data = np.zeros(10000*(10 + (5 * num_of_AAPS)))
	indx = 100000
	for audio_key in sorted(AAP_keys.keys()):
		# x, f = librosa.load(AAP_keys[audio_key], sr=24414)
		# length = len(x)
		# big_wav_data[indx:indx+length] = x
		# indx += 24414*(librosa.get_duration(y=x,sr=f))
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

## Function to use for threading (plays or records a file, recording done from USB mic)
def play_audio(data,samplerate,device,rec,dur,name,usb_ep):
	if not rec: 
		sd.play(data=data,samplerate=samplerate,device=device)
	elif rec:
		recording = sd.rec(frames =(int((dur+1)*samplerate)),samplerate=samplerate, device=device,channels=1)
	sd.wait()
	if rec:
		write(filename =os.path.join(usb_ep,name),data=recording,rate=samplerate)
	return 0

## Create threads for simultaneous recording
def make_threads(tone_path,tess_path,name,usb_ep):
	tone,fs = librosa.load(tone_path, sr=None)
	tess,fx = librosa.load(tess_path, sr = None)
	dur = librosa.get_duration(y= tess,sr=fx)
	name = name+".wav"
	thread1 = threading.Thread(target=play_audio,kwargs = {'name':name,'rec':False,'dur':dur,'data':tess,'samplerate':fx,'device':("Headphones (Baby Boom XL), Windows DirectSound"),'usb_ep': usb_ep})
	thread2 = threading.Thread(target=play_audio, kwargs = {'name':name,'rec':False,'dur':dur,'data':tone,'samplerate':fs,'device':"Speakers (USB Audio), Windows DirectSound",'usb_ep': usb_ep})
	#thread3 = threading.Thread(target=play_audio, kwargs = {'name':name,'rec':True,'data':tess,'dur':dur,'samplerate':fx,'device':"Microphone (USB audio CODEC), Windows DirectSound",'usb_ep': usb_ep})
	thread1.start()
	thread2.start()
	#thread3.start()
	thread1.join()
	thread2.join()
	#thread3.join()
	return 0



def create_volume_sets(tess_import,export_path,AAPS):
	volume_sets =[]
	for AAP in AAPS:
		#print(AAP)
		trial_num = "trial"+str(AAP[2])
		to_do = []
		for actor in os.listdir(os.path.join(tess_import[trial_num])):
			for audio in os.listdir(os.path.join(tess_import[trial_num],actor)):
				audio_name = trial_num+"_"+AAP[1][:-4]+"_"+AAP[0]+"_"+audio
				if audio_name not in os.listdir(os.path.join(export_path,trial_num,"Alexa")):
					to_do.append((audio,AAP[0],AAP[1],AAP[2]))
		if to_do:
			volume_sets.append((AAP[0],to_do))
	return volume_sets








def experiment_record(method,file_list,import_directory_TESS,import_directory_tones,export_directory):
	## Recording tones from Alexa (no markers added, use find marker if it is the case that markers were added)
	## file list: (tone_files[], volume[]) record all tone files at every volume
	## method: "alexa_record_tones"
	## import_directory_TESS: NONE
	## import_directory_tones: directory to the tones that you want to record
	## export directory: directory for exporting  
	if method == "alexa_record_tones":
		for volume in file_list[1]:
			##### CHANGE TO TONES SPEAKER DEVICE INSTEAD OF DEFAULT
			os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume)
			for audio_file in file_list[0]:
				if audio_file not in os.listdir(export_directory):
					i = 0
					while True:
						audioName = volume+"_"+audio_file[:-4]
						if (i == 10):
							sys.exit("10 try fails")
						try:
							d,f = librosa.load(alexa_open_prompt_tones,sr=None)
							sd.play(data = d, samplerate= f,device = "Speakers (USB Audio), Windows DirectSound")
							sd.wait()
							d2,f2 = librosa.load(os.path.join(import_directory_tones,audio_file))
							sd.play(data = d2, samplerate = f2,device = "Speakers (USB Audio), Windows DirectSound")
							sd.wait()
						except:
							print("file: "+audio_file+" couldnt be played.")
							break
						time.sleep(20)
						try:
							code,transcript = experiment_scrape(scrape_type="index",index = 1, name=audioName)
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
								try:
									os.rename(os.path.join(alexa_record_path,audio_file),os.path.join(export_directory,audio_file))
								except:
									pass
								break
						except:
							print("scraper didnt return 225 exception line 41")
							i=i+1
							continue

	## Recording TESS from Alexa
	# File_list: (files[],volume) record all the files at a single volume, the file list contains tess files to record
	# rest same as above except a TESS import is given not a tones
	elif method == "alexa_record_tess":
		try:
			os.makedirs(export_directory,"Alexa")
			os.makedirs(export_directory,"transcripts")
		except:
			pass
		#os.system('C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume '+file_list[1]+' "Baby Boom XL\\Subunit\\Volume"')
		for audio_file in file_list[0]:
			i = 0
			actor = audio_file[-7:-4]
			if audio_file not in os.listdir(export_directory):
				while True:
					audioName = audio_file[:-4]
					if (i == 10):
						break
					try:
						d,f = librosa.load(alexa_open_prompt_tess_alexa,sr=None)
						sd.play(data = d, samplerate= f,device = "Headphones (Baby Boom XL), Windows DirectSound")
						sd.wait()
						d2,f2 = librosa.load(os.path.join(import_directory_TESS,actor,audio_file))
						sd.play(data = d2, samplerate = f2,device = "Headphones (Baby Boom XL), Windows DirectSound")
						sd.wait()
					except:
						print("file: "+audio_file+" couldnt be played.")
						break
					time.sleep(20)
					try:
						code,transcript = experiment_scrape(scrape_type = "TESS", name = audioName)
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
							with open (os.path.join(export_directory,"transcripts",(audioName+".txt")),'w') as f:
								f.write(transcript)
							try:
								os.rename(os.path.join(alexa_record_path,audio_file),os.path.join(export_directory,"Alexa",audio_file))
							except:
								pass
							break
					except:
						print("sraper didnt return 225 exception line 41")
						i=i+1
						continue
	
	## Recording from the USB mic    
	elif method == "USB_record_TESS" or method == "USB_record_tones" or method == "USB_record_PADDED":
		n = method+"_padded_long.wav"
		if method == "USB_record_TESS":
			AAP_k = data_set_prep(import_directory_TESS, export_directory,n,merge=True)
		elif method == "USB_record_tones":
			AAP_k = data_set_prep(import_directory_tones, export_directory,n)
		elif method == "USB_record_PADDED":
			AAP_k = []
		long_aap,fs = librosa.load(os.path.join(export_directory,"padded_long",n), sr=10000)
		try:
			os.mkdir(export_directory,"long_records")
		except:
			pass
		for volume in file_list:
			## CHANGE THIS TO CHANGE VOLUME FOR THE RIGHT DEVICE
			os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume)
			if method == "USB_record_tones":
				sd.default.device = ("Microphone (USB audio CODEC), Windows DirectSound","Speakers (USB Audio), Windows DirectSound")
			else:
				sd.default.device = ("Microphone (USB audio CODEC), Windows DirectSound","Headphones (Baby Boom XL), Windows DirectSound")
			myrecording = sd.playrec(long_aap, samplerate=fs, channels=1)
			sd.wait()  # Wait until recording is finished
			p = os.path.join(export_directory,"long_records",(volume+"_padded_long.wav"))
			try:
				os.makedirs(os.path.join(export_directory,"long_records"))
			except:
				pass
			write(p, fs, myrecording)  # Save as WAV file
			try: 
				os.makedirs(os.path.join(export_directory,"individual_AAPS",volume))
			except:
				pass

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

	elif method == "eval_record_alexa" or method == "eval_record_dot":
		#os.system('C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume 64226 "Baby Boom XL\\Subunit\\Volume"')
		for trial in file_list:
			trial_num = "trial"+str(trial[2])
			try:
				os.makedirs(os.path.join(export_directory,trial_num,"USB"))
				os.makedirs(os.path.join(export_directory,trial_num,"Alexa","transcripts"))
			except:
				pass
		volume_sets = create_volume_sets(import_directory_TESS,export_directory,file_list)
		#print(volume_sets)
		for volume_set in volume_sets:
			#print("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume "+volume_set[0]+' "USB Audio\\Subunit\\Speakers"')
			
			time.sleep(2)
			new_export = os.path.join(export_directory,("trial"+str(volume_set[1][0][3])))
			alexa_export_path = os.path.join(new_export,"Alexa")
			usb_mic_export_path = os.path.join(new_export,"USB")
			transcript_folder = os.path.join(alexa_export_path,"transcripts")
			missed_files = 0
			for combo in volume_set[1]:
				i = 0
				audio_file = combo[0]
				actor = "Actor_" + combo[0][-7:-4]
				while True:
					scrape_now = False
					audio_name = "trial"+str(combo[3])+"_"+combo[2][:-4]+"_"+combo[1]+"_"+audio_file[:-4]
					if(i == 3):
						missed_files = missed_files+1
						if missed_files == 5:
							sys.exit("Too many files missed reset the echo")
						break
					## TRY THIS METHOD FIRST (BETTER TRIM ON FILES)
					if(i<3):
						if method == "eval_record_alexa":
							d,f = librosa.load(alexa_open_prompt_tess_alexa,sr=None)
						elif method == "eval_record_dot":
							d,f = librosa.load(alexa_open_prompt_tess_dot,sr=None)
						#os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume 8000")	
						#sd.play(data = d, samplerate= f,device = "Headphones (Baby Boom XL), Windows DirectSound")
						
						sd.play(data = d, samplerate= f,device = "Speakers (USB Audio), Windows DirectSound")
						sd.wait()
						tp = os.path.join(fixed_tess_path,actor,combo[0])
						tess,fs = librosa.load(tp, sr=None)
						sd.play(data = tess, samplerate=fs,device = "Headphones (Baby Boom XL), Windows DirectSound")
						sd.wait()
						#os.system("C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume 655")
						# try:
						# 	#now = time.time()
						# 	text = rec.recognize_sphinx(audio)
						# 	if text == 'Echo': #not re.match(prompt_regexp, text) is not None:
						# 		#print(time.time()-now)
						# 		scrape_now = True
						# 		make_threads(name= audio_name,tone_path=os.path.join(import_directory_tones,combo[2]), tess_path=os.path.join(fixed_tess_path,actor,combo[0]), usb_ep=usb_mic_export_path)
						# 	else:
						# 		print(f"Ooops. Heard '{text}'")
						# 		continue
						# except sr.UnknownValueError:
						# 	print("Waiting...")
						# 	continue	
						time.sleep(55)
						try:
							code,transcript = experiment_scrape(name = audio_name,scrape_type="TESS")
							if (code == 225):
								i = i+1
								continue
							elif (code == 10):
								try:
									os.rename(os.path.join(alexa_record_path,(audio_name+".wav")),os.path.join(alexa_export_path,(audio_name+".wav")))
								except:
									print("failed to move file")
									pass
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
						
			