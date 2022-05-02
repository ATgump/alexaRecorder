import find_marker
import os
padd="C:\\Users\\avery\\OneDrive\\Desktop\\3000hz_p02_amp_p5_time.wav"
ep="C:\\Users\\avery\\OneDrive\\Documents\\padded_aaps_for_avery"
aap_set = "C:\\Users\\avery\\OneDrive\\Documents\\aaps_for_avery"
for aap in os.listdir(aap_set):
    find_marker.pad(export_path= (ep+"\\"+aap),padding= padd,clip= (aap_set+"\\"+aap))