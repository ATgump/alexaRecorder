from pydub import AudioSegment
import numpy as np
import soundfile as sfile
import math
import matplotlib.pyplot as plt
import os
AudioSegment.converter = r"C:\Users\avery\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\Users\avery\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
# https://freewavesamples.com/files/Alesis-Sanctuary-QCard-Crickets.wav
#dirs =os.listdir(filename)
#print(dirs)
db_recordings_dir = r"C:\Users\avery\OneDrive\Documents\DB_test\long_records"


def convert_to_decibel(arr):
    ref = 1
    if arr!=0:
        return 20 * np.log10(abs(arr) / ref)
        
    else:
        return -60

report =""
for audio_file in os.listdir(db_recordings_dir):
    print(audio_file)
    report += f"{audio_file}:\n"
    filename = os.path.join(db_recordings_dir,audio_file)
    audio=AudioSegment.from_wav(filename)
    signal, sr = sfile.read(filename)
    samples=audio.get_array_of_samples()
    samples_sf=0
    try:
        samples_sf = signal[:, 0]  # use the first channel for dual
    except:
        samples_sf=signal  # for mono

    data=[convert_to_decibel(i) for i in samples_sf]
    percentile=np.percentile(data,[25,50,75])
    report += f"1st Quartile : {percentile[0]}\n2nd Quartile : {percentile[1]}\n3rd Quartile : {percentile[2]}\nMean : {np.mean(data)}\nMedian : {np.median(data)}\nStandard Deviation : {np.std(data)}\nVariance : {np.var(data)}\n\n\n" 
    print(f"1st Quartile : {percentile[0]}")
    print(f"2nd Quartile : {percentile[1]}")
    print(f"3rd Quartile : {percentile[2]}")
    print(f"Mean : {np.mean(data)}")
    print(f"Median : {np.median(data)}")
    print(f"Standard Deviation : {np.std(data)}")
    print(f"Variance : {np.var(data)}")

with open(os.path.join(db_recordings_dir,"report.txt"),"w+") as f:
    f.write(report)
    
# plt.figure()
# plt.subplot(3, 1, 1)
# plt.plot(samples)
# plt.xlabel('Samples')
# plt.ylabel('Data: AudioSegment')

# plt.subplot(3, 1, 2)
# plt.plot(samples_sf)
# plt.xlabel('Samples')
# plt.ylabel('Data: Soundfile')
# plt.subplot(3, 1, 3)
# plt.plot(data)
# plt.xlabel('Samples')
# plt.ylabel('dB Full Scale (dB)')
# plt.tight_layout()
# plt.show()