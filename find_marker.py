from ast import NodeVisitor
import scipy
import pydub
import scipy.io
import librosa
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import pandas as pd
from scipy.io import wavfile
from scipy.signal import argrelmax
from matplotlib.mlab import specgram

def pad():
    seven_five_hertz = pydub.AudioSegment.from_file("C:\\Users\\avery\\OneDrive\\Desktop\\75_hertz_half_sec.wav", format="wav")
    test_tone = pydub.AudioSegment.from_file("C:\\Users\\avery\\OneDrive\\Desktop\\testing_tones\\ae_MSE_trial_1_candidate_0.wav", format="wav")
    pad = test_tone+seven_five_hertz
    pad.export("C:\\Users\\avery\\OneDrive\\Desktop\\padded_test2.wav", format="wav")
    return 0

def trim():
    rate,data = scipy.io.wavfile.read("C:\\Users\\avery\\OneDrive\\Desktop\\padded_test2_mono.wav")
    f,t,z = scipy.signal.spectrogram(data,rate)
    ztwo = np.array(np.abs(z))
    i=0
    # f x t
    times = []
    while i < ztwo.shape[0]:
        j=0
        while j < ztwo.shape[1]:
            if f[i] > 500 and t[j] > 0 and ztwo[i][j] > 25:
                times.append(t[j])
            j = j+1
        i = i+1
    return np.min(times)




# ts =trim()
# to_trim = pydub.AudioSegment.from_file("C:\\Users\\avery\\OneDrive\\Desktop\\padded_test2_mono.wav", format="wav")
# clip = (ts*1000)+200
# to_trim = to_trim[clip:clip+4000]
# to_trim.export("C:\\Users\\avery\\OneDrive\\Desktop\\padded_test2_mono_clipped.wav", format="wav")
# print(ts)

