from  socket import *
udp_client=socket(AF_INET,SOCK_DGRAM)
ip=input('输入你想要连接的服务器ip:')
port=8000
ip_port=(ip,port)
while True:
    try:
        message=input('你要说些什么:')
        udp_client.sendto(message.encode(),ip_port)
        data,addr=udp_client.recvfrom(1024)
        if 'bye'==data.decode():
            print('对方请求断开')
            message=input('你要说些什么:')
            udp_client.sendto(message.encode(),ip_port)
            udp_client.close()
        print('对方向你发来信息:',end='')
        print(data.decode())
        message=input('你要说些什么:')
        udp_client.sendto(message.encode(),ip_port)
    except Exception as error:
        print(f'异常错误为:{error}')