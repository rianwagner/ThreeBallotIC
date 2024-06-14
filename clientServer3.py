import socket
import threading
import json
import uuid

# Configurações
HOST = 'localhost'
PORT = 5003
NEXT_SERVER_PORT = 5004  # Porta do próximo servidor na cadeia

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

def send_ballots_to_next_server(cedula1, cedula2, cedula3):
    try:
        next_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        next_server_socket.connect((HOST, NEXT_SERVER_PORT))
        payload = json.dumps({"cedula1": cedula1, "cedula2": cedula2, "cedula3": cedula3})
        next_server_socket.sendall(payload.encode('utf-8'))
        response = next_server_socket.recv(1024).decode('utf-8')
        print(f"Resposta do próximo servidor: {response}")
        next_server_socket.close()
    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao próximo servidor na porta {NEXT_SERVER_PORT}")

def handle_client(connection):
    try:
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
        
        # Recebe a cédula do servidor anterior
        cedula1_json = connection.recv(1024).decode('utf-8')
        cedula2_json = connection.recv(1024).decode('utf-8')
        print(f"Cédula recebida do servidor 1: {cedula1_json}")
        print(f"Cédula recebida do servidor 2: {cedula2_json}")

        cedula1 = json.loads(cedula1_json)
        cedula2 = json.loads(cedula2_json)

        # Manda uma nova cédula vazia para o cliente
        cedula3 = generate_ballot()
        connection.sendall(cedula2.encode('utf-8'))

        # Recebe a cédula preenchida do cliente
        cedula3_json = connection.recv(1024).decode('utf-8')
        print(f"Cédula recebida do cliente: {cedula3_json}")
        cedula3 = json.loads(cedula3_json)

        if cedula3.get("candidato A", "") or cedula3.get("candidato B", "") or cedula3.get("candidato C", ""):
            votos_por_cliente[client_id] = True
            cedula_id = str(cedula3["id"])
            votos[cedula_id] = cedula3
            print(f"Voto registrado para a cédula {cedula_id}: {json.dumps(cedula3, indent=2)}")
            connection.sendall("Voto registrado com sucesso.".encode('utf-8'))

            # Envia ambas as cédulas para o próximo servidor
            send_ballots_to_next_server(cedula1, cedula2, cedula3)
        else:
            connection.sendall("Cédula inválida no servidor 3.".encode('utf-8'))

    except Exception as e:
        print(f"Erro no servidor 3: {e}")
    finally:
        connection.close()

# Função para o servidor
def server_task():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor 3 ouvindo em {HOST}:{PORT}")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Conexão de {client_address} no Servidor 3")
        threading.Thread(target=handle_client, args=(connection,)).start()

if __name__ == "__main__":
    # Inicia a thread do servidor
    threading.Thread(target=server_task).start()