import socket
import json

# Configurações
HOST = 'localhost'
PORT = [5001, 5002, 5003, 5004]

def vote_on_server(port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, port))

        # Solicita o ID do cliente para este servidor
        client_id = input(f"Digite seu ID de cliente para o servidor {port}: ")

        # Envia o ID do cliente
        client_socket.sendall(client_id.encode('utf-8'))

        # Recebe a cédula vazia do servidor
        cedula_json = client_socket.recv(1024).decode('utf-8')
        print(f"Cédula recebida do servidor {PORT}: {cedula_json}")
        cedula = json.loads(cedula_json)

        # Preenche a cédula
        print("Digite 1 para o candidato escolhido e 0 para os outros.")
        cedula["candidato A"] = input("Digite o seu voto para o candidato A: ")
        cedula["candidato B"] = input("Digite o seu voto para o candidato B: ")
        cedula["candidato C"] = input("Digite o seu voto para o candidato C: ")

        # Envia a cédula preenchida
        client_socket.sendall(json.dumps(cedula).encode('utf-8'))

        # Recebe a confirmação
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

    except Exception as e:
        print(f"Erro no cliente ao conectar no servidor {port}: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
     for port in PORT:
        vote_on_server(port)
    
     print("Processo de votação concluído.")
