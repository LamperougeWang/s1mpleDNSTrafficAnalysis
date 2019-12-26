from scapy.all import *
import operator
def read_test(n):
    i=0
    with PcapReader(filename="output_00000_20190701000004.pcap") as pcap_reader:
        for pkt in pcap_reader:
            print(repr(pkt))
            if (i>n):
                break


def count_domain_name_frequency(filename,n):
    i=0
    frequency = {}
    with PcapReader(filename=filename) as pcap_reader:
        for pkt in pcap_reader:
            if (DNS in pkt):
                dns = pkt.getlayer('DNS')
                if (dns.qr==0):
                    if hasattr(dns, 'qd') and hasattr(dns.qd, 'qname'):
                        domain_name = dns.qd.qname
                    else:
                        continue
                    if domain_name == None:
                        continue
                    if domain_name not in frequency:
                        frequency[domain_name] = 1
                    else:
                        frequency[domain_name] += 1
                    # print(dns.qd.qname)
                    # i=i+1
                    # if (i>n):
                    #     break
    sorted_fre = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)
    print(sorted_fre)

if __name__ == '__main__':
    count_domain_name_frequency('output_00000_20190701000004.pcap',50)
    # frequency = {}
    # frequency['word']=21
    # frequency['as']=3
    # frequency['hell']=5
    # x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    # sorted_x = sorted(x.items(), key=operator.itemgetter(1))
    # sorted_fre = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)
    # print(sorted_fre)