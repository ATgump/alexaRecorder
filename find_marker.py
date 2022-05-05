from ast import NodeVisitor
import scipy
import pydub
import scipy.io
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import pandas as pd
from scipy.io import wavfile
from scipy.signal import argrelmax
from matplotlib.mlab import specgram
import tempfile

def pad(padding, clip, export_path):
    p = pydub.AudioSegment.from_file(padding, format="wav")
    c = pydub.AudioSegment.from_file(clip, format="wav")
    padd = p+c
    padd.export(export_path, format="wav")
    return 0



def trim_time(clip):
    rate,data = scipy.io.wavfile.read(clip)
    segments = int(rate*.001*10)
    overl = segments // 4
    f,t,z = scipy.signal.spectrogram(data,rate,nperseg=segments,noverlap=overl)
    ztwo = np.array(np.abs(z))
    i=0
    # f x t
    times = []
    while i < ztwo.shape[0]:
        j=0
        while j < ztwo.shape[1]:
            if f[i] > 2800 and f[i] < 3200 and ztwo[i][j] > 3000:
                times.append(t[j])
            j = j+1
        i = i+1
    return np.min(times)

# def end_silence_time(clip):
#     rate,data = scipy.io.wavfile.read(clip)
#     segments = int(rate*.001*10)
#     overl = segments // 4
#     f,t,z = scipy.signal.spectrogram(data,rate,nperseg=segments,noverlap=overl)
#     ztwo = np.array(np.abs(z))
#     i=0
#     # f x t
#     times = []
#     while i < ztwo.shape[0]:
#         j=0
#         while j < ztwo.shape[1]:
#             if ztwo[i][j] > 150000:
#                 times.append(t[j])
#             j = j+1
#         i = i+1
#     return np.max(times)





def trim_time_data(clip):
    rate,data = scipy.io.wavfile.read(clip)
    segments = int(rate*.001*10)
    overl = segments // 4
    f,t,z = scipy.signal.spectrogram(data,rate,nperseg=segments,noverlap=overl)
    ztwo = np.array(np.abs(z))
    #print(ztwo.shape)
    i=0
    md = 0
    ts = sorted(t)
    q=0
    while q < len(ts)-1:
        if ts[q+1] - ts[q] > md:
            md = ts[q+1] - ts[q]
        q=q+1

    # f x t
    times = []
    while i < ztwo.shape[0]:
        j=0
        while j < ztwo.shape[1]:
            if f[i] > 2800 and f[i] < 3200 and ztwo[i][j] > 3000:
                times.append((t[j],ztwo[i][j],f[i]))
            j = j+1
        i = i+1
    if len(times) == 0:
        return (0,0,0)
    mint = (0,0,0)
    max_amp = (0,0,0)
    mi = 10000
    #sort_times = sorted(times,key=lambda x: x[0])

    for (ti,a,fr) in times:
        if ti < mi:
            mi = ti
            mint = (ti,a,fr)
   
    for (ti,a,fr) in times:
        if a > max_amp[1] and ti == mi:
            max_amp = (ti,a,fr)
    # while True:
    #     if sort_times[i] == max_amp:
    #         found = True
    #     if found:
    #         if(sort_times[i][1] > 200000) and sort_times[i][2] != 3000:
    #             time2 = sort_times[i][0]
    #             break
    #     i = i+1
    return mint, md, max_amp#, time2

def trim_clip(clip_path, export_path):
    tt =trim_time(clip_path)
    to_trim = pydub.AudioSegment.from_file(clip_path, format="wav")
    clip = (tt*1000)+200
    # over = clip+4000 - to_trim.duration_seconds*1000
    # if over > 0:
    #     clip = clip-over
    #     to_trim = to_trim[clip:clip+4000]
    #     to_trim.export(export_path, format="wav")
        # else:
    to_trim = to_trim[clip:clip+4000]
    to_trim.export(export_path, format="wav")
    return 0

