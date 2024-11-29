import socket
import threading
import tkinter as tk
from tkinter import filedialog

# Создаем сокет
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 10001))

# Функция для отправки сообщений
def send_message():
    msg = message_entry.get()
    client.send(msg.encode("utf-8"))
    message_entry.delete(0, tk.END)

# Функция для получения сообщений
def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            chat_box.insert(tk.END, msg + "\n")
        except:
            print("An error occurred!")
            client.close()
            break

# Функция для отправки файлов
def send_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        client.send(f"FILE:{file_name}".encode("utf-8"))
        with open(file_path, "rb") as file:
            file_size = os.path.getsize(file_path)
            client.send(str(file_size).encode("utf-8"))
            while file_size > 0:
                data = file.read(1024)
                client.send(data)
                file_size -= len(data)
        print(f"File {file_name} sent successfully.")

# Создание графического интерфейса
root = tk.Tk()
root.title("Chat")

chat_box = tk.Text(root)
chat_box.pack()

message_entry = tk.Entry(root)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

file_button = tk.Button(root, text="Send File", command=send_file)
file_button.pack()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()
