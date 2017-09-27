import socket
import threading
from random import randint


class Listener(threading.Thread):
    def __init__(self, _s):
        threading.Thread.__init__(self)
        self.socket = _s

    def run(self):
        while True:
            try:
                data, addr = s.recvfrom(1024)
                data = data.decode('utf8')
                print("%s\n>" % data,end="")
            except Exception as e:
                print("[listen err] %s" % e)


if __name__ == '__main__':
    server_addr = ('chat.aistl.com', 9000)
    listen_port = randint(20000, 30000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # DGRAM -> UDP
    is_exit = False
    s.bind(('0.0.0.0', listen_port))
    l = Listener(s)
    l.start()
    print("listening at port:%d" % listen_port)
    is_exit = True
    try:
        while is_exit:
            cmd = input(">")
            s.sendto(cmd.encode(), server_addr)
    except KeyboardInterrupt:
        print("[sys err] user stop.")
    print("server exit.")
