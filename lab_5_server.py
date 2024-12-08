import socket
import threading
from pathlib import Path
import signal
import sys

clients = {}
addresses = {}

def accept_incoming_connections():
    while True:
        client, client_address = sock.accept()
        print(f"{client_address} has connected.")
        client.send(b"Welcome to the chat! Please type your name and press enter:")
        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(1024).decode("utf-8")
    welcome = f"Welcome {name}! If you ever want to quit, type /quit to exit."
    client.send(welcome.encode("utf-8"))
    msg = f"{name} has joined the chat!"
    broadcast(msg.encode("utf-8"))
    clients[client] = name

    while True:
        try:
            msg = client.recv(1024)
            if msg.startswith(b"/quit"):
                client.close()
                del clients[client]
                broadcast(f"{name} has left the chat.".encode("utf-8"))
                break
            elif msg.startswith(b"/file"):
                handle_file_upload(client, name, msg)
            elif msg.startswith(b"/download"):
                handle_file_download(client, msg)
            else:
                broadcast(f"{name}: {msg.decode('utf-8')}".encode("utf-8"))
        except UnicodeDecodeError:
            print("Received non-text data, ignoring.")

def handle_file_upload(client, name, msg):
    try:
        _, file_name, file_size = msg.split()
        file_size = int(file_size)
        file_path = Path("uploads") / file_name.decode("utf-8")
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as file:
            bytes_received = 0
            while bytes_received < file_size:
                data = client.recv(1024)
                file.write(data)
                bytes_received += len(data)

        broadcast(f"{name} has uploaded a file: {file_name.decode('utf-8')}".encode("utf-8"))
    except Exception as e:
        print(f"Error handling file upload: {e}")

def handle_file_download(client, msg):
    try:
        _, file_name = msg.split()
        file_path = Path("uploads") / file_name.decode("utf-8")
        if file_path.is_file():
            file_size = file_path.stat().st_size
            client.send(f"/file {file_name.decode('utf-8')} {file_size}".encode("utf-8"))
            with open(file_path, "rb") as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    client.send(data)
        else:
            client.send(b"File not found.")
    except Exception as e:
        print(f"Error handling file download: {e}")

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(prefix.encode("utf-8") + msg)

def signal_handler(sig, frame):
    print("\nShutting down the server...")
    sock.close()
    sys.exit(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 10001))
sock.listen(5)
print("Waiting for connections...")

signal.signal(signal.SIGINT, signal_handler)

accept_thread = threading.Thread(target=accept_incoming_connections)
accept_thread.start()
accept_thread.join()
sock.close()