from threading import Thread
import sys
from socket import *
import os
import time


ADDR = ("0.0.0.0", 8888)
FTP_DIR = r"E:/Download/"


class FTPServer(Thread):
    def __init__(self, client):
        self.client = client
        super(FTPServer, self).__init__()

    def get_list(self):
        f_list = os.listdir(FTP_DIR)
        if not f_list:
            self.client.send("文件库为空".encode())
        else:
            self.client.send(b'OK')
            time.sleep(1)
        f_str = ''
        for file in f_list:
            if file[0] != '.' and os.path.isfile(FTP_DIR+file):
                f_str += file + '\n'
        self.client.send(f_str.encode())

    def send_file(self, filename):
        try:
            f = open(FTP_DIR+filename, 'rb')
        except Exception:
            self.client.send("文件不存在".encode())
            return
        else:
            self.client.send(b"OK")
            time.sleep(0.1)
        while True:
            data = f.read(1024)
            if data == b'':
                time.sleep(0.1)
                self.client.send(b"##")
                break
            print(data)
            self.client.send(data)

    def put_file(self, filename):
        if os.path.exists(FTP_DIR+filename):
            self.client.send("文件已存在".encode())
        else:
            self.client.send(b'OK')

        f = open(FTP_DIR+filename, 'wb')
        while True:
            data = self.client.recv(1024)
            if data == b'##*':
                break
            f.write(data)
        f.close()



    def run(self):
        while True:
            data = self.client.recv(2048).decode()
            if data == 'FL':
                # 获取文件列表
                self.get_list()
            elif data == 'EX' or '':
                # 客户端退出，服务器对应该客户端的线程结束即可
                return
            elif data[:2] == 'DL':
                filename = data[2:]
                self.send_file(filename)
            elif data[:2] == 'UL':
                filename = data[2:]
                self.put_file(filename)


def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    print("服务器正在监听8888......")

    while True:
        try:
            client, addr = s.accept()
            print("已连接的客户端"+addr[0]+"，"+"端口号"+str(addr[1]))
        except KeyboardInterrupt:
            sys.exit("服务器退出")

        except Exception as e:
            print(e)
            continue

        t_client = FTPServer(client)
        t_client.setDaemon(True)
        t_client.start()


if __name__ == "__main__":
    main()

pass
