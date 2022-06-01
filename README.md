# How to Use:
experiment_record(method,file_list,import_directory_TESS,import_directory_tones,export_directory)
the parameters will depend on the method

Disregard all other files, just haven't deleted yet all that you need is the 'experiment_record.py' file.
!ONLY WORKS FOR WINDOWS!
nircmd is a requirment (download here: https://nircmd.nirsoft.net/)
Run pip install -r requirements.txt (Python 2), or pip3 install -r requirements.txt (Python 3) to download the other dependencies (some setup may be required for pydub you need ffmpeg - https://stackoverflow.com/questions/53480893/pydub-installation-and-ffmpeg)

Things still to do:
    1. Get this working for linux system using amixer instead of nircmd
    2. remove unecessary requirments
    3. Cleanup scraper (redundant code here still)
    4. update alexa_record_tones to include recording for tones with a marker (files needed for this in find_marker.py)
## Method: alexa_record_tones
    1. method: "alexa_record_tones"
    2. file list: (tone_files[], volume[]) record all tone files at every volume (files are just filenames not paths)
    3. import_directory_TESS: NONE
    4. import_directory_tones: directory to the tones that you want to record
    5. export directory: directory for exporting
## Method: alexa_record_TESS
    1. method: "alexa_record_TESS"
    2. file_list: (files[],volume) record all the TESS files at a single volume, the file list contains tess files to record (again not paths)
    3. import_directory_TESS:  directory to the TESS that you want to record
    4. import_directory_tones: None
    5. export directory: directory for exporting
## Method: USB_record_TESS
    1. method: "USB_record_TESS"
    2. file_list: volumes[], in this case the file_list is just a volume_list (all the files in the import directories get recorded)
    3. import_directory_TESS:  directory to the TESS that you want to record (all files in this directory will be recorded)
    4. import_directory_tones: directory to the tones that you want to record (all files in this directory will be recorded)
    5. export directory: directory for exporting
## Method: USB_record_tones
    1. method: "USB_record_tones"
    2. file_list: volumes[], in this case the file_list is just a volume_list (all the files in the import directories get recorded)
    3. import_directory_TESS:  directory to the TESS that you want to record (all files in this directory will be recorded)
    4. import_directory_tones: directory to the tones that you want to record (all files in this directory will be recorded)
    5. export directory: directory for exporting

## Method: eval_record
    1. method: "eval_record"
    2. file_list: [(string,string,int)] -> [(volume,tone,trial#)], tone is just name not pathh 
    3. import_directory_TESS: dict where d["trial#"] = path to tess Trial subset
    4. import_directory_tones: directory to the tones that you want to record (only 1 directory here, the new AAPS, if this changes will update such that it is the same as the TESS imports where d[tone] = tone path)
    5. export directory: directory for exporting
