from transcription import valid_transcript_tess
import pickle
#conf_file = open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\confidence_fixed_pickle",'rb')
#trans_file = open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\transcript_fixed_pickle",'rb')

conf_file = open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\confidence_ALEXA_pickle",'rb')
trans_file = open("C:\\Users\\avery\\OneDrive\\Desktop\\Python Programs\\alexaAutomatedRecording\\alexa_automated_recording\\transcript_ALEXA_pickle",'rb')
confidences = pickle.load(conf_file)
transcripts = pickle.load(trans_file)

conf_file.close()
trans_file.close()

sum = 0
for key in confidences.keys():
    cf = confidences[key]
    ts = transcripts[key]
    valid_transcript = valid_transcript_tess(ts,cf)
    if valid_transcript:
        sum = sum
    if not valid_transcript:
        sum = sum + 1
print("MSE LOSS = "+str((1/len(confidences)*sum)))