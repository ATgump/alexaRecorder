# Path to recording of "hey alexa"
#alexa_open_prompt_tess_alexa = "C:\\Users\\avery\\OneDrive\\Desktop\\echoOpen.wav"
#alexa_open_prompt_tess_dot = 
hey_alexa_path = "C:\\Users\\avery\\OneDrive\\Desktop\\echoOpen_no_skill.wav"

##### Shouldn't need to cange after this

# Imports
import sys
import librosa
import sounddevice as sd
import numpy as np

# CHeck the arguments
if len(sys.argv) <= 1:
    print(f'usage {sys.argv[0]} <audio 1>')
else:
    aap_filename = sys.argv[1]
    
    x0, _ = librosa.load(hey_alexa_path, sr=10000)
    x1, _ = librosa.load(aap_filename, sr=10000)
    
    playme = np.zeros(len(x0) + len(x1) +5000)
    playme[0:len(x0)] = x0
    playme[len(x0)+5000:] = x1
    
    sd.play(playme, samplerate=10000)
    sd.wait()