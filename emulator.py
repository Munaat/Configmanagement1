import sys
import tarfile
import tkinter as tk
from tkinter import scrolledtext


class FileSystem:
    def __init__(self, structure, username, file):
        self.structure = structure
        self.current_path = []
        self.username = username
        self.file = file

    def ls(self):
        current_dir = self._get_current_directory()
        output = []
        if current_dir is not None:
            for item in current_dir:
                if item != '':
                    output.append(item)
        else:
            output.append("Текущий путь не существует.")
        return output

    def cd(self, directory):
        output = []
        if directory == "..":
            if self.current_path:
                self.current_path.pop()
        elif directory in self._get_current_directory():
            self.current_path.append(directory)
        else:
            output.append(f"Директория '{directory}' не найдена.")
        output.append(self.username+":"+self.pwd()+">")
        return output

    def pwd(self):
        if self.current_path:
            return "/" + "/".join(self.current_path)
        else:
            return "/"

    def pwdmod(self):
        if self.current_path:
            return "/".join(self.current_path)
        else:
            return ""

    def du(self):
        total_size = 0
        current_dir_path = self.pwdmod()

        with tarfile.open(self.file, 'r') as tar:
            for member in tar.getmembers():
                # Проверяем, находится ли файл в текущей директории или в подкаталогах
                if member.name.startswith(current_dir_path):
                    total_size += member.size

        return total_size

    def _get_current_directory(self):
        current_dir = self.structure
        for dir_name in self.current_path:
            current_dir = current_dir.get(dir_name, None)
            if current_dir is None:
                return None
        return current_dir


def list_tar_contents(tar_file_path):
    try:
        with tarfile.open(tar_file_path, 'r') as tar:
            # Получаем список имён файлов в архиве
            file_names = tar.getnames()
            data = []
            for name in file_names:
                data.append(name)
            return data
    except FileNotFoundError:
        print(f"Файл {tar_file_path} не найден.")
    except tarfile.TarError:
        print(f"Ошибка при открытии tar-архива {tar_file_path}.")


def build_file_system_structure(paths):
    file_system = {}
    for path in paths:
        parts = path.split('/')
        current_level = file_system
        for part in parts:
            if '.' in part:  # Если в названии есть точка, это файл
                current_level[part] = None  # Добавляем файл как строку (или просто None)
                break  # Выходим из цикла, так как файл не имеет вложенных элементов
            else:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
    return file_system


class ConsoleEmulator:
    def __init__(self, root, fs, ss):
        self.root = root
        self.root.title("Консольная Эмуляция")

        self.fs = fs

        self.root.configure(bg='black')

        # Поле вывода
        self.output_field = tk.Text(root, height=25, width=100, bg='black', fg='green', font=('Courier New', 12))
        self.output_field.pack(pady=1)
        self.output_field.config(state=tk.DISABLED)

        # Поле ввода
        self.input_field = tk.Entry(root, width=100, bg='black', fg='green', font=('Courier New', 12))
        self.input_field.pack(pady=10)
        self.input_field.bind('<Return>', self.on_enter)

        self.input_field.focus()

        self.execute_commands_from_file(ss)

    def on_enter(self, event):
        self.process_input()

    def process_input(self):
        self.output_field.config(state=tk.NORMAL)
        user_input = self.input_field.get()
        self.output_field.insert(tk.END, f"{self.fs.username}:{self.fs.pwd()}> {user_input}\n")  # Отображение введенной команды
        self.input_field.delete(0, tk.END)  # Очистка поля ввода

        command = user_input.split()

        if command[0] == "cd":
            op = self.fs.cd(command[1])
            for el in op:
                self.output_field.insert(tk.END, el+'\n')

        if command[0] == "ls":
            op = self.fs.ls()
            for el in op:
                self.output_field.insert(tk.END, el + '\n')

        if command[0] == "du":
            self.output_field.insert(tk.END, str(self.fs.du()) + '\n')

        if command[0] == "who":
            users = [self.fs.username, "petya", "vasya"]
            for el in users:
                self.output_field.insert(tk.END, el + '\n')

        if command[0] == "whoami":
            self.output_field.insert(tk.END, self.fs.username + '\n')

        if command[0] == "exit":
            self.root.destroy()

        self.output_field.config(state=tk.DISABLED)

    def execute_commands_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                commands = f.readlines()
                for command in commands:
                    command = command.strip()
                    if command:  # Проверяем, что команда не пустая
                        self.output_field.insert(tk.END, f"{self.fs.username}:{self.fs.pwd()}> {command}\n")
                        self.process_command(command)
                        self.root.update()  # Обновляем интерфейс
        except FileNotFoundError:
            self.output_field.insert(tk.END, f"Файл {file_path} не найден.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Ошибка: {str(e)}\n")

    def process_command(self, command):
        self.output_field.config(state=tk.NORMAL)
        parts = command.split()
        if parts[0] == "cd":
            op = self.fs.cd(parts[1])
            for el in op:
                self.output_field.insert(tk.END, el + '\n')

        if parts[0] == "ls":
            op = self.fs.ls()
            for el in op:
                self.output_field.insert(tk.END, el + '\n')

        if parts[0] == "du":
            self.output_field.insert(tk.END, str(self.fs.du()) + '\n')

        if parts[0] == "who":
            users = [self.fs.username, "petya", "vasya"]
            for el in users:
                self.output_field.insert(tk.END, el + '\n')

        if parts[0] == "whoami":
            self.output_field.insert(tk.END, self.fs.username + '\n')

        if parts[0] == "exit":
            self.root.destroy()

        self.output_field.config(state=tk.DISABLED)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python emulator.py <username> <path_to_tar> <start_script>")
        sys.exit(1)
username = sys.argv[1]
tar_path = sys.argv[2]
start_script = sys.argv[3]

data = list_tar_contents(tar_path)
file_system_structure = build_file_system_structure(data)
fs = FileSystem(file_system_structure, username, tar_path)
root = tk.Tk()
console_emulator = ConsoleEmulator(root, fs, start_script)
root.mainloop()
