import os
import json
import time
import socket


class ScriptsRunServer:
    def __init__(self, files, output):
        self.files = files
        self.output = output
        self.start_time = time.strftime('%Y%m%d%H%M%S')

    def run_scripts(self, scripts):
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        for script in scripts:
            script_folder = os.path.join(self.output, script)
            if not os.path.exists(script_folder):
                os.makedirs(script_folder)

            output_file = os.path.join(script_folder, f"{self.start_time}.txt")
            with open(output_file, "a") as f:
                try:
                    result = os.popen(f"bash {script}").read()
                    f.write(f"Время запуска скрипта: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(result)
                    print(f'Скрипт {script} выполнен!')

                except Exception as e:
                    f.write(f"Ошибка запуска скрипта: {e}\n")

    def save_data(self, scripts):
        data = {"scripts": []}
        for script in scripts:
            script_data = {"name": script, "folder": os.path.join(self.output, script)}
            data["scripts"].append(script_data)
        with open(self.files, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.files):
            with open(self.files, "r") as f:
                data = json.load(f)
                return [script["name"] for script in data.get("scripts", [])]
        else:
            return []

    def main(self):
        scripts = self.load_data()
        print("Введите названия скриптов (по окончанию 'exit'): ")
        while True:
            script = input()
            if script.lower() == "exit":
                break
            if script not in scripts:
                scripts.append(script)

        self.save_data(scripts)

        n_iter = int(input('Сколько раз выполнить скрипты: '))
        for _ in range(n_iter):
            self.run_scripts(scripts)
            time.sleep(2)

    def start_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(1)
            print("Сервер запущен...")
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    data = conn.recv(1024)
                    if data.decode() == "get_scripts":
                        scripts = self.load_data()
                        conn.sendall(json.dumps(scripts).encode())
                    elif data.decode().startswith("add_script:"):
                        new_script = data.decode().split(":")[1]
                        scripts = self.load_data()
                        if new_script not in scripts:
                            scripts.append(new_script)
                            self.save_data(scripts)
                            conn.sendall("Скрипт успешно добавлен".encode('utf-8'))
                        else:
                            conn.sendall("Скрипт с таким названием уже добавлен".encode('utf-8'))
                    elif data.decode().startswith("create_file:"):
                        script_name = data.decode().split(":")[1]
                        scripts = self.load_data()
                        if script_name in scripts:
                            script_folder = os.path.join(self.output, script_name)
                            output_file_path = os.path.join(script_folder, f"total_{self.start_time}.txt")
                            output_content = ""
                            for file_name in os.listdir(script_folder):
                                file_path = os.path.join(script_folder, file_name)
                                with open(file_path, "r") as file:
                                    output_content += file.read() + "\n"
                            with open(output_file_path, "w") as output_file:
                                output_file.write(output_content)
                            conn.sendall(f"Файл для скрипта {script_name} успешно создан".encode('utf-8'))
                        else:
                            conn.sendall("Скрипт с таким названием не найден".encode('utf-8'))
                    else:
                        conn.sendall("Неправильное действие.".encode('utf-8'))


data_file = "script_data.json"
output_folder = "script_outputs"

run_server = ScriptsRunServer(data_file, output_folder)
run_server.main()
run_server.start_server('127.0.0.1', 65432)
