from re import L
import pip._vendor.requests

URL = "https://s3.amazonaws.com/tcmg476/http_access_log"
response = pip._vendor.requests.get(URL)
open("LogFile.txt", "wb").write(response.content)

totalLogs = 0
f = open("LogFile.txt", "r")
if f.mode == 'r':
    fl = f.readlines()
    for x in fl:
        totalLogs = totalLogs + 1
f.close
print(totalLogs)
##########################################################################################################################################################################
totalLogsSix = 0 #initialize counter for the six months
f = open("LogFile.txt", "r")
if f.mode == 'r':
    fl = f.readlines()
    for x in fl:
      if (x[0] == 'l') and (x[10] == '[') : #if the line starts with l then it is a different format than rtemote
        temp_date =  x[11:22] #we dissect these elements since we only want to see day month and year
        if temp_date[7:] == '1995': #looking for th eyear 1995 only filter
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

print(totalLogsSix)
            
f.close

