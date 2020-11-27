from socket import *
import sys


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
        elif cmd == '3':
            pass
        elif cmd == '0':
            ftp.quit()
            break
        else:
            print("请输入正确序号")


if __name__ == "__main__":
    main()
