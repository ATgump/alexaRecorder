import playsound
import os
for i in (range(1,10)):
    os.system(r'C:\Users\avery\Downloads\nircmd\nircmd.exe setsysvolume 655 "Speakers" '+str(i))
    playsound.playsound(r"C:\Users\avery\OneDrive\Desktop\003-001-001-001-003-001-026.wav")
    print(i)
