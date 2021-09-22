# sftp_downloader

This code helps to download IMAGEN data via sftp.
You need to....
* ...have login credentials given in a file secret.py (use secret_template.py to create it.) Caution: never push the file with your login credentials to a public github repository
* ...know what you want to download, look at the folder structure

###Prerequisites
* Python 3 (tested with 3.7)
* pysftp

###How-To
The downloader assumes the following folder structure:
``remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}/{subj_files}``
The paths need to be specified in the script, e.g.
```
remote_path = "/data/imagen/2.7"
time_dirs = ["BL","FU1"]
# time_dirs = ["BL","FU1","FU2","FU3"]
intermed_dir1 = "imaging/spm_first_level"
subjs = ["000099616225","000085724167"]
dirs = ["EPI_stop_signal/","EPI_short_MID/"]
subj_files =["con_0006_stop_failure_-_stop_success.nii.gz",
             "con_0005_stop_success_-_stop_failure.nii.gz"]

```


There are three modes that help to do different things
```
mode = "dirs"   # "files" or "dirs" or "subjects"
```
1. "subjects" mode: download given subject folders recursively (including all subdirectories and files)
2. "dirs" mode: download specific subdirectories within subject folders recursively
3. "files" mode: download specific files within specific subdirectories within subject folders
    
Furthermore, with the "overall_mode" you can download folders recursively at a higher point in the folder hierarchy.
```
overall_mode = True  # or False
# directories not split by subjects:  remote_path/{time_dirs}/{overall_dirs}
overall_dirs = ["dawba/", "geolocation/","cantab/", "meta_data/", "psytools/"]
```

###ToDos
* simple switch to download all subjects in given folders that are found on the server
* better logging to check what might have gone wrong

