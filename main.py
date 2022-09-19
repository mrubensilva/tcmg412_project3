import os, sys, requests
from urllib.request import urlretrieve

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

# Prompt user for link to remote log file
remote_log = input("Enter the URL for remote copy of log: ")
# Prompt user for name of local log file 
local_log = input("Choose name for local file copy of log: ")

# Check if local log file exists with name user provides to local_log
file_exists = os.path.exists(local_log)

# Download file if local_log file does not exist, move on if else
def need_download():
  if file_exists == False: 
    print("\nNo local file found with that name! Downloading now...")
    urlretrieve(remote_log, local_log, reporthook)
  else:
    print("\nA file with that name already exists! Checking local copy...")

need_download()
    
# Fetch size of remote log file and output
remote_log_size = float(requests.head("https://s3.amazonaws.com/tcmg476/http_access_log").headers["content-length"])

print("\nSize of remote log file: ", remote_log_size)

# Fetch size of local log copy and output
local_log_size = float(os.path.getsize(local_log))

print("Size of local log file copy: ", local_log_size)

# Check if user needs to download remote log file by comparing remote log file size with local log file size 
def need_update(): 
  a, b = remote_log_size, local_log_size

  if a != b:
    print("File size mismatch! Downloading updated remote log file...")
    urlretrieve(remote_log, local_log, reporthook)
  else:
    print("\nFile size match! Skipping remote log file download...")

need_update()


# Update user that fetching step is complete
print("\nAnalyzing file now...")

# Read local log file and count lines to output total requests
with open(local_log, "r") as fp:
  lines = len(fp.readlines())
  print("\nTotal requests made in time period represented in log file:", lines)
