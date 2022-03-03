from dataclasses import field
from email import header
import vk
import os
from urllib import response
import requests
import datetime
from datetime import date
import time
from bs4 import BeautifulSoup
import re


def get_name():
    print("Please, write name of directory: ",end ="")
    name = input()
    return name


def get_uid():
    print("Enter, user vk id of personal vk page: ", end ="")
    url = input()
    return url

def get_time():
    time = datetime.datetime.now().time()
    return str(time)[0:8]

def get_date():
    date_r = date.today()
    return str(date_r)[8:] + "." + str(date_r)[5:7] + "." + str(date_r)[0:4]

def check_uniq(name):   # проверка есть ли в дирректории папка с таким именем
    for i in os.listdir('.'):
        if(i == name):
            return True
    return False

def time_to_start_end(dialog):
    while(1):
        print(dialog)
        time_s = input()
        if(re.fullmatch(r'[0-2][0-9]:\d\d',str(time_s))):
            return time_s
        else:
            print("ERROR!!!!!")        
    
def wait(timeS):
    while(1):
        if(get_time()[0:5] != timeS):
            time.sleep(60 - int(str(datetime.datetime.now().time())[6:8]))
        else:
            break

def get_period():
    print("Enter period of scaning(minutes): ",end = "")
    return float(input())

def analize(response):
    if(response[0].get("online") == 0):
        return "N"  # No
    elif(response[0].get("online") == 1 and response[0].get("online_mobile",0) == 1 ):
        return "T"  #telephone
    elif(response[0].get("online") == 1):
        return "C"  # computer
    else:
        return "E"  #Error

def work(f,timeStop,uid,per,token):
    session = vk.Session(access_token=token)
    vk_api = vk.API(session,v= "5.95")
    while(1):
        if( int(get_time()[0:2]) >= int(timeStop[0:2]) and int(get_time()[3:5]) >= int(timeStop[3:5])):
            break
        #response = requests.get(uid)
        resp = vk_api.users.get(user_id = uid, fields = "online")
        status = analize(resp)
        print(get_time() + " " + status)
        f.write(get_time() + " " + status + '\n')
        time.sleep(per*60)
 


def main():
    name = get_name()
    f = open("./access_token.txt",'r')
    token = f.readline()
    token = str(token)[0:-1]
    f.close()
    if(check_uniq(name)):
        os.chdir("./"+str(name))  
    else:
        os.mkdir("./"+str(name), 0o777)
        os.chdir("./"+str(name))  
    uid = get_uid()
    f = open(get_date()+".txt", "a")
    timeStart = time_to_start_end("Enter time, when script will start working in format(hh:mm): ")
    timeStop = time_to_start_end("Enter time, when script will finish it's working in format(hh:mm): ")
    per = get_period()
    wait(timeStart)
    work(f,timeStop,uid,per,token)
    f.close()


if __name__ == "__main__":
    main()