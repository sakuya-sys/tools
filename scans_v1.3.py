from scapy.all import IP,TCP,sr1,send,RandShort,ICMP,UDP
import argparse,socket
import threading


#TCP全连接
#使用socket模拟
#需要模拟三次握手 和 四次挥手
'''def all_TCP(ip,port):
    #创建了一个SYN包  但是并没有指名源端口

    #packet=scapy.IP(dst=ip)/scapy.TCP(dport=port,flags="S")
    
    #用sr来发送并且等待接受返回包的数据 _表示占位 忽略不需要返回的数据包 verbose用来关闭scapy的默认输出
    #scapy.sr()返回2个列表 应答包与未应答包
    

    syn_pkt=scapy.IP(dst=ip)/scapy.TCP(dport=port,flags='S',sport=scapy.RandShort())
    # sr1只接收第一个响应包 (即应答包
    syn_ack_resp=scapy.sr1(syn_pkt,timeoust=3,verbose=0)
    #计入初始SYN包的序列号
    cline_seq=syn_pkt[scapy.TCP].seq

    if not syn_ack_resp:
        print("{}{}TCP 连接失败".format(ip,port))
    #else:
        #遍历响应数据包
        #for snd,rcv in resp:

            #检测是否有TCP响应包 以0x12为标志
    if syn_ack_resp.haslayer(scapy.TCP) and syn_ack_resp[scapy.TCP].flags==0x12:
                #ACK+RST包 (ACK用来完成三次握手 RST用来结束连接
                #如使用sr导致等待响应 会有一定延迟 还是并没有设定源端口 没有设置序列号
                #send_rst=scapy.sr(scapy.IP(dst=ip)/scapy.TCP(dport=port,flags='AR'),timeout=3,verbose=0)
                
                #发送ACK报文 完成三次握手
                ack_num=syn_ack_resp[scapy.TCP].seq+1#记录syn_ack响应包的确认号  要是前一个响应包的序列号加1
                ack_pkt=scapy.IP(det=ip)/scapy.TCP(
                    sport=syn_ack_resp[scapy.TCP].dport,#给定源端口 且源端口为发送SYN包的源端口
                    dport=port,
                    flags='A',
                    ack=ack_num,
                    seq=cline_seq+1
                )
                #使用send立即发送 不用等待响应包 
                scapy.send(ack_pkt,verbose=0)
                #此时已经完成了TCP的连接 完成了三次握手

                
                print('IP为{}的主机的{}port正在开放'.format(ip,port))
                
                #构造FIN数据包 准备进行四次挥手完成正常的断开连接
                fin_pkt=scapy.IP(dst=ip)/scapy.TCP(
                    sport=syn_ack_resp[scapy.TCP].dport,
                    dport=port,
                    flags='F',
                    #seq=ack_pkt[scapy.TCP].sep+1, 
                    #ack=ack_num #上一个包没有ACK控制位 所以ack值不变
                )
               #发送并等待响应包
                fin_ack_resp=scapy.sr1(fin_pkt,timeout=3,verbose=0)

                if fin_ack_resp and fin_ack_resp[scapy.TCP].flags==0x10:
                    print('服务端确认关闭请求ACK')

                server_fin_resp=scapy.sr1(scapy.IP(dst=ip)/scapy.TCP(flags='A'),timeout=3,verbose=0)
                if server_fin_resp and server_fin_resp[scapy.TCP].flags==0x11:
                    print('服务端发送FIN')


                    final_ack=scapy.IP(dst=ip)/scapy.TCP(
                        sport=syn_ack_resp[scapy.TCP].dport,
                        dport=port,
                        ack=server_fin_resp[scapy.TCP].seq+1,
                        seq=fin_pkt[scapy.TCP].seq+1
                    )
    else:
                print("IP为{}的主机的{}port未开放".format(ip,port))
    pass'''


#使用socket模块写 TCP全连接
open_port=[]

def is_open(ip,port):
    s=socket.socket()
    try:
        s.connect((ip,port))#要使用元组来保存
        s.close()
        return True
    except:
        return False

def scan(ip,port):
    global open_port
    
    if is_open(ip,int(port)):
            print('主机ip为{}的{}端口正在开放'.format(ip,port))
            open_port.append(int(port))
    else:
            print('主机ip为{}的{}端口没有开放'.format(ip,port))
    pass


#半连接TCP
#只需要模拟三次握手的前两次就行 之后直接发送RST包断开连接就可以了

def half_TCP(ip,port):
    global open_port
    #创建了一个SYN包
    syn_pkt=IP(dst=ip)/TCP(dport=port,flags="S")
    #用sr1来发送并且接受一个返回包的数据
    syn_ack_resp=sr1(syn_pkt,timeout=3,verbose=0)

    
    #接受到其中第一个元组的第一个元素，包含TCP层的数据包 #判断是否是SYN-ACK包 
    if syn_ack_resp.haslayer(TCP) and syn_ack_resp[TCP].flags=='SA':
            #发送一个RST包 (用来直接断开连接 不需要完成三次握手
            send(IP(dst=ip)/TCP(dport=port,flags='R'),verbose=0)
            print('IP为{}的主机的{}port正在开放'.format(ip,port))
            open_port.append(int(port))
    else:
            print("IP为{}的主机的{}port未开放".format(ip,port))

    pass

#icmp扫描
'''def icmp_scan(ip,port):
    icmp_pkt=IP(dst=ip)/ICMP(dport=port)
    icmp_resp=sr1(icmp_pkt,tiemout=3,verbose=0)

    if not icmp_resp:
        print('IP为{}的主机的{}port未开放')
    else:
        print('IP为{}的主机的{}port正在开放'.format(ip,port))'''
    #笑死了 icmp作为网络层协议 不依赖传输层协议 根本就不能当做扫描的原理
#icmp更多作为判断主机是否在线 域名解析是否正常等判断主机正常的行为

#udp扫描 响应报文是icmp报文 不能简单的看是否有响应报文来检测是否存在端口开放 
#暂时无法使用
'''def udp_scan(ip,port):
    udp_pkt=IP(dst=ip)/UDP(dport=port)
    resp=sr1(udp_pkt,timeout=3,verbose=0)
    if not resp:
        print('IP为{}的主机的{}port未开放')
    else:
        print('IP为{}的主机的{}port正在开放'.format(ip,port))'''



#默认端口是开放的 主要目的是得到banner信息 简单的banner探测 不是http格式的报文 所以不能检测80端口
def banner_scan(ip,port):
    s=socket.socket()

    try:
        s.connect((ip,port))
        #发送hello数据流
        s.send('hello'.encode())
        #接收服务端响应 得到所在端口的服务类型
        banner=s.recv(1024)
        s.close()

        if banner:
                print('服务类型是{}'.format(banner.decode('utf-8')))
        else:
                print('服务类型无法被识别')
    except:
          print('端口未开放{}'.format(port))
          print('简单的banner探测 不是http格式的报文 所以不能检测服务是web服务的端口 (因为要求是http报文的格式) 比如80端口')


      

def main():
    #定义参数使用帮助
    usage='python scan_v1.3 -i <ip> -p <port> -m <method>'


    #定义ArgumentParser对象 用于解析命令行参数
    parse=argparse.ArgumentParser(description="NETWORK SCANNING TOOL")
    parse.add_argument('-i','--ip',required=True,help='IP')
    parse.add_argument('-p','--port',required=True,help='port')
    #method设置了一个互斥组 就是不能-m -TA这样设置参数 只能-TA 只要方法就行
    method_group=parse.add_mutually_exclusive_group(required=True)

    #action='store_true'就是布尔型开关
    method_group.add_argument('-TA',action='store_true',help='TCP全连接扫描')
    method_group.add_argument('-TH',action='store_true',help='TCP半连接扫描')
    method_group.add_argument('-U',action='store_true',help='UPD连接扫描(暂时无法使用)')
    method_group.add_argument('-B',action='store_true',help='banner扫描')

    #解析命令行参数并赋值给args
    args=parse.parse_args()

    ip=args.ip
    port=args.port
    method=args.TH
    #print('{} {} {}'.format(ip,port,method))


    defaultportlist=[80,3306,3307,22,21,20,23,443,8080]

    #除了banner扫描 其他所有的扫描的具体方法
    #单点扫描
    #列表扫描
    #范围扫描
    #默认扫描

    #TCP全连接端口扫描 高并发

    if args.TA:
        threads=[]
        if ',' in port:#列表扫描
            portlist=list(port.split(','))
            for i in portlist:
                t1=threading.Thread(target=scan,args=(ip,i))#创建一个线程 目标函数是scan 传入ip与port参数
                threads.append(t1)
                try:
                    t1.start()
                except Exception as error:
                     print(f'异常错误为：{error}')#启动线程执行任务

            #scan(ip,portlist)

        elif '-' in port:#范围扫描
            portlist=list(port.split('-'))
            port1=portlist[0]
            port2=portlist[1]
            for i in range(int(port1),int(port2)+1):
                t2=threading.Thread(target=scan,args=(ip,i))
                threads.append(t2)
                try:
                    t2.start()
                except Exception as error:
                     print(f'异常错误为：{error}')
    
        elif 'default' in port:#默认扫描
            for i in defaultportlist:
                t3=threading.Thread(target=scan,args=(ip,i))
                threads.append(t3)
                try:
                    t3.start()
                except Exception as error:
                     print(f'异常错误为：{error}')
        

        else:#单点扫描
            for i in [int(port)]:
                t4=threading.Thread(target=scan,args=(ip,i))
                threads.append(t4)
                try:
                    t4.start()
                except Exception as error:
                     print(f'异常错误为：{error}')
                     


        for t in threads:
             t.join()
        print('\nIP为{}的主机的这些端口{}正在开放'.format(ip,open_port))


          


    #TCP半连接端口扫描
    if args.TH:
        threads=[]
        if ',' in port:#列表扫描
            portlist=list(port.split(','))
            for i in portlist:
                t1=threading.Thread(target=half_TCP,args=(ip,i))#创建一个线程 目标函数是scan 传入ip与port参数
                threads.append(t1)
                try:
                    t1.start()
                except Exception as error:
                     print(f'异常错误为：{error}')#启动线程执行任务

            #scan(ip,portlist)

        elif '-' in port:#范围扫描
            portlist=list(port.split('-'))
            port1=portlist[0]
            port2=portlist[1]
            for i in range(int(port1),int(port2)+1):
                t2=threading.Thread(target=half_TCP,args=(ip,i))
                threads.append(t2)
                try:
                    t2.start()
                except Exception as error:
                     print(f'异常错误为：{error}')
    
        elif 'default' in port:#默认扫描
            for i in defaultportlist:
                t3=threading.Thread(target=half_TCP,args=(ip,i))
                threads.append(t3)
                try:
                    t3.start()
                except Exception as error:
                     print(f'异常错误为：{error}')
        

        else:#单点扫描
            for i in [int(port)]:
                t4=threading.Thread(target=half_TCP,args=(ip,i))
                threads.append(t4)
                try:
                    t4.start()
                except Exception as error:
                     print(f'异常错误为：{error}')


        for t in threads:
             t.join()
        print('\nIP为{}的主机的这些端口{}正在开放'.format(ip,open_port))
    
    #UDP连接端口扫描(暂时没有该功能


    #banner探测

    if args.B:
        banner_scan(ip,int(port))
        



if __name__=='__main__':
      main()