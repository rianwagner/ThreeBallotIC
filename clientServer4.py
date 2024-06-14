import socket
import threading

# Configurações
HOST = 'localhost'
PORT = 5004

# Função para o servidor
def server_task():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor 4 ouvindo em {HOST}:{PORT}")

    while True:
        connection, client_address = server_socket.accept()
        print(f"Conexão de {client_address} no Servidor 4")
        threading.Thread(target=handle_client, args=(connection,)).start()

def handle_client(connection):
    while True:
        data = connection.recv(1024)
        if data:
            print(f"Recebido no Servidor 4: {data.decode('utf-8')}")
            connection.sendall(data)
        else:
            break
    connection.close()

if __name__ == "__main__":
    # Inicia a thread do servidor
    threading.Thread(target=server_task).start()

