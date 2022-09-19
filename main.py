import os, sys, urllib, requests, filecmp
from urllib.request import urlretrieve

# Prompt user for link to log file
remote_log = input("Enter the URL for remote copy of log: ")
# Prompt user for name of local file copy 
local_log = input("Choose name for local copy of log: ")

# Fetch size of remote log file and output
remote_log_size = float(requests.head('https://s3.amazonaws.com/tcmg476/http_access_log').headers['content-length'])

print("Size of remote log file: ", remote_log_size)

# Fetch size of local log copy and output
local_log_size = float(os.path.getsize(local_log))

print("Size of local log file copy: ", local_log_size)

# Progress bar for remote log file download
def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # Total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))
  
# Check if user needs to download remote log file by comparing remote log file size with local log file size 
def need_download(): 
  a, b = remote_log_size, local_log_size

  if a != b:
    print("File size mismatch, downloading remote log file...")
    urlretrieve(remote_log, local_log, reporthook)
  else:
    print("File size match, skipping remote log download...")

need_download()