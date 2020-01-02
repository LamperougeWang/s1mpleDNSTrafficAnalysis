from scapy.all import *
import operator
import os, sys
from threading import Thread
from concurrent.futures import ThreadPoolExecutor,wait,as_completed
from time import sleep
import re
import json
import multiprocessing


def funcname(json_dir_path=None):
    # Reading data back
    with open(json_dir_path+'data.json', 'r') as f:
        data = json.load(f)
    print(type(data))
    print(data)

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

def annexJsonToDict(json_dir_path, json_list):
    name_dict = {}

    for json_file_name in json_list:
        json_file_full_name = json_dir_path+json_file_name
        with open(json_file_full_name, 'r') as f:
            data = json.load(f)

        # key_list = data.keys()
        for key in list(data):
            if data[key] < 5:
                data.pop(key)
        
        name_dict = { **name_dict, **data }


    return name_dict

def sort_dict(json_file_full_name):
    with open(json_file_full_name, 'r') as f:
        data = json.load(f)
    print(type(data))
    sorted_data = sorted(data.items(), key=operator.itemgetter(1),reverse=True)
    n = 0
    for item in sorted_data:
        n+=1
        print(item)
        # if n > 50:
        #     break
    # print(type(sorted_name_dict))



def main(argv):
    # argv[0] json_dir_path
    # argv[1] dst_dir_path
    # argv[2] dst_name
    
    traffic_dir_path = "/home/guest/nextnet/IPv6_DNS/temp/"
    json_dir_path = None
    dst_dir_path = None
    dst_name = None

    if len(argv) == 1:    
        json_dir_path = "/home/guest/nextnet/IPv6_DNS/tempjsondir/"
        dst_dir_path = "/home/guest/nextnet/IPv6_DNS/summaryjsondir/"
        dst_name = 'data'
    else:
        json_dir_path = argv[0]
        dst_dir_path = argv[1]
        dst_name = argv[2]

    json_list = get_dir_file(json_dir_path)
    print(json_list)
    # return
    aggregate_dict = {}
    
    aggregate_dict = annexJsonToDict(json_dir_path, json_list)
    # sorted_name_dict = sorted(name_dict.items(), key=operator.itemgetter(1),reverse=True)
    print(type(aggregate_dict))
    
    # # key_list = name_dict.keys()
    # # # for key in list(name_dict):
    # # #     if name_dict[key] < 5:
    # # #         name_dict.pop(key)
    # # sorted_name_dict = dict(sorted_name_dict)
    # # json_str = json.dumps(name_dict)

    with open(dst_dir_path + dst_name+'.json', 'w') as f:
        json.dump(aggregate_dict, f)

    # for jsonfile in json_list:
    #     read_json_into_dict(json_dir_path, jsonfile,name_dict)
    # sorted_name_dict = sorted(name_dict.items(), key=operator.itemgetter(1),reverse=True)
    # print(name_dict)


if __name__ == '__main__':
    main(sys.argv)
    # sort_dict('/home/guest/nextnet/IPv6_DNS/summaryjsondir/data.json')

    
    