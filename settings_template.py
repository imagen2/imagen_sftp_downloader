class local_settings():
    def __init__(self):
        self.remote_path = "/data/imagen/2.7" #the remote path on the sftp server
        self.local_path ="/my/local/datapath/" #your local path where the data will be downloaded
        self.log_path ="/my/local/download_logs" #give a path where logs can be saved

class dl_settings():
    def __init__(self, description, mode, time_dirs, overall_dirs, intermed_dir1, subjs, dirs, subj_files):
        self.description = description
            # string, short description what the given settings will do
            # e.g. "download available data from all timepoints and subjects for imaging/spm_first_level/.../EPI_short_MID/",
        self.mode = mode  # string, "files" or "dirs" or "subjects" or "overall"
            # the folder structure of the server is: remote_path/{time_dirs}/intermed_dirs/
            # some of the intermed_dirs (e.g. imaging/spm*) are organised as follows: remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}
            # the "mode" setting provides several ways of downloading parts of the data, using different hierarchies
            # "overall": download all directories, subdirectories and files within the given folders  remote_path/{time_dirs}/{overall_dirs}
            # "dirs": download n directories per subject within remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}
            # "files": download n files from folder remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}/{subj_files}
            #          dirs should have only one entry in this case, because files are expected to be present within each dir
            # "subjects": dowload n subject folders from: remote_path/{time_dirs}/intermed_dir/
        self.time_dirs = time_dirs
            # list of strings, example:  ["BL","FU1","FU2","FU3"]
        self.overall_dirs = overall_dirs
            # list of strings, e.g. ["dawba/", "geolocation/", "cantab/", "meta_data/", "psytools/"]
        self.intermed_dir1 = intermed_dir1
            # string, e.g. "imaging/spm_first_level"
        self.subjs = subjs
            # list of strings, e.g. ["000099616225", "000085724167"]
            # leave empty (self.subjs = [])to download all available subj-subdirectories within intermed_dir1
        self.dirs = dirs
            # list of strings, e.g. ["EPI_stop_signal/", "EPI_short_MID/"]
        self.subj_files = subj_files
            # list of strings, e.g. ["con_0006_stop_failure_-_stop_success.nii.gz",
            #                        "con_0005_stop_success_-_stop_failure.nii.gz"]
            # if mode = "dir" subj_files is ignored

dl_fMRI_MID = dl_settings(
        ## commented example
        description = "download available data from baseline of all subjects for imaging/spm_first_level/.../EPI_short_MID/, just contrast images",
        mode = "files",  # string, "files" or "dirs" or "subjects" or "overall"
            # the folder structure of the server is: remote_path/{time_dirs}/intermed_dirs/
            # some of the intermed_dirs (e.g. imaging/spm*) are organised as follows: remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}
            # the "mode" setting provides several ways of downloading parts of the data, using different hierarchies
            # "overall": download all directories, subdirectories and files within the given folders  remote_path/{time_dirs}/{overall_dirs}
            # "dirs": download n directories per subject within remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}
            # "files": download n files from folder remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}/{subj_files}
            #          Unix-style wildcards can be used
            # "subjects": download n subject folders from: remote_path/{time_dirs}/intermed_dir/
        time_dirs = ["BL"],
            # list of strings, example:  ["BL","FU1","FU2","FU3"]
        overall_dirs = [],
            # list of strings, e.g. ["dawba/", "geolocation/", "cantab/", "meta_data/", "psytools/"]
        intermed_dir1 = "imaging/spm_first_level",
            # string, e.g. "imaging/spm_first_level"
        subjs = [],
            # list of strings, e.g. ["000099616225", "000085724167"]
            # leave empty (self.subjs = [])to download all available subj-subdirectories within intermed_dir1
        dirs = ["EPI_short_MID/"],
            # list of strings, e.g. ["EPI_stop_signal/", "EPI_short_MID/"]
        subj_files = ['con*'],
        #subj_files = ["rp_nuisance_extended.txt"]
            # list of strings, e.g. ["con_0006_stop_failure_-_stop_success.nii.gz",
            #                        "con_0005_stop_success_-_stop_failure.nii.gz"]
            # UNIX-style wildcards can be used to download all matching files (e.g. ['con*','*.txt*']
            # if mode = "dir" subj_files is ignored
)

#further examples
dl_fMRI_all_FU2 = dl_settings(
        description = "download available data from all subjects at FU2 for imaging/spm_first_level/",
        mode = "subjects",
        time_dirs = ["FU2"],
        overall_dirs = [],
        intermed_dir1 = "imaging/spm_first_level",
        subjs = [],
        dirs = [],
        subj_files = []
)

dl_fMRI_Face = dl_settings(
        description = "download data of subjects 000099616225, 000085724167 from all timepoints for imaging/spm_first_level/EPI_faces",
        mode = "dirs",
        time_dirs = ["BL","FU1"],
        overall_dirs = [],
        intermed_dir1 = "imaging/spm_first_level",
        subjs = ["000099616225", "000085724167"],
        dirs = ["EPI_faces"],
        subj_files = []
)

dl_overall_data = dl_settings(
        description = "download available data from overall folders (dawba,geolocation,cantab,meta_data,psytools)",
        mode = "overall",
        time_dirs = ["BL","FU1","FU2","FU3"],
        overall_dirs = ["dawba/", "geolocation/", "cantab/", "meta_data/", "psytools/"],
        intermed_dir1 = "",
        subjs = [],
        dirs = [],
        subj_files = []
)

#put all definitions here into a list named dl_tasks, and they will be downloaded sequentially
dl_tasks = [
    dl_fMRI_MID,
    dl_overall_data
]

#dl_tasks = [
#    dl_overall_data
#]

#dl_tasks =[
#    dl_fMRI_all_FU2
#]

#dl_tasks =[
#    dl_fMRI_Face
#]