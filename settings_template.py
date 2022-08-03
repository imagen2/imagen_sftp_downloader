class local_settings():
    def __init__(self):
        self.remote_path = "/data/imagen/2.7" #the remote path on the sftp server
        self.local_path ="/my/local/datapath/" #your local path where the data will be downloaded
        self.time_dirs = ["BL", "FU1"]
        # time_dirs = ["BL","FU1","FU2","FU3"]

        # mode = "dirs"   # "files" or "dirs" or "subjects"
        self.mode = "subjects"  # "files" or "dirs" or "subjects" or "overall"
        # "overall": all directories, subdirectories and files within a folder remote_path/{time_dirs}/{overall_dirs}
        self.overall_dirs = ["dawba/", "geolocation/", "cantab/", "meta_data/", "psytools/"]
        # "dirs": n directories per subject are downloaded remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}
        # "files": one file per subject is downloaded: remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}/{subj_files}
        self.intermed_dir1 = "imaging/spm_first_level"
        self.subjs = ["000099616225", "000085724167"]
        self.dirs = ["EPI_stop_signal/", "EPI_short_MID/"]
        # if mode = "dir" subj_files is ignored
        # if dir2 has more than 1 element and mode="files" subj_files are expected in each directory
        self.subj_files = ["con_0006_stop_failure_-_stop_success.nii.gz",
                      "con_0005_stop_success_-_stop_failure.nii.gz"]