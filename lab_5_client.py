import socket
import threading
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext, filedialog, PhotoImage

def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            if msg.startswith("/file"):
                handle_file_download(msg)
            else:
                chat_window.config(state=tk.NORMAL)
                chat_window.insert(tk.END, msg + "\n")
                chat_window.config(state=tk.DISABLED)
                chat_window.yview(tk.END)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    if msg.startswith("/quit"):
        client_socket.send(msg.encode("utf-8"))
        client_socket.close()
        app.quit()
    elif msg.startswith("/file"):
        send_file(msg)
    elif msg.startswith("/download"):
        download_file()
    else:
        client_socket.send(msg.encode("utf-8"))

def send_file(msg):
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            file_path = Path(file_path)
            if file_path.is_file():
                file_size = file_path.stat().st_size
                client_socket.send(f"/file {file_path.name} {file_size}".encode("utf-8"))
                with open(file_path, "rb") as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        client_socket.send(data)
            else:
                print("File not found.")
    except Exception as e:
        print(f"Error sending file: {e}")

def download_file():
    file_name = filedialog.askopenfilename(initialdir="uploads", title="Select file to download")
    if file_name:
        client_socket.send(f"/download {Path(file_name).name}".encode("utf-8"))

def handle_file_download(msg):
    try:
        _, file_name, file_size = msg.split()
        file_size = int(file_size)
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")], initialfile=file_name)
        if save_path:
            with open(save_path, "wb") as file:
                bytes_received = 0
                while bytes_received < file_size:
                    data = client_socket.recv(1024)
                    file.write(data)
                    bytes_received += len(data)
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, f"File {file_name} downloaded.\n")
            chat_window.config(state=tk.DISABLED)
            chat_window.yview(tk.END)
    except Exception as e:
        print(f"Error handling file download: {e}")

def on_closing(event=None):
    my_msg.set("/quit")
    send()

app = tk.Tk()
app.title("Chat")

# Настройка стилей
app.geometry("400x500")
app.config(bg="#f4f4f9")  # Цвет фона окна

# Окно чата
chat_window = scrolledtext.ScrolledText(app, wrap=tk.WORD, height=15, width=50, bg="#eaeaea", fg="#333333", font=("Arial", 10), padx=10, pady=10)
chat_window.pack(padx=10, pady=10)
chat_window.config(state=tk.DISABLED)

# Текстовое поле для ввода сообщения
message_frame = tk.Frame(app, bg="#f4f4f9")  # Создаем контейнер для текстового поля
message_frame.pack(fill=tk.X, padx=10, pady=5)

my_msg = tk.StringVar()
my_msg.set("")
message_entry = tk.Entry(message_frame, textvariable=my_msg, width=50, font=("Arial", 12), bd=2, relief="solid")
message_entry.pack(fill=tk.X, padx=10, pady=5)
message_entry.bind("<Return>", send)

# Панель кнопок
button_frame = tk.Frame(app, bg="#f4f4f9")
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Кнопка отправки сообщения
send_icon = PhotoImage(file="send_icon.png")  # Укажите путь к иконке
send_button = tk.Button(button_frame, text="Send", image=send_icon, compound=tk.LEFT, command=send, 
                        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat", padx=10, pady=5)
send_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Кнопка отправки файла
file_icon = PhotoImage(file="file_icon.png")  # Укажите путь к иконке
file_button = tk.Button(button_frame, text="Send File", image=file_icon, compound=tk.LEFT, command=lambda: send_file("/file"), 
                        bg="#008CBA", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat", padx=10, pady=5)
file_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Кнопка скачивания файла
download_icon = PhotoImage(file="download_icon.png")  # Укажите путь к иконке
download_button = tk.Button(button_frame, text="Download File", image=download_icon, compound=tk.LEFT, command=download_file, 
                            bg="#FF5722", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat", padx=10, pady=5)
download_button.pack(side=tk.RIGHT, padx=10, pady=5)

app.protocol("WM_DELETE_WINDOW", on_closing)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 10001))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

app.mainloop()