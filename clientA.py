import socket
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Configurações do cliente
HOST = 'localhost'  # Endereço IP do servidor B (localhost neste exemplo)
PORT = 12345  # Porta do servidor B

# Crie um socket do tipo AF_INET (IPv4) e SOCK_STREAM (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecte-se ao servidor B
client_socket.connect((HOST, PORT))

# Receba as cédulas encriptadas e a chave pública do servidor B
data = client_socket.recv(4096)  # Tamanho do buffer pode ser ajustado conforme necessário
data = data.decode('utf-8')
received_data = json.loads(data)

# Carregue a chave pública do servidor B
public_key_data = received_data["public_key"]
public_key = RSA.import_key(public_key_data)

# Descriptografe os IDs nas cédulas
cipher = PKCS1_OAEP.new(public_key)
for cedula in received_data["cedulas"]:
    cedula_id_encrypted = cedula["Id"]
    cedula_id = cipher.decrypt(cedula_id_encrypted)

    # Atualize a cédula com o ID descriptografado
    cedula["Id"] = cedula_id.decode('utf-8')

# Exiba as cédulas com os IDs descriptografados
print("Cédulas recebidas do Servidor B:")
for cedula in received_data["cedulas"]:
    print(json.dumps(cedula, indent=4))

# Feche a conexão com o servidor B
client_socket.close()
