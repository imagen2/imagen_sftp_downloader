import pysftp
import os
import traceback
import logging
from datetime import datetime

from secret import login_credentials # secret login info in separate file
#from settings import local_settings # local settings info in separate file

from settings import *
# alternatively: enter here
# class login_credentials():
#     def __init__(self):
#         self.host = "imagen2.cea.fr"
#         self.user = "myusername"
#         self.pswd = "mypassword"

##### functions
def setup_logger(name, log_file, level):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    if level >= logging.INFO:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def make_dir(local_path):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
        log_it("directory created: " +local_path, logging.INFO)

def log_it(msg,level):
    for lg in logger:
        lg.log(level,msg)

now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#logging.basicConfig(filename='get_data'+now_str+'.log', level=logging.WARNING)
#logging.basicConfig(filename='get_data'+now_str+'.log', level=logging.WARNING)

# construct to separate loggers for debugging and warning
logger_info = [{"name":'info_logger',"level":logging.INFO},
          {"name":'debug_logger',"level":logging.DEBUG}]
logger=[]
for li in logger_info:
    logger.append(setup_logger(li["name"], li["name"]+'_get_data_'+now_str+'.log', li["level"]))

# info_logger = setup_logger('info_logger', 'info_get_data_'+now_str+'.log', logging.INFO)
# info_logger.info("###logfile for download process (info and warnings)")
# # detailed debug log
# debug_logger = setup_logger('debug_logger', 'debug_get_data_'+now_str+'.log', logging.DEBUG)
# debug_logger.info("###logfile for download process (detailled debugging log)")

lc = login_credentials()
ls = local_settings()
make_dir(ls.local_path)

with pysftp.Connection(host=lc.host, username=lc.user, password=lc.pswd) as sftp:
    log_it("Connection to " + lc.host + " successfully established ... ", logging.INFO)
    for dl_i, dl in enumerate(dl_tasks):
        try:
            log_it("working on: download setting " + str(dl_i+1) +"/" + str(len(dl_tasks))+" : " + dl.description, logging.INFO)
            for td in dl.time_dirs:
                if dl.mode == "overall":
                    log_it("downloading complete folders (one folder containing data of many subjects)", logging.INFO)
                    try:
                        base_remote_dir = os.path.join(ls.remote_path, td)
                        sftp.chdir(base_remote_dir)
                        local_dir = os.path.join(ls.local_path, td)
                        make_dir(local_dir)
                        for o_dir in dl.overall_dirs:
                            log_it("downloading folder " + os.path.join(base_remote_dir, o_dir) +
                                   " --> " + os.path.join(local_dir, o_dir), logging.INFO)
                            try:
                                sftp.get_r(o_dir, local_dir)
                                log_it("overall folder download successful!",logging.INFO)
                            except:
                                log_it("overall folder download not successful!", logging.WARN)
                                exc_str = traceback.format_exc(limit=1)
                                log_it(exc_str, logging.DEBUG)

                    except:
                        log_it("problem with directory " + base_remote_dir, logging.WARN)
                        exc_str = traceback.format_exc(limit=1)
                        log_it(exc_str, logging.DEBUG)
                else:
                    try:
                        base_remote_dir = os.path.join(ls.remote_path, td, dl.intermed_dir1)
                        if sftp.exists(base_remote_dir):
                            sftp.chdir(base_remote_dir)




                            if len(dl.subjs) == 0:
                                log_it("getting available subjects from folder " + base_remote_dir, logging.INFO)
                                subjs = sftp.listdir()
                                log_it("downloading " + str(len(subjs)) + " subject directories from " + base_remote_dir, logging.INFO)
                            else:
                                subjs = dl.subjs
                            for subj in subjs:
                                if dl.mode == "subjects":
                                    local_dir = os.path.join(ls.local_path, td, dl.intermed_dir1)
                                    make_dir(local_dir)
                                    log_it("downloading folder " + os.path.join(base_remote_dir, subj) +
                                          " --> " + os.path.join(local_dir,subj), logging.INFO)
                                    try:
                                        if sftp.exists(subj) == True:
                                            sftp.get_r(subj, local_dir)
                                            log_it("recursive subject download successful! (subject " +subj + ")", logging.INFO)
                                        else:
                                            log_it(os.path.join(base_remote_dir,subj) + " does not exist on " + lc.host,
                                                       logging.WARN)
                                    except:
                                        log_it("subject download not successful! (subject " +subj + ")", logging.WARNING)
                                        exc_str = traceback.format_exc(limit=1)
                                        log_it(exc_str, logging.DEBUG)
                                        #traceback.print_exc(limit=1)
                                else:
                                    try:
                                        base_remote_dir =  os.path.join(ls.remote_path, td, dl.intermed_dir1, subj)
                                        sftp.chdir(base_remote_dir)
                                        local_dir = os.path.join(ls.local_path, td, dl.intermed_dir1, subj)
                                        make_dir(local_dir)
                                        for dir2 in dl.dirs:
                                            if dl.mode == "dirs":
                                                #l_path = os.path.join(dl.local_path, td, dl.intermed_dir1, subj, dir2)
                                                #make_dir(l_path)
                                                #
                                                #local_dir = os.path.join(dl.local_path)
                                                log_it("downloading folder " + os.path.join(base_remote_dir,dir2) +
                                                       " --> " + os.path.join(local_dir,dir2), logging.INFO)
                                                try:
                                                    if sftp.exists(dir2) == True:
                                                        sftp.get_r(dir2, local_dir)
                                                        log_it(
                                                            "recursive subject download successful! (subject " + subj + ")",
                                                            logging.INFO)
                                                    else:
                                                        log_it(os.path.join(base_remote_dir,
                                                                            dir2) + " does not exist on " + lc.host,
                                                               logging.WARN)
                                                except:
                                                    log_it("folder download not successful!", logging.WARN)
                                                    exc_str = traceback.format_exc(limit=1)
                                                    log_it(exc_str, logging.DEBUG)
                                            if dl.mode == "files":
                                                for subj_file in dl.subj_files:
                                                    local_dir = os.path.join(ls.local_path, td, dl.intermed_dir1, subj, dir2)
                                                    make_dir(local_dir)
                                                    dl_dir = os.path.join(ls.remote_path, td, dl.intermed_dir1, subj, dir2)
                                                    l_path = os.path.join(ls.local_path, td, dl.intermed_dir1, subj, dir2)
                                                    dl_file = os.path.join(dl_dir, subj_file)
                                                    local_file = os.path.join(local_dir, subj_file)
                                                    try:
                                                        if dl.mode == "files":
                                                            log_it("downloading file " + dl_file +
                                                                   " --> " + local_file, logging.INFO)
                                                            #print("remote file:" + dl_file)
                                                            #print("local file:" + local_file)
                                                            sftp.get(dl_file, local_file)
                                                            log_it("file download successful!", logging.INFO)
                                                    except:
                                                        log_it("Download not successful!",logging.WARN)
                                                        exc_str = traceback.format_exc(limit=1)
                                                        log_it(exc_str, logging.DEBUG)
                                    except:
                                        log_it("problem with directory " + os.path.join(ls.remote_path, td, dl.intermed_dir1, subj),logging.WARN)
                                        exc_str = traceback.format_exc(limit=1)
                                        log_it(exc_str, logging.DEBUG)

                        else:
                            log_it(base_remote_dir + " does not exist on " + lc.host,
                                                   logging.WARN)
                    except:
                        log_it("problem with directory " + os.path.join(ls.remote_path, td, dl.intermed_dir1), logging.WARN)
                        exc_str = traceback.format_exc(limit=1)
                        log_it(exc_str, logging.DEBUG)
        except:
            log_it("CAUTION: download setting " + str(dl_i + 1) + "/" + str(len(dl_tasks)) + " : " + dl.description + "did not finish without errors!",
                   logging.WARN)

# connection closed automatically
if sftp._sftp_live == False:
    log_it("connection closed", logging.INFO)

#close logging handlers for files to become immediately available
for lgr in logger:
    handler = lgr.handlers[0]
    lgr.removeHandler(handler)
    handler.close()