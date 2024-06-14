import socket
import threading
import json
import uuid

# Configurações
HOST = 'localhost'
PORT = 5001
NEXT_SERVER_PORT = 5002  # Porta do próximo servidor na cadeia

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

def send_ballot_to_next_server(cedula):
    try:
        next_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        next_server_socket.connect((HOST, NEXT_SERVER_PORT))
        next_server_socket.sendall(json.dumps(cedula).encode('utf-8'))
        next_server_socket.close()
    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao próximo servidor na porta {NEXT_SERVER_PORT}")

def handle_client(connection):
    try:
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

        # Manda uma cédula vazia para o cliente
        cedula = generate_ballot()
        connection.sendall(cedula.encode('utf-8'))

        # Recebe a cédula preenchida do cliente
        cedula_json = connection.recv(1024).decode('utf-8')
        print(f"Cédula recebida do cliente: {cedula_json}")
        cedula = json.loads(cedula_json)

        if cedula.get("candidato A", "") or cedula.get("candidato B", "") or cedula.get("candidato C", ""):
            votos_por_cliente[client_id] = True
            cedula_id = str(cedula["id"])
            votos[cedula_id] = cedula
            print(f"Voto registrado para a cédula {cedula_id}: {json.dumps(cedula, indent=2)}")
            connection.sendall("Voto registrado com sucesso.".encode('utf-8'))

            # Envia a cédula preenchida para o próximo servidor
            send_ballot_to_next_server(cedula)
        else:
            connection.sendall("Cédula inválida.".encode('utf-8'))

    except Exception as e:
        print(f"Erro no servidor 1: {e}")
    finally:
        connection.close()

def server_task():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor 1 ouvindo em {HOST}:{PORT}")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Conexão de {client_address} no Servidor 1")
        threading.Thread(target=handle_client, args=(connection,)).start()

if __name__ == "__main__":
    threading.Thread(target=server_task).start()
