
from cmath import exp
import librosa
import sounddevice as sd
import time
import soundfile as sf
import os
from scipy.io.wavfile import write
from experiment_record import  experiment_record,data_set_prep
#from listener import  experiment_record

#time.sleep(15)
# fixed_tess = "C:\\Users\\avery\\OneDrive\\Documents\\tess_to_record.wav"
# export_path = "C:\\Users\\avery\\OneDrive\\Documents\\different_distances_TESS_USB_recorded\\1feet"
# #n = "test1"+"_padded_long.wav"
# #data_set_prep(fixed_tess, export_path,n,merge=True)
# #experiment_record(method = "USB_record_TESS", import_directory_TESS=fixed_tess,import_directory_tones="",export_directory=export_path,file_list=["64226"])
# AAPs = "C:\\Users\\avery\\OneDrive\\Documents\\new_aap_multidist"
# volumes = ["65536","61440","53248","45056","32768","16384","9831","3277","655"]
# export_directory = "C:\\Users\\avery\\OneDrive\\Documents\\new_aap_multidist_recordings"
# #experiment_record(method = "USB_record_tones",file_list= volumes, import_directory_TESS="",import_directory_tones=AAPs,export_directory= ed)
# AAP_keys = dict()
# AAP_files = []
# num_of_AAPS = 0
# AAP_files = os.listdir(AAPs)
# num_of_AAPS = len(AAP_files)
# for file in AAP_files:
#     AAP_keys[file] = os.path.join(AAPs,file)

# for AAPS in os.listdir(os.path.join(export_directory,"long_records")):
#     starting_index = 100000
#     x, _ = librosa.load(os.path.join(export_directory,"long_records",AAPS), sr=10000)
#     # Write the recorded files into a new directory
#     volume = ""
#     for char in AAPS:
#         if char == "_":
#             break
#         volume += char
#     print(volume)
#     os.makedirs(os.path.join(export_directory,"individual_AAPS",volume),exist_ok=True)
#     dest = os.path.join(export_directory,"individual_AAPS",volume)
#     # Parse them out; key is filename with no path info
#     indx = starting_index
#     for audio_key in sorted(AAP_keys.keys()):
#         data = x[indx:indx+40000]
#         indx = indx + 50000
#         sf.write(os.path.join(dest, audio_key), data, 10000)

# long_aap,fs = librosa.load(fixed_tess,sr=None)

# sd.default.device = ("Microphone (USB audio CODEC), Windows DirectSound","Headphones (Baby Boom XL), Windows DirectSound")
# myrecording = sd.playrec(long_aap, samplerate=fs, channels=1)

# sd.wait()  # Wait until recording is finished
# p = os.path.join(export_path,"1feet_recording_USB.wav")
# write(p, fs, myrecording)  # Save as WAV file






#trial3_trial2_ae_MSE-FFT_individual_14_655_003-001-005-001-159-001-028


time.sleep(20)




# trial_1_tess = "C:\\Users\\avery\\OneDrive\\Documents\\trial1"
# trial_2_tess = "C:\\Users\\avery\\OneDrive\\Documents\\trial2"
# trial_3_tess = "C:\\Users\\avery\\OneDrive\\Documents\\trial3"
#export_path1 = "C:\\Users\\avery\\OneDrive\\Documents\\trial_1_eval_different_distances\\2feet"
#export_path2 = "C:\\Users\\avery\\OneDrive\\Documents\\trial_1_eval_different_distances\\3feet"
#export_path = "C:\\Users\\avery\\OneDrive\\Documents\\echo_dot_evals\\5feet"
#export_path = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_evals\\9feet"

#export_path = "C:\\Users\\avery\\OneDrive\\Documents\\automated_AAP_evals\\dot\\1feet"
export_path = r"C:\Users\avery\OneDrive\Documents\eval_different_angles\9feet\6"
#export_path = "C:\\Users\\avery\\OneDrive\\Documents\\new_aap_multidist_evals\\alexa_evals\\1feet"
#export_path = "C:\\Users\\avery\\OneDrive\\Documents\\new_aap_multidist_evals\\alexa_evals\\2feet"

tess_imports = dict()

# Trial 1 AAP  655 trial_0_individual_13_ae_MSE-FFT
# Trial 2 AAP  655 trial_1_individual_15_ae_MSE-FFT
# Trial 3 AAP  655 trial2_ae_MSE-FFT_individual_14.wav
AAPS_to_test = [("655","ae_PURE_trial_1_candidate_6.wav",1)]
AAP_path = r"C:\Users\avery\OneDrive\Documents"
#AAP_path = "C:\\Users\\avery\\OneDrive\\Documents\\avery_new_ae"
#AAP_path = "C:\\Users\\avery\\OneDrive\\Documents\\trial3_aaps"

trial_1_angles_tess = r"C:\Users\avery\OneDrive\Documents\trial_different_angles"
#AAP_path = "C:\\Users\\avery\\OneDrive\\Documents\\new_aap_multidist"
#AAPS_to_test = [("655","trial0_ae_MSE-FFT_individual_18.wav",1)]
#tess_imports["trial1"] = trial_1_tess
#tess_imports["trial2"] = trial_2_tess
#tess_imports["trial3"] = trial_3_tess
tess_imports["trial1"] = trial_1_angles_tess

experiment_record(method = "eval_record_dot", import_directory_TESS=tess_imports,import_directory_tones=AAP_path,export_directory=export_path,file_list=AAPS_to_test)

#fixed_tess_path = "C:\\Users\\avery\\OneDrive\\Documents\\fixed_tess\\fixed_tess"

#export_path = r"C:\Users\avery\OneDrive\Documents\DB_test"

#data_set_prep(import_path=fixed_tess_path,export_path=export_path,name="DB_test_no_pads_TESS.wav",merge=True,DB_expir=True)
#experiment_record(method = "USB_record_DB",import_directory_TESS="",import_directory_tones="",export_directory=export_path,file_list="",dbTestName="DB_recording_9feet.wav")
