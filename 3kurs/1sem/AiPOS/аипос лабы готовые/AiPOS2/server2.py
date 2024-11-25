import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
user_socket, address = server_socket.accept()
print("user connected")

last_check = 0
all_messages = ""
start_time = time.time()  
end_time = None

while True:
    data = user_socket.recv(1024)
    all_messages += data.decode()
    if len(all_messages) - last_check > 48:
        control_sum = sum(map(lambda char: ord(char), all_messages[last_check:last_check + 48]))
        print("Сумма: ", control_sum)
        print("Количество всех символов: ", len(all_messages))
        user_socket.send(f"!control_sum: {control_sum} {last_check}".encode())
        user_socket.send(f"!control_len: {len(all_messages)}".encode())
        last_check += 48
    if '~#~' in all_messages:
        user_socket.send(f"!close_connection".encode())
        end_time = time.ctime()
        user_socket.close()
        break
    print(data.decode())
    user_socket.send(data)

start_time = time.ctime(start_time)
end_time = time.ctime(end_time)

with open("log.txt", "a") as file:
    file.write(f"Начало соединения: {start_time}\n")
    file.write(f"Окончание соединения: {end_time}\n")
    file.write(f"Продолжительность соединения: {end_time - start_time:.2f} сек\n")
