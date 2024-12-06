import socket
import threading
from pathlib import Path

# Словарь для хранения клиентов и их адресов
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
        client.send("Welcome to the chat! Please enter your name: ".encode("utf-8"))
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    try:
        name = client.recv(1024).decode("utf-8")  # Получаем имя клиента
        welcome = f"Welcome {name}! If you ever want to quit, type 'quit' to exit."
        client.send(welcome.encode("utf-8"))
        
        msg = f"{name} has joined the chat!"
        broadcast(msg)  # Сообщаем всем клиентам, что новый пользователь присоединился
        clients[client] = name  # Добавляем клиента в список
        
        while True:
            try:
                msg = client.recv(1024).decode("utf-8")  # Ожидаем сообщение от клиента
                if msg.lower() == "quit":
                    client.send("Goodbye!".encode("utf-8"))
                    client.close()  # Закрываем соединение с клиентом
                    del clients[client]  # Удаляем клиента из списка
                    broadcast(f"{name} has left the chat.")  # Уведомляем остальных клиентов
                    break
                elif msg.startswith("FILE:"):  # Если это файл
                    file_name = msg.split(":", 1)[1]
                    receive_file(client, file_name)
                else:
                    broadcast(msg, name + ": ")  # Рассылаем сообщение всем остальным
            except ConnectionResetError:
                # Если соединение с клиентом потеряно, удаляем его из списка
                print(f"Connection lost with {name}")
                del clients[client]
                break
    except Exception as e:
        print(f"Error handling client: {e}")

# Функция для рассылки сообщений всем клиентам
def broadcast(msg, name=""):
    for sock in clients:
        sock.send((name + msg).encode("utf-8"))

# Функция для приема и сохранения файла
def handle_file_message(client, file_name):
    # Путь к файлу на сервере
    file_path = Path("received_files") / file_name
    file_url = f"http://localhost:10001/{file_name}"  # Пример ссылки для скачивания
    receive_file(client, file_path)  # Получаем и сохраняем файл
    # Отправляем ссылку на файл всем клиентам
    broadcast(f"File received: {file_url}", name="Server: ")

def receive_file(client, file_path):
    file_size = int(client.recv(1024).decode("utf-8"))
    with open(file_path, "wb") as file:
        while file_size > 0:
            data = client.recv(1024)
            file.write(data)
            file_size -= len(data)
    print(f"File {file_path} received successfully.")


# Запуск сервера
accept_thread = threading.Thread(target=accept_incoming_connections)
accept_thread.start()
accept_thread.join()
sock.close()
