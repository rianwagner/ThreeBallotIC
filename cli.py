import socket
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Configurações dos servidores
servers = [
    ('127.0.0.1', 8001),
    ('127.0.0.1', 8002),
    ('127.0.0.1', 8003)
]

# Cria uma conexão para cada servidor e as mantem em uma lista
connections = []

for server_ip, server_port in servers:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    connections.append((server_ip, server_port, client_socket))

# Várias conexões abertas para diferentes servidores
for server_ip, server_port, client_socket in connections:
    print(f"Conectado ao servidor {server_ip}:{server_port}")

if server_ip == '127.0.0.1' and server_port == 8001:
        received_data = client_socket.recv(1024).decode('utf-8')
        print(f"Recebido do Servidor 1: {received_data}")
# Receber dados de cada servidor
for _, _, client_socket in connections:
    received_data = client_socket.recv(1024).decode('utf-8')
    print(f"Recebido: {received_data}")

for _, _, client_socket in connections:
    client_socket.close()
