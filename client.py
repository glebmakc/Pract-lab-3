import socket  # Импортируем модуль для работы с сокетами

def run_client(host, port):  # Определяем функцию для запуска клиента с параметрами host (хост) и port (порт)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  # Создаем сокет для работы
        client_socket.connect((host, port))  # Устанавливаем соединение с указанным хостом и портом
        print("Соединение с сервером")

        while True:  # Запускаем бесконечный цикл для отправки и приема данных
            message = input("Введите сообщение для отправки серверу: ")
            if not message:  # Если сообщение пустое
                break  # Выходим из цикла
            print("Отправка данных серверу:", message)
            client_socket.sendall(message.encode())  # Отправляем сообщение серверу (преобразуем в байты перед отправкой)
            data = client_socket.recv(1024)  # Получаем ответ от сервера (не более 1024 байт)
            print("Прием данных от сервера:", data.decode())

    print("Разрыв соединения с сервером")

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Устанавливаем хост (локальный адрес)
    PORT = 12345  # Устанавливаем порт
    run_client(HOST, PORT)  # Запускаем клиент с указанным хостом и портом
