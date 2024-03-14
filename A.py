import socket
import json
import uuid

num_cedulas = 3
cedulas = []

for _ in range(num_cedulas):
    cedula = {
        "Id": str(uuid.uuid4()),
        "Candidato A": 0,
        "Candidato B": 0,
        "Candidato C": 0,
        "Nulo": 0
    }
    cedulas.append(cedula)

def votar_candidato(cedula_id, candidato):
    for cedula in cedulas:
        if cedula["Id"] == cedula_id:
            if candidato in cedula:
                cedula[candidato] += 1
                return True
    return False

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 8002  # Porta para conexão

# Crie um socket do tipo IPv4 e TCP, bind e agaurde conexões
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("Servidor aguardando conexões...")

# Loop principal do servidor
while True:
    client_socket, addr = server_socket.accept()
    print(f"Conexão estabelecida com {addr}")

    try:
        # Recebe string JSON
        data = client_socket.recv(1024)
        data = data.decode('utf-8')

        # Analisa JSON
        request = json.loads(data)

        # Processamento da solicitação
        if request["action"] == "votar":
            cedulas = request.get("cedulas", [])
            for cedula in cedulas:
                cedula_id = cedula.get("Id")
                candidato = next((key for key, value in cedula.items() if value == 1), None)
                if cedula_id and candidato:
                    votar_candidato(cedula_id, candidato)

            # Resposta JSON 
            response = {"success": True}
        else:
            response = {"error": "Ação desconhecida"}

    except json.JSONDecodeError:
        response = {"error": "Solicitação inválida"}

    # Envio da resposta
    response_json = json.dumps(response)
    client_socket.send(response_json.encode('utf-8'))

    client_socket.close()
