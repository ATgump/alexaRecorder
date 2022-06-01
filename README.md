# How to Use:
experiment_record(method,file_list,import_directory_TESS,import_directory_tones,export_directory)
the parameters will depend on the method

## Method: alexa_record_tones
    1. method: "alexa_record_tones"
    2. file list: (tone_files[], volume[]) record all tone files at every volume (files are just filenames not paths)
    3. import_directory_TESS: NONE
    4. import_directory_tones: directory to the tones that you want to record
    5. export directory: directory for exporting
## Method: alexa_record_TESS
    1. method: "alexa_record_tones"
    2. file_list: (files[],volume) record all the TESS files at a single volume, the file list contains tess files to record (again not paths)
    3. import_directory_TESS:  directory to the tones that you want to record
    4. import_directory_tones: None
    5. export directory: directory for exporting