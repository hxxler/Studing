import socket
from rc2 import * 
import ast
def run_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection established from {addr}")
            
            P=123
            rc2_P = RC2(bytearray(f'{P}', 'ascii'))
            OpenKey = client_socket.recv(1024)
            print("openkeyEnc",OpenKey)
            OpenKey = rc2_P.decrypt(OpenKey,MODE_ECB).decode(encoding='ascii')
            print("openkey",OpenKey)
            K = 13
            OpenKey = OpenKey.split('\x00')[0]
            OpenKey = ast.literal_eval(OpenKey)
            rc2_Openkey = RC2(bytearray(f'{OpenKey}', 'ascii'))
            encrypted = rc2_Openkey.encrypt(bytearray(f'{K}', 'ascii'),MODE_ECB)
            print("btarr",bytearray(f'{K}', 'ascii'))
            print("K1",encrypted)
            encrypted = rc2_P.encrypt(encrypted,MODE_ECB)
            print("K2",encrypted)
            print(rc2_Openkey.decrypt(rc2_P.decrypt(encrypted,MODE_ECB),MODE_ECB))
            client_socket.send(encrypted)
            Ra = client_socket.recv(1024)
            Rb = "Its a Bob"
            rc2_K = RC2(bytearray(f'{K}', 'ascii'))
            Ra = rc2_K.decrypt(Ra,MODE_ECB).decode(encoding='ascii').split('\x00')[0]
            print(Ra)
            Ra = rc2_K.encrypt(bytearray(f'{Ra}', 'ascii'),MODE_ECB)
            Rb = rc2_K.encrypt(bytearray(f'{Rb}', 'ascii'),MODE_ECB)
            client_socket.send(Ra)
            client_socket.send(Rb)
            Rb = rc2_K.decrypt(client_socket.recv(1024),MODE_ECB).decode(encoding='ascii').split("\x00")[0]
            if Rb != "Its a Bob":
                print("error Rb")
                client_socket.send(("Error").encode(encoding='ascii'))
                client_socket.close()
            client_socket.send(("All Ok").encode(encoding='ascii'))
            data = client_socket.recv(1024)
            while data:
                enc = data
                data = rc2_K.decrypt(data,MODE_ECB).decode(encoding='ascii').split("\x00")[0]
                if data == 'disconnect': client_socket.close()
                
                client_socket.send(enc)
                data = client_socket.recv(1024)
            
            client_socket.close()
            print(f"Connection closed from {addr}")

# Запуск сервера
run_server('localhost', 8000)
