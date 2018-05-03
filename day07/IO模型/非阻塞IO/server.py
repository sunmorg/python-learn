from socket import *
server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 8080))
server.listen(5)
server.setblocking(False)

rlist = []
wlist = []
while True:

    try:
        conn, addr = server.accept()
        rlist.append(conn)
        print(rlist)
    except BlockingIOError:
        del_rlist = []
        #收消息
        for conn in rlist:
            try:
                data = conn.recv(1024)
                if not data:
                    del_rlist.append(conn)
                    continue
                conn.send(data.upper())
            except BlockingIOError:
                continue
            except Exception:
                conn.close()


        for conn in del_rlist:
            rlist.remove(conn)


        #发消息
        del_wlist = []
        for item in wlist:
            try:
                conn = item[0]
                data = item[1]
                conn.send(data)
                del_wlist.append(item)
            except BlockingIOError:
                pass

        for item in del_wlist:
            wlist.remove(item)


server.close()

