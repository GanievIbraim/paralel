import socket
import threading
from pathlib import Path

clients = {}

# Создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 10001))
sock.listen(5)
print("Waiting for connection...")

# Функция для приема входящих соединений
def accept_incoming_connections():
    while True:
        client, client_address = sock.accept()
        print(f"Connection from {client_address} has been established.")
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    try:
        # Обработка общения с клиентом
        while True:
            msg = client.recv(1024).decode("utf-8")
            if msg.lower().startswith("file:"):
                file_name = msg.split(":", 1)[1]
                send_file(client, file_name)
            elif msg.lower() == "quit":
                client.close()
                break
            else:
                broadcast(msg)
    except Exception as e:
        print(f"Error handling client: {e}")

def broadcast(msg):
    for sock in clients:
        sock.send(msg.encode("utf-8"))

def send_file(client, file_name):
    file_path = Path("received_files") / file_name
    if file_path.exists():
        file_size = file_path.stat().st_size
        client.send(f"FILE_SIZE:{file_size}".encode("utf-8"))  # Отправляем размер файла
        with open(file_path, "rb") as file:
            while file_size > 0:
                data = file.read(1024)
                client.send(data)
                file_size -= len(data)
        print(f"File {file_name} sent successfully.")
    else:
        client.send("FILE_NOT_FOUND".encode("utf-8"))

# Запуск сервера
accept_thread = threading.Thread(target=accept_incoming_connections)
accept_thread.start()
accept_thread.join()
sock.close()
