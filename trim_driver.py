import find_marker
import os
## Old paths
# "C:\\Users\\avery\\Documents\\alexa_recorded_tones_set2_padded"
# "C:\\Users\\avery\\Documents\\alexa_recorded_tones_set2_trimmed"

clips_to_trim_path = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_s3_quiet_ranges"
trimmed_export_path = "C:\\Users\\avery\\OneDrive\\Documents\\alexa_recorded_tones_set3_quiet_trimmed"
for c in os.listdir(clips_to_trim_path):
    find_marker.trim_clip(clip_path= (clips_to_trim_path+"\\"+c), export_path= (trimmed_export_path+"\\"+c))