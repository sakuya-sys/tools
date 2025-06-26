from  socket import *
udp_server=socket(AF_INET,SOCK_DGRAM)
udp_server.bind(('127.0.0.1',6666))
while True:
    try:
        data,addr=udp_server.recvfrom(1024)
        if 'bye'==data.decode():
            print('对方请求断开')
            message=input('你要说些什么:')
            udp_server.sendto(message.encode(),addr)
            udp_server.close()
        print('对方向你发来信息:',end='')
        print(data.decode())
        message=input('你要说些什么:')
        udp_server.sendto(message.encode(),addr)
    except Exception as error:
        print(f'异常错误为:{error}')