import os
recordings_path = "C:\\Users\\avery\\Documents\\alexa_recorded_tess"
fixed_tess = "C:\\Users\\avery\\Documents\\fixed_tess\\fixed_tess"
for recording in os.listdir(recordings_path):
    if not recording.startswith("Actor"):
        print(recording[-5])
        if recording[-5] == '6':
            print("moved")
            os.replace("C:\\Users\\avery\\Documents\\alexa_recorded_tess" + "\\" + recording,"C:\\Users\\avery\\Documents\\alexa_recorded_tess\\Actor_026"+"\\"+recording)
        if recording[-5] == '8':
            os.replace("C:\\Users\\avery\\Documents\\alexa_recorded_tess" + "\\" + recording,"C:\\Users\\avery\\Documents\\alexa_recorded_tess\\Actor_028"+"\\"+recording)
            print("moved")
        