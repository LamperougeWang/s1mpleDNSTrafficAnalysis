from scapy.all import *
import operator
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor,wait,as_completed
from time import sleep
import re
import json

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


def count_domain_name_frequency(traffic_dir_path, file_name):
    # print(traffic_dir_path)
    # print(file_name)
    file_id = re.findall(r'\d+', file_name)[0]
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
                        print(domain_name)
                        n+=1
                        if (n>20):
                            break
            # except expression as identifier:
            #     pass
            finally:
                print("UnicodeDecodeError")
                pass
            
    sorted_fre = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)
    # print(sorted_fre)
    json_str = json.dumps(sorted_fre)

    with open(traffic_dir_path+file_id+'.json', 'w') as f:
        f.write(json_str)
    print(file_id+"finished")

if __name__ == '__main__':
    traffic_dir_path = "/home/guest/nextnet/IPv6_DNS/temp/"
    file_list = get_dir_file(traffic_dir_path)
    executor = ThreadPoolExecutor(max_workers=50)
    f_list = []
    for name in file_list:
        future = executor.submit(count_domain_name_frequency,traffic_dir_path,name)
        print(future.result())
        # f_list.append(future)
    # print(wait(f_list))



    