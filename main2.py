import socket
import json


def send_command(commands, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        for command in commands:
            client_socket.sendall(command.encode())
        data = b''
        while True:
            response = client_socket.recv(1024)
            if not response:
                break
            data += response
        return data


def main():
    host = '127.0.0.1'
    port = 65432

    while True:
        print("\nВыберите действие:")
        print("1. Получить список скриптов")
        print("2. Добавить новый скрипт")
        print("3. Создать файл со всеми запусками скрипта")
        print("4. Выход")
        choice = input("Ваш выбор: ")

        if choice == "1":
            scripts = send_command(["get_scripts"], host, port)
            print("Список скриптов:")
            for script in json.loads(scripts):
                print(script)
        elif choice == "2":
            new_script = input("Введите название нового скрипта: ")
            response = send_command([f"add_script:{new_script}"], host, port)
            print(response.decode())
        elif choice == "3":
            script_name = input("Введите название скрипта, для которого создать файл: ")
            response = send_command([f"create_file:{script_name}"], host, port)
            print(response.decode())
        elif choice == "4":
            break
        else:
            print("Неверный выбор")


main()
