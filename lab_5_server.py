import socket
import threading
import os

# Словарь для хранения клиентов и их адресов
clients = {}
addresses = {}

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
        addresses[client] = client_address
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

# Функция для приема файлов
def receive_file(client, file_name):
    file_size = int(client.recv(1024).decode("utf-8"))
    with open(file_name, "wb") as file:
        while file_size > 0:
            data = client.recv(1024)
            file.write(data)
            file_size -= len(data)
    print(f"File {file_name} received successfully.")

# Запуск сервера
accept_thread = threading.Thread(target=accept_incoming_connections)
accept_thread.start()
accept_thread.join()
sock.close()
