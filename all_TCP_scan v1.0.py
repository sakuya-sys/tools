import sys
import socket

def is_open(ip,port):
    s=socket.socket()
    try:
        s.connect((ip,port))#要使用元组来保存
        s.close()
        return True
    except:
        return False

def scan(ip,portlist):
    open_port=list()
    for i in portlist:
        if is_open(ip,int(i)):
            print('主机ip为{}的{}端口正在开放'.format(ip,i))
            open_port.append(int(i))
        else:
            print('主机ip为{}的{}端口没有开放'.format(ip,i))
    if len(open_port)>0:
        print('这些端口正在开放{}'.format(open_port))
    else:
        print('目的主机没有端口正在开放')
    print('\n如果响应太慢 或者没有端口开放')
    print('可能是由于路由的问题 或者是有防火墙给拦截了')
    print('本身是TCP全连接的方式扫描 所以花费的时间会比较长')
    pass

def many_scan(ip,s1,s2):
    open_port=list()
    for i in range(int(s1),int(s2)+1,1):
        if is_open(ip,i):
            print('主机ip为{}的{}端口正在开放'.format(ip,i))
            open_port.append(i)
        else:
            print('主机ip为{}的{}端口没有开放'.format(ip,i))
    if len(open_port)>0:
        print('这些端口正在开放{}'.format(open_port))
    else:
        print('目的主机没有端口正在开放')
    print('tip:\n如果响应太慢 或者没有端口开放')
    print('可能是由于路由的问题 或者是有防火墙给拦截了')
    print('本身是TCP全连接的方式扫描 所以花费的时间会比较长')
    pass


def main():
    defaultportlist=[80,8080,3306,22,21,23,1007]
    
    if len(sys.argv)>1:
        if sys.argv[1]=='-v':
            print('本扫描器版本属于v1.0 (对于我本人来说)')

        elif sys.argv[1]=='-p':#单点扫描
            ip,port=sys.argv[2],sys.argv[3]
            scan(ip,[port])

        elif sys.argv[1]=='-p1':#列表扫描
            ip=sys.argv[2]
            portlist=list(map(int,sys.argv[3].split(',')))
            scan(ip,portlist)

        elif sys.argv[1]=='-p2':#范围扫描
            ip,port1,port2=sys.argv[2],sys.argv[3],sys.argv[4]
            many_scan(ip,port1,port2)
    
        elif sys.argv[1]=='-p3':#默认扫描
            ip=sys.argv[2]
            scan(ip,defaultportlist)
        
    else:
        print('使用教程如下：')
        print('-p <ip> <port> 进行单点扫描')
        print('-p1 <ip> <port>,<port1>,<port2> (请输入多个端口号,比如 80,81,22,23) 进行批量扫描')
        print('-p2 <ip> <port1> <port2> (请输入端口范围) 进行范围扫描')
        print('-p3 <ip> (使用常用端口扫描)')
        print('本扫描器属于TCP全连接扫描器')


if __name__=='__main__':
    main()