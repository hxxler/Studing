import socket
import rsa
from rc2 import * 


def run_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")
        
        openkey,closekey = rsa.RSAopenCloseKey()
        P = 123
        rc2_P = RC2(bytearray(f'{P}', 'ascii'))
        #openkeyTemp = rc2_P.encrypt(bytearray(f'{openkey}','ascii'),MODE_ECB)
        #openkeyTemp = rc2_P.decrypt(openkeyTemp,MODE_ECB).decode(encoding='ascii')
        rc2_ok = RC2(bytearray(f'{openkey}', 'ascii'))
        #print("13 Ok:", rc2_ok.encrypt(bytearray(f"{13}",'ascii'),MODE_ECB))
        msg = bytearray(f'{openkey}', 'ascii')
        encrypted = rc2_P.encrypt(msg, MODE_ECB)
        print("openkeyorig",openkey)
        print("openkeyEnc",encrypted)
        print("Open key:",rc2_P.decrypt(encrypted,MODE_ECB).decode(encoding='ascii'))
        client_socket.send(encrypted)
        data = client_socket.recv(1024)
        print("Kenc:",data)
        K = rc2_ok.decrypt(rc2_P.decrypt(data,MODE_ECB),MODE_ECB).decode(encoding='ascii').split("\x00")[0]
        print("K:",int(K))
        rc2_K = RC2(bytearray(f'{K}', 'ascii'))
        encrypted = rc2_K.encrypt(bytearray('Its a Alice','ascii'),MODE_ECB)
        print("alice:",rc2_K.decrypt(encrypted,MODE_ECB).decode(encoding='ascii'))
        client_socket.send(encrypted)
        Ra = client_socket.recv(1024)
        Rb = client_socket.recv(1024)
        Ra = rc2_K.decrypt(Ra,MODE_ECB).decode(encoding='ascii').split("\x00")[0]
        Rb = rc2_K.decrypt(Rb,MODE_ECB).decode(encoding='ascii').split("\x00")[0]
        print(Ra,'+',Rb)
        if Ra != 'Its a Alice':
            print("error Ra")
            client_socket.close()
            return
        encrypted = rc2_K.encrypt(bytearray(f"{Rb}",'ascii'),MODE_ECB)
        client_socket.send(encrypted)
        serverMsg = client_socket.recv(1024).decode(encoding='ascii')

        while True:
            user_input = input("Enter characters: ")
            if user_input == "disconnect":
                user_input = rc2_K.encrypt(bytearray(f'{user_input}','ascii'),MODE_ECB)
                client_socket.send(user_input)
                break
            user_input = rc2_K.encrypt(bytearray(f'{user_input}','ascii'),MODE_ECB)
            client_socket.send(user_input)
            data = rc2_K.decrypt(client_socket.recv(1024),MODE_ECB).decode(encoding='ascii').split("\x00")[0] 
            print("Received:", data)
            if data == "Connection closed":
                break
        
        client_socket.close()
        print("Connection closed")

# Запуск клиента
run_client('localhost', 8000)
