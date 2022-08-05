import pysftp
import os
import traceback
import logging
import fnmatch
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
        try:
            log_it("directory created: " +local_path, logging.INFO)
        except:
            pass

def log_it(msg,level):
    for lg in logger:
        lg.log(level,msg)

lc = login_credentials()
ls = local_settings()
make_dir(ls.local_path)
make_dir(ls.log_path)

now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#logging.basicConfig(filename='get_data'+now_str+'.log', level=logging.WARNING)
#logging.basicConfig(filename='get_data'+now_str+'.log', level=logging.WARNING)

# construct to separate loggers for debugging and warning
logger_info = [{"name":'info_logger',"level":logging.INFO},
          {"name":'debug_logger',"level":logging.DEBUG}]
logger=[]
for li in logger_info:
    logger.append(setup_logger(li["name"], os.path.join(ls.log_path,li["name"]+'_get_data_'+now_str+'.log'), li["level"]))

# info_logger = setup_logger('info_logger', 'info_get_data_'+now_str+'.log', logging.INFO)
# info_logger.info("###logfile for download process (info and warnings)")
# # detailed debug log
# debug_logger = setup_logger('debug_logger', 'debug_get_data_'+now_str+'.log', logging.DEBUG)
# debug_logger.info("###logfile for download process (detailled debugging log)")

try:
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
                            if sftp.exists(base_remote_dir):

                                sftp.chdir(base_remote_dir)
                                local_dir = os.path.join(ls.local_path, td)
                                make_dir(local_dir)
                                for o_dir in dl.overall_dirs:
                                    log_it("downloading folder " + os.path.join(base_remote_dir, o_dir) +
                                           " --> " + os.path.join(local_dir, o_dir), logging.INFO)
                                    try:
                                        if os.path.exists(os.path.join(local_dir,o_dir)):
                                            log_it("local folder " + local_dir +" exists, download is skipped! Check if you already have tha data, delete local folder if you want to re-download ", logging.WARN)
                                        elif not sftp.exists(o_dir):
                                            log_it(os.path.join(base_remote_dir,o_dir) + " does not exist on " + lc.host, logging.WARN)
                                        else:
                                            sftp.get_r(o_dir, local_dir)
                                            log_it("overall folder download successful!",logging.INFO)
                                    except:
                                        log_it("overall folder download not successful!", logging.WARN)
                                        exc_str = traceback.format_exc(limit=3)
                                        log_it(exc_str, logging.DEBUG)
                            else:
                                log_it(base_remote_dir + " does not exist on " + lc.host, logging.WARN)
                        except:
                            log_it("problem with directory " + base_remote_dir, logging.WARN)
                            exc_str = traceback.format_exc(limit=3)
                            log_it(exc_str, logging.DEBUG)
                    else:
                        try:
                            base_remote_dir = os.path.join(ls.remote_path, td, dl.intermed_dir1)
                            if sftp.exists(base_remote_dir):
                                sftp.chdir(base_remote_dir)
                                if len(dl.subjs) == 0:
                                    log_it("getting available subjects from folder " + base_remote_dir, logging.INFO)
                                    subjs = sftp.listdir()
                                    log_it("downloading from " + str(len(subjs)) + " subject directories in " + base_remote_dir, logging.INFO)
                                else:
                                    subjs = dl.subjs
                                for subj in subjs:
                                    if dl.mode == "subjects":
                                        local_dir = os.path.join(ls.local_path, td, dl.intermed_dir1)
                                        make_dir(local_dir)
                                        log_it("downloading folder " + os.path.join(base_remote_dir, subj) +
                                              " --> " + os.path.join(local_dir,subj), logging.INFO)
                                        try:

                                            if os.path.exists(os.path.join(local_dir, subj)):
                                                log_it("local folder " + os.path.join(local_dir, subj) + " exists, download is skipped! Check if you already have tha data, delete the local folder if you want to re-download ",
                                                    logging.WARN)
                                            elif not sftp.exists(subj):
                                                log_it(os.path.join(base_remote_dir,subj) + " does not exist on " + lc.host,
                                                           logging.WARN)
                                            else:
                                                sftp.get_r(subj, local_dir)
                                                log_it("recursive subject download successful! (subject " +subj + ")", logging.INFO)

                                        except:
                                            log_it("subject download not successful! (subject " +subj + ")", logging.WARNING)
                                            exc_str = traceback.format_exc(limit=3)
                                            log_it(exc_str, logging.DEBUG)
                                            #traceback.print_exc(limit=1)
                                    else:
                                        try:
                                            base_remote_dir =  os.path.join(ls.remote_path, td, dl.intermed_dir1, subj)
                                            try:
                                                sftp.chdir(base_remote_dir)
                                                log_it("downloading selected content from subject " + subj + " in " +
                                                       os.path.join(ls.remote_path, td, dl.intermed_dir1),
                                                       logging.INFO)
                                                local_dir = os.path.join(ls.local_path, td, dl.intermed_dir1, subj)
                                                make_dir(local_dir)
                                            except:
                                                log_it("folder " + base_remote_dir + " does not exist on " + lc.host,
                                                       logging.WARN)
                                            for dir2 in dl.dirs:
                                                if dl.mode == "dirs":
                                                    #l_path = os.path.join(dl.local_path, td, dl.intermed_dir1, subj, dir2)
                                                    #make_dir(l_path)
                                                    #
                                                    #local_dir = os.path.join(dl.local_path)
                                                    log_it("downloading folder " + os.path.join(base_remote_dir,dir2) +
                                                           " --> " + os.path.join(local_dir,dir2), logging.INFO)

                                                    if os.path.exists(os.path.join(local_dir, dir2)):
                                                        log_it(
                                                            "local folder " + os.path.join(local_dir, dir2) + " exists, download is skipped! Check if you already have tha data, delete the local folder if you want to re-download ",
                                                            logging.WARN)
                                                    elif not sftp.exists(dir2):
                                                        log_it(os.path.join(base_remote_dir, dir2) + " does not exist on " + lc.host,
                                                               logging.WARN)
                                                    else:
                                                        try:
                                                            sftp.get_r(dir2, local_dir)
                                                            log_it(
                                                                "recursive subject download successful! (directory " + dir2 + ")",
                                                                logging.INFO)
                                                        except:
                                                            log_it("folder download not successful!", logging.WARN)
                                                            exc_str = traceback.format_exc(limit=3)
                                                            log_it(exc_str, logging.DEBUG)
                                                if dl.mode == "files":
                                                    dl_dir = os.path.join(ls.remote_path, td, dl.intermed_dir1, subj, dir2)
                                                    l_path = os.path.join(ls.local_path, td, dl.intermed_dir1, subj, dir2)
                                                    if not sftp.exists(dl_dir):
                                                        log_it(dl_dir + " does not exist on " + lc.host,
                                                               logging.WARN)
                                                    else:
                                                        make_dir(l_path)
                                                        #get a list of files that satisfies either of dl.subj_files patterns
                                                        dl_file_list = set()
                                                        for subj_file in dl.subj_files:
                                                            dl_file_list.update(set(fnmatch.filter(sftp.listdir(dl_dir), subj_file)))
                                                        dl_file_list = list(dl_file_list)
                                                        log_it("attempt to download all files matching " +str(dl.subj_files) + " in folder " + dir2, logging.INFO)
                                                        for m_file in dl_file_list:
                                                            try:
                                                                dl_file = os.path.join(dl_dir,m_file)
                                                                local_file = os.path.join(l_path, m_file)
                                                                log_it("downloading files " +  dl_file +
                                                                       " --> " + local_file, logging.INFO)
                                                                #print("remote file:" + dl_file)
                                                                #print("local file:" + local_file)

                                                                if os.path.exists(local_file):
                                                                    log_it(
                                                                        "local folder " + local_file + " exists, download is skipped! Check if you already have tha data, delete the local folder if you want to re-download ",
                                                                        logging.WARN)
                                                                elif not sftp.exists(dl_file):
                                                                    log_it(dl_file + " does not exist on " + lc.host,
                                                                           logging.WARN)
                                                                else:
                                                                    try:
                                                                        sftp.get(dl_file, local_file)
                                                                        log_it(
                                                                            "file download successful!",
                                                                            logging.INFO)
                                                                    except:
                                                                        log_it("file download not successful!",
                                                                               logging.WARN)
                                                                        exc_str = traceback.format_exc(limit=3)
                                                                        log_it(exc_str, logging.DEBUG)
                                                            except:
                                                                log_it("problem downloading file!",logging.WARN)
                                                                exc_str = traceback.format_exc(limit=3)
                                                                log_it(exc_str, logging.DEBUG)
                                                        ############### work in progress
                                        except:
                                            log_it("problem with directory " + os.path.join(ls.remote_path, td, dl.intermed_dir1, subj),logging.WARN)
                                            exc_str = traceback.format_exc(limit=3)
                                            log_it(exc_str, logging.DEBUG)

                            else:
                                log_it(base_remote_dir + " does not exist on " + lc.host,
                                                       logging.WARN)
                        except:
                            log_it("problem with directory " + os.path.join(ls.remote_path, td, dl.intermed_dir1), logging.WARN)
                            exc_str = traceback.format_exc(limit=3)
                            log_it(exc_str, logging.DEBUG)
            except:
                log_it("CAUTION: download setting " + str(dl_i + 1) + "/" + str(len(dl_tasks)) + " : " + dl.description + "did not finish without errors!",
                       logging.WARN)
                exc_str = traceback.format_exc(limit=3)
                log_it(exc_str, logging.DEBUG)

    # connection closed automatically
    if sftp._sftp_live == False:
        log_it("connection closed", logging.INFO)
except:
    log_it("Connection to " + lc.host + " (user:" + lc.user + ") could not be established", logging.WARN)
    exc_str = traceback.format_exc(limit=3)
    log_it(exc_str, logging.WARN)
#close logging handlers for files to become immediately available
for lgr in logger:
    handler = lgr.handlers[0]
    lgr.removeHandler(handler)
    handler.close()