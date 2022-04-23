from transcription import extract_text_vosk
import os
import pickle
fixed_tess = "C:\\Users\\avery\\Documents\\alexa_recorded_tess"
tess_dict = dict()
for folder in os.listdir(fixed_tess):
    if folder == "Actor_026" or folder == "Actor_028":
        for recording in os.listdir(fixed_tess+"\\"+folder):
            tess_dict[recording] = fixed_tess+"\\"+folder+"\\"+recording
ts,cf = extract_text_vosk(tess_dict)
with open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\confidence_ALEXA_pickle",'ab') as f:
    pickle.dump(cf,f)     
with open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\transcript_ALEXA_pickle",'ab') as f:
    pickle.dump(ts,f)  