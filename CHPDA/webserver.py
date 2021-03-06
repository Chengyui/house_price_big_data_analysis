# 将指定的html文件放置到指定端口

import socket
import os

def send2browser(filename):
    server_html = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_html.bind(('localhost', 8081))

    # 如果发现文件不存在，打开默认文件
    if os.path.exists(filename) == False :
        print("跳转到默认文件")
        file_html = open("error.html", "rb")
    else:
        # 以字节读取数据的权限去打开html_pro.html文件
        file_html = open(filename, "rb")

    # 读取文件内容
    data = file_html.read()
    server_html.listen(10)
    print("http://localhost:8081")
    # while True:
    conn, addr = server_html.accept()
    msg = conn.recv(1024 * 12)
    print(conn)

    # 下面这句话必须写，关于http协议的内容，以后说
    conn.sendall(bytes("HTTP/1.1 201 OK\r\n\r\n", "utf-8"))
    # 发送读取的内容
    conn.sendall(data)
    conn.close()
