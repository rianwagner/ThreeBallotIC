import socket
import json
import uuid

# Exibir as cédulas do usuário
def exibir_cedulas(cedulas):
    print("\nCédulas do usuário:")
    for i, cedula in enumerate(cedulas):
        print(f"Cédula {i + 1}: {json.dumps(cedula, indent=4)}")

# Configurações do cliente
HOST = 'localhost'  #IP do servidor
PORT = 12345  #Porta do servidor

# Criar socket do tipo IPv4 e TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
client_socket.connect((HOST, PORT))

# IDs de cédulas
cedula_ids = [str(uuid.uuid4()) for _ in range(3)]

# Voto, confirmação do voto e comunicação com o servidor
candidato_escolhido = input("Escolha o candidato (A, B ou C) ou vote NULO: ").strip().upper()
if candidato_escolhido not in ["A", "B", "C", "NULO"]:
    print("Opção de candidato inválida. Escolha entre os candidatos validos ou vote NULO!, .")
else:
    cedulas = []
    for cedula_id in cedula_ids:
        if len(cedulas) < 2:
            cedula = {
                "Id": cedula_id,
                "Candidato A": 0,
                "Candidato B": 0,
                "Candidato C": 0,
                "Nulo": 0
            }
            cedula[f"Candidato {candidato_escolhido}"] = 1
            cedulas.append(cedula)
        else:
            cedulas.append({
                "Id": cedula_id,
                "Candidato A": 0,
                "Candidato B": 0,
                "Candidato C": 0,
                "Nulo": 0
            })

    confirmacao = input("\nConfirmar o voto? (S para confirmar, qualquer outra tecla para cancelar): ").strip().upper()
    if confirmacao == "S":
        # Solicitação para enviar as cédulas para o servidorA
        request = {
            "action": "votar",
            "cedulas": cedulas
        }

        # Solicitação JSON para o servidorA
        request_json = json.dumps(request)
        client_socket.send(request_json.encode('utf-8'))

        # Resposta
        response_data = client_socket.recv(1024)
        response = json.loads(response_data.decode('utf-8'))
        if "success" in response and response["success"]:
            print("Votos registrados com sucesso.")
        else:
            print("Erro ao registrar os votos.")
    else:
        print("Voto cancelado.")

    exibir_cedulas(cedulas)

client_socket.close()
