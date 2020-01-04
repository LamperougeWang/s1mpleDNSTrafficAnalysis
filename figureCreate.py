from bloom_filter import BloomFilter
from scapy.all import *
import operator
import os, sys
import matplotlib.pyplot as plt
import matplotlib
from time import sleep
import re
import json
import multiprocessing
import ipaddress
from matplotlib.backends.backend_pdf import PdfPages 

def getHotestKey(num, data):

    for key in list(data):
        if data[key] < num:
            data.pop(key)
            
    return data


def getHotDomainRanking():

    with open('data_v6.json', 'r') as f:
        domain_data_v6 = json.load(f)    

    domain_data_v6 = getHotestKey(100, domain_data_v6)
    
    sorted_domain_data_v6 = sorted(domain_data_v6.items(), key=operator.itemgetter(1),reverse=True)
        
    # matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False
    host_list = []
    request_num_list = []

    n = 0
    for item in sorted_domain_data_v6:
        n += 1
        if n > 20:
            break
        host_list.append(item[0])
        request_num_list.append(item[1])
        # print(item[0])
        # print(item[1])
    host_list.reverse()
    request_num_list.reverse()

    fig, ax = plt.subplots()
    b = ax.barh(range(len(host_list)), request_num_list, color='#6699CC')


    #为横向水平的柱图右侧添加数据标签。
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y()+rect.get_height()/2, '%d' %
                int(w), ha='left', va='center')
    
    #设置Y轴纵坐标上的刻度线标签。
    ax.set_yticks(range(len(host_list)))
    ax.set_yticklabels(host_list,fontsize=3,wrap=True)
    # ax.set_ylable(fontsize=5)
    
    #不要X横坐标上的label标签。
    plt.xticks(())
    # plt.yticks(fontsize=10)
    plt.title('HotDomainRanking', loc='center', fontsize='12',
            fontweight='bold', color='black')
    
    

    plt.savefig('HotDomainRanking.pdf')
    plt.show()


def getTimeRequest():
    with open('timeRequestDict.json', 'r') as f:
        time_request_dict = json.load(f)    

        
    # matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False
    time_list = []
    request_num_list = []
    for i in range(23):
        time_list.append(i)
        for key in time_request_dict.keys():
            if i == int(key):
                request_num_list.append(time_request_dict[key])
                break
    
    print(time_list)
    print(request_num_list)
    # l = plt.plot(time_list, request_num_list, 'r--')
    plt.plot(time_list, request_num_list, 'go-')
    plt.title('DNS Request Number over Time in One Day')
    plt.xlabel('Time')
    plt.ylabel('Request Number')
    # plt.xticks(rotation=45)
    # plt.legend()

    for a, b in zip(time_list, request_num_list):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=5)

    plt.savefig('RequestNumOverTime.pdf')
    plt.show()

def getTimeAmp():
    with open('timeAmpDict.json', 'r') as f:
        time_amp_dict = json.load(f)    

        
    # matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False
    time_list = []
    amp_num_list = []
    for i in range(23):
        time_list.append(i)
        for key in time_amp_dict.keys():
            if i == int(key):
                amp_num_list.append(time_amp_dict[key])
                break
    
    print(time_list)
    print(amp_num_list)
    # l = plt.plot(time_list, amp_num_list, 'r--',label="Packet Number")
    plt.plot(time_list, amp_num_list, 'r^-',label="Packet Number")
    plt.title('DNS Amplification Attack Packet Number over Time in One Day')
    plt.xlabel('Time')
    # plt.ylabel('Amplification Packet Number')
    # plt.xticks(rotation=45)
    plt.legend()

    for a, b in zip(time_list, amp_num_list):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=4)

    plt.savefig('AmpNumOverTime.pdf')
    plt.show()

if __name__ == "__main__":
    # getTimeRequest()
    getTimeAmp()


    
