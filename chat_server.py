# -*- coding: utf-8 -*-
'''
p2p server.
winxos 2015-12-04
'''
import socket
import threading
import os


class Listener(threading.Thread):
    def __init__(self, _s):
        threading.Thread.__init__(self)
        self.clients = {}
        self.messages = ""
        self.socket = _s
        self.is_exit = False

    def broadcast_except(self, data, except_addr):
        self.messages += "%s\n" % data
        for a in self.clients:
            if a != except_addr:
                self.socket.sendto(("%s" % data).encode(), a)

    def run(self):
        while not self.is_exit:
            try:
                data, addr = s.recvfrom(1024)
                data = data.decode('utf8')
                print("%s:%s" % (addr, data))
                if addr not in self.clients:
                    cmds = data.split()
                    if cmds[0] == "login":
                        name = cmds[1]
                        if str(name).strip() != "":
                            print("added %s" % name)
                            self.clients[addr] = name
                            self.broadcast_except("%s join." % name, addr)
                            self.socket.sendto(("welcome %s." % name).encode(), addr)
                            self.socket.sendto(("%s" % self.messages).encode(), addr)
                else:
                    if str(data).strip() != "":
                        self.broadcast_except(self.clients[addr] + ":" + data, "")

            except Exception as e:
                print("[listen err] %s" % e)


if __name__ == '__main__':
    port = 9000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # DGRAM -> UDP
    s.bind(('0.0.0.0', port))
    l = Listener(s)
    l.setDaemon(True)
    l.start()
    print("listening at port:%d" % port)
    is_exit = False
    try:
        while l.isAlive():
            pass
    except KeyboardInterrupt:
        print("[sys err] user stop.")
    is_exit = True
    print("server exit.")
    os._exit(0)
