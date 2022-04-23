import os
recordings_path = "C:\\Users\\avery\\Documents\\alexa_recorded_tess"
fixed_tess = "C:\\Users\\avery\\Documents\\fixed_tess\\fixed_tess"
i = 0
j = 0
for folder in os.listdir(fixed_tess):
    for recording in os.listdir(fixed_tess+"\\"+folder):
        if os.path.exists(recordings_path+"\\"+folder+"\\"+recording):
            pass
        else:
            i = i+1
            print(recording)
        if os.path.exists(recordings_path+"\\"+folder+"_Transcripts\\"+recording[:-4]+".txt"):
            continue
        else:
            j = j+1
            print("TXT"+recording)
print(i)
print("\n")
print(j)