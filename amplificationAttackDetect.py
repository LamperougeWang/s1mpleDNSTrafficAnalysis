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


def detect_amplification(traffic_dir_path,json_dir_path, file_name):

    suspious = {}
    file_id = re.findall(r'\d+', file_name)[-1]
    n=0
    bloom = BloomFilter(max_elements=1000000, error_rate=0.05)
    with PcapReader(filename=traffic_dir_path+file_name) as pcap_reader:
        for pkt in pcap_reader:
            try:
                if (DNS in pkt):
                    ipv6 = pkt.getlayer('IPv6') #v4 or v6?
                    if ipv6 == None:
                        continue
                    udp = pkt.getlayer('UDP')
                    dns = pkt.getlayer('DNS')
                    if dns.qr==0: #request
                        bloom.add( (int(ipaddress.IPv6Address(ipv6.src)),\
                            int(ipaddress.IPv6Address(ipv6.dst)),\
                            udp.sport, udp.dport, dns.id))
                        
                    elif dns.qr == 1: #reply
                        reply_tuple = ((int(ipaddress.IPv6Address(ipv6.dst)),\
                            int(ipaddress.IPv6Address(ipv6.src)),\
                            udp.dport, udp.sport, dns.id)) # reverse the direction against request
                        if reply_tuple not in bloom:
                            if ipv6.dst not in suspious:
                                suspious[ipv6.dst] = 1
                            else:
                                suspious[ipv6.dst] += 1 
                    else:
                        pass

                    # n+=1
                    # if (n>20):
                    #     break
            finally:
                # print("UnicodeDecodeError")
                pass

    with open(json_dir_path+file_id+'amp.json', 'w') as f:
        # f.write(json_str)
        json.dump(suspious,f)
    print(file_id+"amp.json finished")

if __name__ == '__main__':

    argv = sys.argv

    traffic_dir_path = "/home/guest/nextnet/IPv6_DNS/temp/"
    file_list = get_dir_file(traffic_dir_path)
    json_dir_path = "/home/guest/nextnet/IPv6_DNS/ampjsondir/"
    # json_list = get_dir_file(json_dir_path)
    name_dict = {}

    executor = ProcessPoolExecutor(max_workers = 25)
    f_list = []
    for name in file_list:
        future = executor.submit(detect_amplification, traffic_dir_path, json_dir_path,name)
        print(future.done())


    print("Main Process")