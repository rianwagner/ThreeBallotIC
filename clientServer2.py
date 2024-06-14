import socket
import threading
import json
import uuid
import time

# Configurações
HOST = 'localhost'
PORT = 5002
NEXT_SERVER_PORT = 5003  # Porta do próximo servidor na cadeia

votos = {}  # Armazena os votos recebidos
votos_por_cliente = {}  # Armazena os clientes que já votaram

clientes_validos = {
    "12345": False,  # False indica que o cliente ainda não votou
    "67890": False,
    "11121": False
}

def generate_ballot():
    cedula_id = uuid.uuid4()
    cedula = {
        "id": str(cedula_id),
        "candidato A": "",
        "candidato B": "",
        "candidato C": ""
    }
    return json.dumps(cedula)

def send_ballots_to_next_server(cedula1, cedula2):
    try:
        next_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        next_server_socket.connect((HOST, NEXT_SERVER_PORT))
        payload = json.dumps({"cedula1": cedula1, "cedula2": cedula2})
        next_server_socket.sendall(payload.encode('utf-8'))
        response = next_server_socket.recv(1024).decode('utf-8')
        print(f"Resposta do próximo servidor: {response}")
        next_server_socket.close()
    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao próximo servidor na porta {NEXT_SERVER_PORT}")

def ballot_recv(connection):
    cedula1_json = connection.recv(1024).decode('utf-8')
    print(f"Cédula recebida do servidor 1: {cedula1_json}")
    return cedula1_json

def handle_client(connection):
    try:
        cedula1 = ballot_recv()

        # Recebe o ID do cliente
        client_id = connection.recv(1024).decode('utf-8').strip()
        print(f"ID do cliente recebido: {client_id}")

        if not client_id or client_id not in clientes_validos:
            connection.sendall("ID de cliente inválido.".encode('utf-8'))
            connection.close()
            return

        if votos_por_cliente.get(client_id, False):
            connection.sendall("Você já votou neste servidor.".encode('utf-8'))
            connection.close()
            return

        # Gera e envia uma nova cédula vazia
        cedula2 = generate_ballot()
        connection.sendall(cedula2.encode('utf-8'))

        # Recebe a cédula preenchida
        cedula2_json = connection.recv(1024).decode('utf-8')
        print(f"Cédula preenchida recebida do cliente: {cedula2_json}")
        cedula2 = json.loads(cedula2_json)

        if cedula2.get("candidato A", "") or cedula2.get("candidato B", "") or cedula2.get("candidato C", ""):
            votos_por_cliente[client_id] = True
            cedula_id = str(cedula2["id"])
            votos[cedula_id] = cedula2
            print(f"Voto registrado: {json.dumps(cedula2, indent=2)}")
            connection.sendall("Voto registrado com sucesso.".encode('utf-8'))

            # Envia ambas as cédulas para o próximo servidor
            send_ballots_to_next_server(cedula1, cedula2)
        else:
            connection.sendall("Cédula inválida no servidor 2.".encode('utf-8'))

    except Exception as e:
        print(f"Erro no servidor 2: {e}")
    finally:
        connection.close()

def server_task():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor 2 ouvindo em {HOST}:{PORT}")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Conexão de {client_address} no Servidor 2")
        threading.Thread(target=handle_client, args=(connection,)).start()

if __name__ == "__main__":

    threading.Thread(target=server_task).start()
