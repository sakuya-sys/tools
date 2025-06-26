import optparse 
import socket
import sys
import threading

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
            print('主机ip为{}的{}端口正在开放'.format(ip,port),flush=0)
            open_port.append(int(port))
    else:
            print('主机ip为{}的{}端口没有开放'.format(ip,port),flush=0)
    pass



def main():

    if sys.argv[1]=='-v':
        print('本扫描器属于v1.2 (对于本人来说)')
        print('本扫描器属于TCP全连接扫描器')
        print('本版本在之前的基础之上,加入了thread模块,实现了并发的端口扫描')
        sys.exit()

    defaultportlist=[80,3306,3307,22,20,21,23,8080]

    usage="\npython scans.py_v1.2 -i <ip> -p <port> 单点扫描\n" \
          "\npython scans.py_v1.2 -i <ip> -p <port1>,<port2>,<port3> 列表扫描\n" \
          "\npython scans.py_v1.2 -i <ip> -p <port1>-<port2> 范围扫描\n" \
          "\npython scans.py_v1.2 -i <ip> -p default 默认扫描"
    parser=optparse.OptionParser(usage=usage)
    parser.add_option("-i",'--ipaddress',type="string",dest="ip",help="your target ip here")
    parser.add_option('-p',"--port",type='string',dest='port',help='your target port here')
    
    (options,args)=parser.parse_args()#设置参数和选项进行赋值

    ip=options.ip
    port=options.port
    
    threads=[]

    if ',' in port:#列表扫描
        portlist=list(port.split(','))
        for i in portlist:
            t1=threading.Thread(target=scan,args=(ip,i))#创建一个线程 目标函数是scan 传入ip与port参数
            threads.append(t1)
            t1.start()#启动线程执行任务

            #scan(ip,portlist)

    elif '-' in port:#范围扫描
        portlist=list(port.split('-'))
        port1=portlist[0]
        port2=portlist[1]
        for i in range(int(port1),int(port2)+1):
            t2=threading.Thread(target=scan,args=(ip,i))
            threads.append(t2)
            t2.start()
    
    elif 'default' in port:#默认扫描
        for i in defaultportlist:
            t3=threading.Thread(target=scan,args=(ip,i))
            threads.append(t3)
            t3.start()
        

    else:#单点扫描
        for i in [int(port)]:
            t4=threading.Thread(target=scan,args=(ip,i))
            threads.append(t4)
            t4.start()

    for t in threads:#等待所有子线程关闭后再关闭主线程
        t.join()
    print('目的主机的这些端口正在开放{}'.format(open_port))
    print('\n如果响应太慢 或者没有端口开放')
    print('可能是由于路由的问题 或者是有防火墙给拦截了 也可能是在线程池溢出了')
    print('本身是TCP全连接的方式扫描 所以花费的时间会比较长')

    

if __name__=='__main__':
    main()