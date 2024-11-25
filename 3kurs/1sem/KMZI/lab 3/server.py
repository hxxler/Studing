import socket
import hashlib
import random

def generate_keys(p, q, g):
    x = random.randint(1, q - 1)
    y = pow(g, x, p)
    return x, y

def sign_message(p, q, g, x, message):
    k = random.randint(1, q - 1)
    r = pow(g, k, p) % q
    h = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    s = (pow(k, -1, q) * (h + x * r)) % q
    return r, s

def verify_signature(p, g, y, message, r, s, q):
    h = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    w = pow(s, -1, q)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p) % p) % q
    return v == r

def start_server():
    host = '127.0.0.1'
    port = 12345

    p = 23
    q = 11
    g = 5

    x, y = generate_keys(p, q, g)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server listening on {host}:{port}")

        conn, addr = server_socket.accept()

        with conn:
            print(f"Connected by {addr}")

            public_key = f"{p},{q},{g},{y}"
            conn.sendall(public_key.encode())

            print(f"Key exchange completed. Public key: {public_key}")

            while True:
                message = conn.recv(1024).decode()

                if not message:
                    break

                print(f"Received message: {message}")

                r, s = sign_message(p, q, g, x, message)
                signature = f"{r},{s}"
                conn.sendall(signature.encode())

if __name__ == "__main__":
    start_server()
