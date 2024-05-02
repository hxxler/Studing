import socket
import hashlib

def verify_signature(p, g, y, message, r, s, q):
    h = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    w = pow(s, -1, q)
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p) % p) % q
    return v == r

def start_client():
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        public_key = client_socket.recv(1024).decode()
        p, q, g, y = map(int, public_key.split(','))

        print(f"Key exchange completed. Public key: {public_key}")

        while True:
            message = input("Enter message (or 'exit' to quit): ")
            
            if message.lower() == 'exit':
                break

            print(f"Message to sign: {message}")
            client_socket.sendall(message.encode())

            signature = client_socket.recv(1024).decode()
            r, s = map(int, signature.split(','))

            print("Verifying signature...")
            result = verify_signature(p, g, y, message, r, s, q)

            if result:
                print("Signature is valid.")
            else:
                print("Signature is invalid.")

if __name__ == "__main__":
    start_client()
