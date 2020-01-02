from bloom_filter import BloomFilter
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

def annexJsonToDict(json_dir_path):
    
    tempn = 0
    name_dict = {}

    json_list = get_dir_file(json_dir_path)
    for json_file_name in json_list:
        
        # tempn+=1
        # if tempn > 2:
        #     break

        json_file_full_name = json_dir_path+json_file_name
        with open(json_file_full_name, 'r') as f:
            data = json.load(f)

        # key_list = data.keys()
        for key in list(data):
            if data[key] < 5:
                data.pop(key)
            elif key.endswith('.arpa.'):
                data.pop(key)
        
        name_dict = { **name_dict, **data }


    return name_dict

def writeAggregatedDictToFile(target_dict, name):
     with open(name, 'w') as f:
        json.dump(target_dict, f)

def getHotestKey(num, data):

    for key in list(data):
        if data[key] < num:
            data.pop(key)
            
    return data



if __name__ == '__main__':

    argv = sys.argv

    # file_list = get_dir_file(traffic_dir_path)
    amp_json_dir_path = "/home/guest/nextnet/IPv6_DNS/ampjsondir/"
    dns_req_mix_json_dir_path = "/home/guest/nextnet/IPv6_DNS/tempjsondir/"
    dns_req_v6_json_dir_path = "/home/guest/nextnet/IPv6_DNS/tempjsondirv6/"

    # domain_data_mix = annexJsonToDict(dns_req_mix_json_dir_path)# "data_v4.json")
    domain_data_v6 = annexJsonToDict(dns_req_v6_json_dir_path)# "data_v6.json")

    # writeAggregatedDictToFile(domain_data_mix, 'data_mix.json')
    writeAggregatedDictToFile(domain_data_v6, 'data_v6.json')


    # with open('data_mix.json', 'r') as f:
    #     domain_data_mix = json.load(f)    

    # with open('data_v6.json', 'r') as f:
    #     domain_data_v6 = json.load(f)    


    # domain_data_mix = getHotestKey(100, domain_data_mix)
    # domain_data_v6 = getHotestKey(100, domain_data_v6)
    
    # sorted_domain_data_mix = sorted(domain_data_mix.items(), key=operator.itemgetter(1),reverse=True)
    # sorted_domain_data_v6 = sorted(domain_data_v6.items(), key=operator.itemgetter(1),reverse=True)


 


    


    