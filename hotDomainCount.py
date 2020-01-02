from scapy.all import *
import operator
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor,wait,as_completed
from concurrent.futures import ProcessPoolExecutor
from time import sleep
import re
import json
import multiprocessing

def read_test(n):
    i=0
    with PcapReader(filename="output_00000_20190701000004.pcap") as pcap_reader:
        for pkt in pcap_reader:
            print(repr(pkt))
            if (i>n):
                break

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


def count_domain_name_frequency(traffic_dir_path,json_dir_path, file_name):
    # print(traffic_dir_path)
    # print(file_name)
    file_id = re.findall(r'\d+', file_name)[-1]
    # print(file_id)
    # print(traffic_dir_path+file_id+'.json')
    # return
    n=0
    frequency = {}
    with PcapReader(filename=traffic_dir_path+file_name) as pcap_reader:
        for pkt in pcap_reader:
            try:
                if (DNS in pkt):
                    dns = pkt.getlayer('DNS')
                    if (dns.qr==0):
                        if hasattr(dns, 'qd') and hasattr(dns.qd, 'qname'):
                            domain_name = (dns.qd.qname).decode('utf-8',errors="ignore")
                        else:
                            continue
                        if domain_name == None:
                            continue
                        if domain_name not in frequency:
                            frequency[domain_name] = 1
                        else:
                            frequency[domain_name] += 1
                        # print(domain_name)
                        # n+=1
                        # if (n>20):
                        #     break
            # except expression as identifier:
            #     pass
            finally:
                # print("UnicodeDecodeError")
                pass
            
    # sorted_fre = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)
    # print(sorted_fre)
    # json_str = json.dumps(sorted_fre)

    with open(json_dir_path+file_id+'.json', 'w') as f:
        # f.write(json_str)
        json.dump(frequency,f)
    print(file_id+"finished")



def count_domain_name_frequency_v6(traffic_dir_path,json_dir_path, file_name):
    # print(traffic_dir_path)
    # print(file_name)
    file_id = re.findall(r'\d+', file_name)[-1]
    # print(file_id)
    # print(traffic_dir_path+file_id+'.json')
    # return
    n=0
    frequency = {}
    with PcapReader(filename=traffic_dir_path+file_name) as pcap_reader:
        for pkt in pcap_reader:
            try:
                if (IPv6 in pkt):
                    if (DNS in pkt):
                        dns = pkt.getlayer('DNS')
                        if (dns.qr==0):
                            if hasattr(dns, 'qd') and hasattr(dns.qd, 'qname'):
                                domain_name = (dns.qd.qname).decode('utf-8',errors="ignore")
                                if domain_name == None:
                                    continue
                                if domain_name.endswith('.arpa.'):
                                    continue
                                if domain_name not in frequency:
                                    frequency[domain_name] = 1
                                else:
                                    frequency[domain_name] += 1
                                # print(domain_name)
                                # n+=1
                                # if (n>20):
                                #     break
                            
                            
                            else:
                                continue
                            
            # except expression as identifier:
            #     pass
            finally:
                # print("UnicodeDecodeError")
                pass
            
    # sorted_fre = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)
    # print(sorted_fre)
    # json_str = json.dumps(sorted_fre)

    with open(json_dir_path+file_id+'.json', 'w') as f:
        # f.write(json_str)
        json.dump(frequency,f)
    print(file_id+" json v6 finished")

def read_json_into_dict(json_dir_path, file_name, name_dict):
    print(file_name)
    with open(json_dir_path+file_name,'r') as json_file:
        data = json.load(json_file)
    
    for item in data:
        if item[0] not in name_dict:
            name_dict[item[0]] = 1
        else:
            name_dict[item[0]] += item[1]
    # print(type(data))
    # print(data)
    
    return name_dict

if __name__ == '__main__':
    traffic_dir_path = "/home/guest/nextnet/IPv6_DNS/temp/"
    file_list = get_dir_file(traffic_dir_path)
    json_dir_path = "/home/guest/nextnet/IPv6_DNS/tempjsondirv6/"
    # json_list = get_dir_file(json_dir_path)
    name_dict = {}


    # print(file_list)
    # for name in file_list:
    #     count_domain_name_frequency_v6(traffic_dir_path,json_dir_path,name)

    executor = ProcessPoolExecutor(max_workers=30)
    f_list = []
    for name in file_list:
        future = executor.submit(count_domain_name_frequency_v6,traffic_dir_path,json_dir_path,name)
        print(future.done())


    print("Main Process")

        # f_list.append(future)
    # print(wait(f_list))
    



    