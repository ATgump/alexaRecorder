import playsound
import os
for i in (range(1,10)):
    os.system(r'C:\Users\avery\Downloads\nircmd\nircmd.exe setsysvolume 64226 "Speakers" '+str(i))
    

for i in (range(1,10)):
    os.system(r'C:\Users\avery\Downloads\nircmd\nircmd.exe setsysvolume 655 "Speaker" '+str(i))
    playsound.playsound(r"C:\Users\avery\OneDrive\Desktop\003-001-001-001-003-001-026.wav")
    print(i)

# for i in (range(1,10)):
#     os.system('C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume 0 "Headphones" '+str(i))

# for i in (range(1,10)):
#     os.system('C:\\Users\\avery\\Downloads\\nircmd\\nircmd.exe setsysvolume 64226 "Headphones" '+str(i))
#     playsound.playsound(r"C:\Users\avery\OneDrive\Desktop\003-001-001-001-003-001-026.wav")
#     print(i)