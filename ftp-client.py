from socket import *
import sys
import time


ADDR = ("127.0.0.1", 8888)


class FTPClient:
    def __init__(self, c):
        self.c = c

    def get_list(self):
        self.c.send(b'FL')
        data = self.c.recv(256).decode()
        if data == "OK":
            f_list = self.c.recv(4096).decode()
            print(f_list)
        else:
            print(data)

    def quit(self):
        self.c.send("EX".encode())
        self.c.close()
        sys.exit()

    def get_file(self, file_name):
        cmd = "DL" + file_name
        self.c.send(cmd.encode())
        data = self.c.recv(128).decode()
        if data == "OK":
            f = open(file_name, 'wb')
            while True:
                data = self.c.recv(1024)
                if data == b"##":
                    break
                print(data)
                f.write(data)
            f.close()
        else:
            print(data.decode())

    def put_file(self,filename):
        try:
            f = open(filename, 'rb')
        except FileNotFoundError:
            print("该文件不存在，请检查文件名是否正确")
            return
        # 防止客户端输入的文件名带有路径，切割去除路径获取纯净文件名
        filename = filename.split('/')[-1]
        cmd = 'UL'+filename
        self.c.send(cmd.decode())
        data = self.c.recv(128).decode()
        if data =='OK':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    data = b'##*'
                    self.c.send(data)
                    break
                self.c.send(data)
            f.close()
        else:
            print(data)




def main():
    c = socket()
    try:
        c.connect(ADDR)
    except Exception as e:
        print(e)
        return

    # 实例化一个对象，针对不同请求调用不同实例方法
    ftp = FTPClient(c)
    while True:
        print("\n==========请输入命令==========")
        print("*******    filelist    *******")
        print("*******    get file    *******")
        print("*******    put file    *******")
        print("*******      exit      *******")
        print("=============================")
        cmd = input("请输入功能序号>>\t")
        if cmd == 'filelist':
            ftp.get_list()
        elif cmd[:3] == 'get':
            filename = cmd.strip(" ").split(" ")[-1]
            ftp.get_file(filename)
        elif cmd[:3] == 'put':
            filename = cmd.strip(' ').split(' ')[-1]
            ftp.put_file(filename)
        elif cmd == 'exit':
            ftp.quit()
            break
        else:
            print("请输入正确序号")


if __name__ == "__main__":
    main()
