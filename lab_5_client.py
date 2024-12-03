import socket
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage

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

# Настройка стилей
root.geometry("400x500")
root.config(bg="#f4f4f9")  # Цвет фона окна

# Окно чата
chat_box = tk.Text(root, wrap=tk.WORD, height=15, width=50, bg="#eaeaea", fg="#333333", font=("Arial", 10), padx=10, pady=10)
chat_box.pack(padx=10, pady=10)

# Текстовое поле для ввода сообщения
message_frame = tk.Frame(root, bg="#f4f4f9")  # Создаем контейнер для текстового поля
message_frame.pack(fill=tk.X, padx=10, pady=5)

message_entry = tk.Entry(message_frame, width=50, font=("Arial", 12), bd=2, relief="solid")
message_entry.pack(fill=tk.X, padx=10, pady=5)

# Панель кнопок
button_frame = tk.Frame(root, bg="#f4f4f9")
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Кнопка отправки сообщения
send_icon = PhotoImage(file="send_icon.png")  # Укажите путь к иконке
send_button = tk.Button(button_frame, text="Send", image=send_icon, compound=tk.LEFT, command=send_message, 
                        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat", padx=10, pady=5)
send_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Кнопка отправки файла
file_icon = PhotoImage(file="file_icon.png")  # Укажите путь к иконке
file_button = tk.Button(button_frame, text="Send File", image=file_icon, compound=tk.LEFT, command=send_file, 
                        bg="#008CBA", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat", padx=10, pady=5)
file_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Запуск потока для получения сообщений
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

root.mainloop()
