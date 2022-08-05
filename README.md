# sftp_downloader

This code may help to download IMAGEN data via sftp.
You need to....
* ...have login credentials and enter these into the file secret.py (use secret_template.py to create it.) Caution: never push the file with your login credentials to a public github repository
* ...know what you want to download, look at the folder structure using an sftp browser before using this script

### Prerequisites
* Python 3 (tested with 3.7+)
* pysftp

### How-To

#### Folder structure
The downloader assumes the following folder structure on the sftp server:

```
remote_path/{time_dirs}/{overall_dirs}
or
remote_path/{time_dirs}/intermed_dir/{subjs}/{dirs}/{subj_files}
```
#### Download modes
There are four modes that help to do different things
```
mode = "dirs"   # "files" or "dirs" or "subjects" or "overall"
```
1. "overall" mode: download a set of given folders recursively (including all subdirectories and files)
2. "subjects" mode: download given subject folders recursively (including all subdirectories and files)
3. "dirs" mode: download specific subdirectories within subject folders recursively
4. "files" mode: download files which match specific patterns within specific subdirectories within subject folders

#### Steps
 * clone the repository
 * use secret_template.py to create a new file secret.py
 * enter your login information in secret.py
 * use settings_template.py to create a new file settings.py
 * enter your local path settings and your download definitions in settings.py 
 (some examples are given in settings_template.py)
 * start the script:
 ```
 python get_data.py
 ```
 * logfiles are created for basic information (info_logger*) and debugging information (debug_logger*) to check if something did not work.
 

### Limitations
* pysftp may not work properly with windows (e.g. recursive downloads may be buggy)
* download is not super fast (own experience:  1.5GB per hour)

### Caution
* not extensively tested for all use-cases, use at your own risk.
