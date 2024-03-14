import socket
import json
import uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Configurações do servidor B
HOST = 'localhost'  # Endereço IP do servidor B (localhost neste exemplo)
PORT = 12345  # Porta do servidor B

# Gere um par de chaves RSA (chave pública e chave privada)
key = RSA.generate(2048)
public_key = key.publickey()

# Crie um socket do tipo AF_INET (IPv4) e SOCK_STREAM (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faça o bind do socket com o endereço e porta
server_socket.bind((HOST, PORT))

# Espere por conexões de clientes
server_socket.listen()

print("Servidor B aguardando conexões...")

# Aceite a conexão do cliente
client_socket, addr = server_socket.accept()
print(f"Conexão estabelecida com {addr}")

# Gere as três cédulas
cedulas = []
for _ in range(3):
    cedula_id = str(uuid.uuid4())
    cedula = {
        "Id": cedula_id,
        "Candidato A": 0,
        "Candidato B": 0,
        "Candidato C": 0,
        "Nulo": 0
    }
    cedulas.append(cedula)

# Encripte os IDs das cédulas com a chave pública
cipher = PKCS1_OAEP.new(public_key)
for cedula in cedulas:
    cedula_id = cedula["Id"].encode('utf-8')
    cedula_id_encrypted = cipher.encrypt(cedula_id)
    cedula["Id"] = cedula_id_encrypted

# Envie as cédulas encriptadas e a chave pública para o cliente
response = {
    "cedulas": cedulas,
    "public_key": public_key.export_key().decode('utf-8')
}

response_json = json.dumps(response)
client_socket.send(response_json.encode('utf-8'))

# Feche a conexão com o cliente
client_socket.close()
