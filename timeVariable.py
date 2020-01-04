from scapy.all import *
import operator
import os, sys
from threading import Thread
from concurrent.futures import ThreadPoolExecutor,wait,as_completed
from concurrent.futures import ProcessPoolExecutor
from time import sleep
import re
import json
import multiprocessing
import ipaddress
def get_dir_file(dirname = None):
    # file_list = []
    if dirname == None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
    else:
        dir_path = dirname
    
    g = os.walk(dir_path)  

    for path,dir_list,file_list in g:  
        pass
        # for file_name in file_list:   
            # print(os.path.join(path, file_name) )
    return file_list    

def getTimeRequestNumber(dns_req_v6_json_dir_path):
    
    timeRequestDict = {}
    
    json_list = get_dir_file(dns_req_v6_json_dir_path)
    for file_name in json_list:
        file_id = re.findall(r'\d+', file_name)[-1]

        json_file_full_name = dns_req_v6_json_dir_path+file_name
        with open(json_file_full_name, 'r') as f:
            data = json.load(f)


        request_num = 0
        for key in list(data):
            request_num += data[key]
         
        if file_id not in timeRequestDict:
            timeRequestDict[file_id] = request_num
    
    return timeRequestDict

def getTimeAmpNumber(amp_json_dir_path):
    
    timeAmpDict = {}
    
    json_list = get_dir_file(amp_json_dir_path)
    for file_name in json_list:
        file_id = re.findall(r'\d+', file_name)[-1]

        json_file_full_name = amp_json_dir_path+file_name
        with open(json_file_full_name, 'r') as f:
            data = json.load(f)


        amp_num = 0
        for key in list(data):
            if data[key] > 5:
                amp_num += data[key]
         
        if file_id not in timeAmpDict:
            timeAmpDict[file_id] = amp_num
    
    return timeAmpDict

if __name__ == '__main__':

    argv = sys.argv

    # file_list = get_dir_file(traffic_dir_path)
    amp_json_dir_path = "/home/guest/nextnet/IPv6_DNS/ampjsondir/"
 
    dns_req_v6_json_dir_path = "/home/guest/nextnet/IPv6_DNS/tempjsondirv6/"

    # timeRequestDict = getTimeRequestNumber(dns_req_v6_json_dir_path)
    # with open('timeRequestDict.json', 'w') as f:
    #     json.dump(timeRequestDict, f)
    # sorted(timeRequestDict.keys())
    # print(timeRequestDict)

    timeAmpDict = getTimeAmpNumber(amp_json_dir_path)
    with open('timeAmpDict.json', 'w') as f:
        json.dump(timeAmpDict, f)
    