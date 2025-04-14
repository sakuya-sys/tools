from optparse import OptionParser
import socket
import sys

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

    if sys.argv[1]=='-v':
        print('本扫描器属于v1.2 (对于本人来说)')

    defaultportlist=[80,3306,3307,22,20,21,23,8080]

    usage="\npython scans.py -i <ip> -p <port> 单点扫描\n" \
          "\npython scans.py -i <ip> -p <port1>,<port2>,<port3> 列表扫描\n" \
          "\npython scans.py -i <ip> -p <port1>-<port2> 范围扫描\n" \
          "\npython scans.py -i <ip> -p default 默认扫描"
    parser=OptionParser(usage=usage)
    parser.add_option("-i",'--ipaddress',type="string",dest="ip",help="your target ip here")
    parser.add_option('-p',"--port",type='string',dest='port',help='your target port here')
    
    (options,args)=parser.parse_args()#设置参数和选项进行赋值

    ip=options.ip
    port=options.port
    
    print(port)
    print(type(port))

    if ',' in port:#列表扫描
        portlist=list(port.split(','))
        scan(ip,portlist)

    elif '-' in port:#范围扫描
        portlist=list(port.split('-'))
        port1=portlist[0]
        port2=portlist[1]
        many_scan(ip,port1,port2)
    
    elif 'default' in port:#默认扫描
        scan(ip,defaultportlist)

    else:#单点扫描
        scan(ip,[port])

if __name__=='__main__':
    main()