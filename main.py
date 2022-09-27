import os, sys, requests, pip._vendor.requests
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
local_log = input("\nChoose name for local file copy of log: ")

response = pip._vendor.requests.get(remote_log)
open(local_log, "wb").write(response.content)

totalDayLogs = 0 #initialize counter for the day months
tempDay = input('\nAnalyze the number of requests on a given day? Enter a date using the format "DD/Mon/YYYY." Or, enter "skip" to skip this step: ')

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
remote_log_size = float(requests.head(remote_log).headers["content-length"])

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
print("\nInspecting file now...\n")
print("****************")
print("MARKETING REPORT")
print("****************")

# Read local log file and count lines to output total requests
with open(local_log, "r") as fp:
  lines = len(fp.readlines())
  print("")
  print(str(lines) + " total requests in log file.")
fp.close

totalLogsSix = 0 #initialize counter for the six months
f = open(local_log, "r")
if f.mode == 'r':
    fl = f.readlines()
    for x in fl:
      if (x[0] == 'l') and (x[10] == '[') : #if the line starts with l then it is a different format than rtemote
        temp_date =  x[11:22] #we dissect these elements since we only want to see day month and year
        if temp_date[7:] == '1995': #looking for the year 1995 only filter
          if temp_date[3:6] == 'Jun' or temp_date[3:6] == 'Jul' or temp_date[3:6] == 'Aug' or temp_date[3:6] == 'Sep' or temp_date[3:6] == 'May': #if the month is from May-Sept it auto qualifies
            totalLogsSix = totalLogsSix + 1
          elif temp_date[3:6] == 'Apr': #if it is april we need to check if it is the 11th and after
              if int(temp_date[0:2]) >= 11:
                totalLogsSix = totalLogsSix + 1
                #print(temp_date)
          elif temp_date[3:6] == 'Oct': #if it is october we check if it is the 11th or before
            if int(temp_date[0:2]) <= 11:
                totalLogsSix = totalLogsSix + 1
      #the same as above but if line starts with remote
      if (x[0] == 'r') and (x[11] == '[') :
        temp_date =  x[12:23]
        if temp_date[7:] == '1995': #looking for th eyear 1995 only filter
          if temp_date[3:6] == 'Jun' or temp_date[3:6] == 'Jul' or temp_date[3:6] == 'Aug' or temp_date[3:6] == 'Sep' or temp_date[3:6] == 'May': #if the month is from May-Sept it auto qualifies
            totalLogsSix = totalLogsSix + 1
          elif temp_date[3:6] == 'Apr':
              if int(temp_date[0:2]) >= 11:
                totalLogsSix = totalLogsSix + 1
          elif temp_date[3:6] == 'Oct':
            if int(temp_date[0:2]) <= 11:
                totalLogsSix = totalLogsSix + 1

print("")
print(str(totalLogsSix) + " requests in the last 6 months.")

if(tempDay != "skip"):
  f = open(local_log, "r")
  if f.mode == 'r':
      fl = f.readlines()
      for x in fl:
        if (x[0] == 'l') and (x[10] == '[') : #if the line starts with l then it is a different format than remote
          temp_date =  x[11:22] #we dissect these elements since we only want to see day month and year
          if temp_date == tempDay: #comparing the current day with the day chosen
            totalDayLogs = totalDayLogs + 1
  
        #the same as above but if line starts with remote
        if (x[0] == 'r') and (x[11] == '[') :
          temp_date =  x[12:23]
          if temp_date == tempDay: #comparing the current day with the day chosen
              totalDayLogs = totalDayLogs + 1
  f.close
  print("")
  print(str(totalDayLogs) + " requests made on "+ str(tempDay) + ".")

#What percentage of the requests were not successful (any 4xx status code)?
file = open(local_log, "r")
#read content of file to string
data = file.read()
#get number of error 3xx occurrences
occurrences_3 = data.count('1.0" 3')
#get percentage of error 3xx occurrences
occurrences_3_percent = int((occurrences_3 / lines) * 100)
#print percentage of error 3xx occurrences
print("")
print(str(occurrences_3_percent) + "% of requests were redirected elsewhere (Error 3xx).")

#get number of error 3xx
occurrences_4 = data.count('1.0" 4')
#get percentage of error 4xx occurrences
occurrences_4_percent = int((occurrences_4 / lines) * 100)
#print percentage of error 4xx occurrences
print("")
print(str(occurrences_4_percent) + "% of requests were unsuccessful (Error 4xx).")

# print('Number of 3xx error occurrences:', occurrences_3)
# print('Number of 4xx error occurrences:', occurrences_4)
f.close

dates = []
Files = {}
file_names = []
error_codes = []
n_dates = []
n1_dates = []
year_amount = []
n_month = {}
not_successful_request = 0
redirected_request = redirected_request = 0

open_log = open(local_log, 'r')

for row in open_log: 
    split = row.split(' ')
    if(len(split) > 8):
        error_codes.append(split[8])
        file_names.append(split[6])
    if(len(split[3]) > 14):
        dates.append(split[3]) 

for date in dates:
    n_dates.append(date[1:12])
    n1_dates.append(date[1:3])

for d in n1_dates:
    if(d in n_month):
        n_month[d] += 1
    else:
        n_month[d] = 1
        
for mistakes in error_codes: 
    if(mistakes[0] == '3'):
        redirected_request = redirected_request + 1
    if(mistakes[0] == '4'):
        not_successful_request = not_successful_request + 1
    
redirected_percent = (redirected_request / len(dates)) * 100
redirected_percent = "{:.2f}".format(redirected_percent)
not_successful_percent = (not_successful_request / len(dates)) * 100
not_successful_percent = "{:.2f}".format(not_successful_percent)

for file in file_names:
    if(file in Files):
        Files[file] += 1
    else:
        Files[file] = 1      

most_requested = max(Files, key=Files.get)
least_requested = min(Files, key=Files.get)

#5
print()
print("Most-requested file: " + str(most_requested))
print()
#6
print("Least-requested file: " + str(least_requested))