from socket import *
import time
serverhost='127.0.0.1'
serverport=8888


server_socket=socket(AF_INET,SOCK_STREAM)#创建一个TCPsocket (欢迎socket)
server_socket.bind((serverhost,serverport))#socket绑定端口号与ip地址
server_socket.listen()#监听 欢迎socket

print('服务器已经准备好了')
time.sleep(3)
print('等待客户端接入')
connection_socket,address=server_socket.accept()#接受客户端的连接 并且创建一个新的socket(连接socket)
print('ip地址为：',address,'的用户上线了')
while True:
    data=connection_socket.recv(1024).decode()#接收数据
    print('收到来自客户端的信息：',data)
    time.sleep(3)
    modified_data=input('你要对对方说什么：')
    connection_socket.send(modified_data.encode())#发送数据
    if(data=='bye'):
        print('用户下线了')
        connection_socket.send(modified_data.encode())
        connection_socket.close()#关闭连接
        print('服务器关闭')
        break

