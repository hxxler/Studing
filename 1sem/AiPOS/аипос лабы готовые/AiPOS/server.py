import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))
print("Server started")

last_check = 0
all_messages = ""
start_time = time.time()  
end_time = None

while True:
    data, address = server_socket.recvfrom(1024)
    all_messages += data.decode()
    
    if len(all_messages) - last_check > 48:
        control_sum = sum(map(lambda char: ord(char), all_messages[last_check:last_check + 48]))
        print("Сумма: ", control_sum)
        print("Количество всех символов: ", len(all_messages))
        server_socket.sendto(f"!control_sum: {control_sum} {last_check}".encode(), address)
        server_socket.sendto(f"!control_len: {len(all_messages)}".encode(), address)
        last_check += 48
    
    if '~#~' in all_messages:
        server_socket.sendto(f"!close_connection".encode(), address)
        end_time = time.ctime()
        break

    print(data.decode())
    server_socket.sendto(data, address)

start_time = time.ctime(start_time)
end_time = time.ctime(end_time)

with open("log1.txt", "a") as file:
    file.write(f"Начало соединения: {start_time}\n")
    file.write(f"Окончание соединения: {end_time}\n")
    file.write(f"Продолжительность соединения: {end_time - start_time:.2f} сек\n")
