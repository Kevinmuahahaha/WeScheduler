#!/usr/bin/python
import socket

def listen_update( notified, q ):
    notify_listener = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    bind_ip = "127.0.0.5"
    bind_port = 9966
    notify_listener.bind((bind_ip, bind_port))
    notify_listener.listen(2)
    print("[*] Listener Bound to %s:%d" % (bind_ip, bind_port))
    print("[*] Ready for Connection.")
    while True:
        client_connection, client_addr = notify_listener.accept()
        print("[*] Received Connection From %s:%d" % ( client_addr[0], client_addr[1]))
        client_data = client_connection.recv(1024).decode('ascii')
        # decode the received binary data into ascii string
        if client_data.strip() == "recheck":
            print("[*] \tConfig Will be Rechecked.")
            notified = True
            q.put( notified )
        else:
            print("[-] \tCommand \'%s\' Unrecognized." % client_data.strip())

        client_connection.close()
