from socket import *
import time

serverhost=input('请输出服务器的ip地址：')
serverport=8888

client_socket=socket(AF_INET,SOCK_STREAM)#创建一个TCPsocket
#此处并没有使用bind() 因为客户端不需要绑定端口号与ip地址 系统会自动分配
client_socket.connect((serverhost,serverport))#主动连接服务器
#上一行命令执行成功 已经自动执行了3次握手 建立了TCP连接
print("连接成功")
while True:
    time.sleep(3)
    data=input('你要对对方说什么:')#用户键入数据 与服务器进行交互
    client_socket.send(data.encode())#发送数据
    modified_data=client_socket.recv(1024).decode()#接收来自服务器的数据
    if(data=='bye'):
        modified_data=client_socket.recv(1024).decode()
        print('收到来自于服务器的信息：',modified_data)
        client_socket.close()#关闭连接
        break
    time.sleep(5)
    print('收到来自于服务器的数据：',modified_data)#打印来自服务器的数据

