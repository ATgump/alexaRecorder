import os
recoridngs_path = "C:\\Users\\avery\\Documents\\alexa_recorded_tess"
fixed_tess = "C:\\Users\\avery\\Documents\\fixed_tess\\Actor_026"
fixed_tess_2 = "C:\\Users\\avery\\Documents\\fixed_tess\\Actor_028"

for recording in os.listdir(recoridngs_path):
    if not recording.startswith("Actor"):
        try:
            os.remove(fixed_tess+"\\"+recording)
        except:
            try:
                os.remove(fixed_tess_2+"\\"+recording)
            except:
                pass
            continue