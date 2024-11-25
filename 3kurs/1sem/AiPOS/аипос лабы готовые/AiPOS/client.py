from datetime import datetime
import socket
import threading
import keyboard
import pyautogui

file = open("log1.txt", 'a')

default_ip_address = 'localhost'
default_host = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

file.write(str(datetime.now()) + " --- connection to server\n")

FLAG = True

def press():
    while True:
        keyboard.wait('home')
        pyautogui.press('Enter')

def input_handler():
    global FLAG
    all_messages = ""
    start_time = datetime.now()  
    end_time = None
    server_address = ('localhost', 12345)
    while FLAG:
        command = input(">>> ")
        sent_time = datetime.now()  
        
        if '~#~' in command:
            client.sendto(command.encode(), server_address)
            file.write(f"Окончание соединения: {end_time}\n")
            file.write(str(datetime.now()) + " --- disconnect from server\n")
            break
        
        if 'disconnect' in command:
            client.sendto("!disconnect".encode(), server_address)
            FLAG = False
            file.write(f"Окончание соединения: {end_time}\n")
            file.write(str(datetime.now()) + " --- disconnect from server\n")
            file.close()
            break

        all_messages += command
        client.sendto(command.encode(), server_address)
        data, _ = client.recvfrom(1024)
        message = data.decode()
        
        if "!close_connection" in message:
            FLAG = False
            file.write(f"Окончание соединения: {end_time}\n")
            file.write(str(datetime.now()) + " --- disconnect from server\n")
            file.close()
            # client.close()  # Удалите эту строку
            break
        elif "!control_sum" in message:
            control_sum, last_check = int(message.split()[1]), int(message.split()[2])
            data, _ = client.recvfrom(1024)
            print("Сумма: ", control_sum)
            print("Количество всех символов: ", len(all_messages))
            if control_sum == sum(map(lambda char: ord(char), all_messages[last_check:last_check+48])) and len(all_messages) == int(data.decode().split()[1]):
                print("Сумма верная.")
            else:
                print("Сумма не верная.")
            data, _ = client.recvfrom(1024)
        
        file.write(f"Sent: {command} --- {sent_time}\n")
        print(f"Sent: {command} --- {sent_time}")
        file.write(message + f" --- {datetime.now()}\n")
        print(message)
    
    end_time = datetime.now() 

exit_thread = threading.Thread(target=press)
input_thread = threading.Thread(target=input_handler)

exit_thread.start()
input_thread.start()

exit_thread.join()
input_thread.join()

file.close()
