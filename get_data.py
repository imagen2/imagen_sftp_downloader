import pysftp
import os
import traceback

from secret import login_credentials # secret login info in separate file
# alternatively: enter here
# class login_credentials():
#     def __init__(self):
#         self.host = "imagen2.cea.fr"
#         self.user = "myusername"
#         self.pswd = "mypassword"

def make_dir(local_path):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
        print("directory created: " +local_path)

lc = login_credentials()
remote_path = "/data/imagen/2.7"
local_path ="/Users/martin/Projects/datasets/IMAGEN/neurospin"
make_dir(local_path)

time_dirs = ["BL","FU1"]
# time_dirs = ["BL","FU1","FU2","FU3"]

#mode = "dirs"   # "files" or "dirs" or "subjects"
mode = "subjects"   # "files" or "dirs" or "subjects" or "overall"
# "overall": all directories, subdirectories and files within a folder remote_path/{time_dirs}/{overall_dirs}
overall_dirs = ["dawba/", "geolocation/","cantab/", "meta_data/", "psytools/"]
# "dirs": n directories per subject are downloaded remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}
# "files": one file per subject is downloaded: remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}/{subj_files}
intermed_dir1 = "imaging/spm_first_level"
subjs = ["000099616225","000085724167"]
dirs = ["EPI_stop_signal/","EPI_short_MID/"]
# if mode = "dir" subj_files is ignored
# if dir2 has more than 1 element and mode="files" subj_files are expected in each directory
subj_files =["con_0006_stop_failure_-_stop_success.nii.gz",
             "con_0005_stop_success_-_stop_failure.nii.gz"]




with pysftp.Connection(host=lc.host, username=lc.user, password=lc.pswd) as sftp:
    print("Connection successfully established ... ")
    for td in time_dirs:
        if mode == "overall":
            print("downloading complete folders (one folder containing data of many subjects)")
            try:
                base_remote_dir = os.path.join(remote_path, td)
                sftp.chdir(base_remote_dir)
                local_dir = os.path.join(local_path, td)
                make_dir(local_dir)
                for o_dir in overall_dirs:
                    print("remote dir:" + os.path.join(base_remote_dir, o_dir))
                    print("local dir:" + os.path.join(local_dir, o_dir))
                    try:
                        sftp.get_r(o_dir, local_dir)
                        print("overall folder download successful!")
                    except:
                        print("overall folder download not successful!")
                        traceback.print_exc(limit=1)

            except:
                print("problem with directory " + base_remote_dir)
                traceback.print_exc(limit=1)
        else:
            try:
                base_remote_dir = os.path.join(remote_path, td, intermed_dir1)
                sftp.chdir(base_remote_dir)
                for subj in subjs:
                    if mode == "subjects":
                        local_dir = os.path.join(local_path, td, intermed_dir1)
                        make_dir(local_dir)
                        print("remote dir:" + os.path.join(base_remote_dir, subj))
                        print("local dir:" + os.path.join(local_dir,subj))
                        try:
                            sftp.get_r(subj, local_dir)
                            print("recursive subject download successful!")
                        except:
                            print("subject download not successful!")
                            traceback.print_exc(limit=1)
                    else:
                        try:
                            base_remote_dir =  os.path.join(remote_path, td, intermed_dir1, subj)
                            sftp.chdir(base_remote_dir)
                            local_dir = os.path.join(local_path, td, intermed_dir1, subj)
                            make_dir(local_dir)
                            for dir2 in dirs:
                                if mode == "dirs":
                                    #l_path = os.path.join(local_path, td, intermed_dir1, subj, dir2)
                                    #make_dir(l_path)
                                    #
                                    #local_dir = os.path.join(local_path)
                                    print("remote dir:" + os.path.join(base_remote_dir,dir2))
                                    print("local dir:" + os.path.join(local_dir,dir2))
                                    try:
                                        sftp.get_r(dir2, local_dir)
                                        print("recursive folder download successful!")
                                    except:
                                        print("folder download not successful!")
                                        traceback.print_exc(limit=1)
                                if mode == "files":
                                    for subj_file in subj_files:
                                        local_dir = os.path.join(local_path, td, intermed_dir1, subj, dir2)
                                        make_dir(local_dir)
                                        dl_dir = os.path.join(remote_path, td, intermed_dir1, subj, dir2)
                                        l_path = os.path.join(local_path, td, intermed_dir1, subj, dir2)
                                        dl_file = os.path.join(dl_dir, subj_file)
                                        local_file = os.path.join(local_dir, subj_file)
                                        try:
                                            if mode == "files":
                                                print("remote file:" + dl_file)
                                                print("local file:" + local_file)
                                                sftp.get(dl_file, local_file)
                                                print("file download successful!")
                                        except:
                                            print("Download not successful!")
                                            traceback.print_exc(limit=1)
                        except:
                            print("problem with directory " + os.path.join(remote_path, td, intermed_dir1, subj))
                            traceback.print_exc(limit=1)
            except:
                print("problem with directory " + os.path.join(remote_path, td, intermed_dir1))
                traceback.print_exc(limit=1)

# connection closed automatically
print("connection closed")