import soundfile as sf
import os

audio_data_path = "C:\\Users\\avery\\Documents\\alexa_recorded_tess_test"
data_folder = "Actor_026"
audio_file = "003-001-001-001-003-001-026.wav"
audioName = audio_file[:-4]
sound_file_tess = sf.SoundFile(audio_data_path+"\\"+data_folder+"\\"+audio_file)
sound_file_recording = sf.SoundFile("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+audioName+".wav")
length_of_tess = sound_file_tess.frames / sound_file_tess.samplerate
length_of_recorder = sound_file_recording.frames / sound_file_recording.samplerate
if length_of_tess - length_of_recorder > .75:
    os.remove("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+audioName)
with open ("C:\\Users\\avery\\Documents\\alexa_recorded_tess\\"+data_folder+"_Transcripts\\"+audioName+".txt",'w') as f:
    f.write("this is a test")

