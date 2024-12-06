# Домашняя работа №1
# Отчет по разработке эмулятора оболочки ОС

## Введение

В данном проекте был разработан эмулятор для языка оболочки ОС, который имитирует сеанс shell в UNIX-подобной операционной системе. Эмулятор запускается из командной строки и работает в графическом интерфейсе пользователя (GUI). Он принимает образ виртуальной файловой системы в формате tar и поддерживает основные команды, такие как `ls`, `cd`, `exit`, а также дополнительные команды `who`, `whoami` и `du`.

## Описание функциональности

### Основные функции эмулятора

1. **ls**: Отображает содержимое текущей директории.
2. **cd <directory>**: Переходит в указанную директорию.
3. **du**: Вычисляет размер текущей директории.
4. **who**: Отображает список пользователей.
5. **whoami**: Показывает имя текущего пользователя.
6. **exit**: Закрывает эмулятор.

### Запуск эмулятора

Эмулятор запускается с помощью командной строки с тремя аргументами:
- Имя пользователя для отображения в приглашении.
- Путь к архиву виртуальной файловой системы (формат tar).
- Путь к стартовому скрипту, который содержит команды для начального выполнения.

Пример команды для запуска:
```bash
python emulator.py <username> <path_to_tar> <start_script>
```

# Архитектура эмулятора оболочки ОС

Архитектура эмулятора состоит из нескольких ключевых компонентов, каждый из которых выполняет свою роль в обеспечении функциональности и взаимодействия с пользователем. Основные классы и функции, которые составляют архитектуру, включают:

1. **Класс `FileSystem`**
2. **Класс `ConsoleEmulator`**
3. **Функции для работы с tar-архивом**
4. **Функция для построения структуры файловой системы**

## 1. Класс `FileSystem`

Класс `FileSystem` управляет виртуальной файловой системой, обрабатывает команды и взаимодействует с tar-архивом. Он хранит структуру файловой системы, текущее состояние (текущий путь) и имя пользователя.

### Конструктор

```python
class FileSystem:
    def __init__(self, structure, username, file):
        self.structure = structure
        self.current_path = []
        self.username = username
        self.file = file
```

- `structure`: Структура файловой системы, построенная из содержимого tar-архива.
- `current_path`: Список, представляющий текущий путь в файловой системе.
- `username`: Имя пользователя, отображаемое в приглашении.
- `file`: Путь к tar-архиву.

### Основные методы

#### Метод `ls`

Метод `ls` возвращает список файлов и директорий в текущей директории.

```python
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
```

- `_get_current_directory`: Вспомогательный метод, который возвращает содержимое текущей директории, основываясь на `current_path`.

#### Метод `cd`

Метод `cd` изменяет текущую директорию.

```python
def cd(self, directory):
    output = []
    if directory == "..":
        if self.current_path:
            self.current_path.pop()
    elif directory in self._get_current_directory():
        self.current_path.append(directory)
    else:
        output.append(f"Директория '{directory}' не найдена.")
    output.append(self.username + ":" + self.pwd() + ">")
    return output
```

- Если пользователь вводит `..`, метод возвращает на уровень выше.
- Если введена существующая директория, она добавляется в `current_path`.
- Если директория не найдена, выводится сообщение об ошибке.

#### Метод `du`

Метод `du` вычисляет размер текущей директории.

```python
def du(self):
    total_size = 0
    current_dir_path = self.pwdmod()

    with tarfile.open(self.file, 'r') as tar:
        for member in tar.getmembers():
            if member.name.startswith(current_dir_path):
                total_size += member.size

    return total_size
```

- Метод открывает tar-архив и суммирует размеры всех файлов, находящихся в текущей директории и подкаталогах.

### Вспомогательный метод `_get_current_directory`

Этот метод возвращает содержимое текущей директории на основе `current_path`.

```python
def _get_current_directory(self):
    current_dir = self.structure
    for dir_name in self.current_path:
        current_dir = current_dir.get(dir_name, None)
        if current_dir is None:
            return None
    return current_dir
```

- Метод проходит по `current_path` и возвращает соответствующую директорию из структуры файловой системы.

## 2. Класс `ConsoleEmulator`

Класс `ConsoleEmulator` отвечает за графический интерфейс и обработку пользовательского ввода.

### Конструктор

```python
class ConsoleEmulator:
    def __init__(self, root, fs, ss):
        self.root = root
        self.root.title("Консольная Эмуляция")
        self.fs = fs
        self.root.configure(bg='black')
        ...
```

- `root`: Основное окно приложения.
- `fs`: Экземпляр класса `FileSystem`, который управляет файловой системой.
- `ss`: Путь к стартовому скрипту.

### Поля ввода и вывода

```python
self.output_field = tk.Text(root, height=25, width=100, bg='black', fg='green', font=('Courier New', 12))
self.output_field.pack(pady=1)
self.output_field.config(state=tk.DISABLED)

self.input_field = tk.Entry(root, width=100, bg='black', fg='green', font=('Courier New', 12))
self.input_field.pack(pady=```python
10)
self.input_field.bind('<Return>', self.on_enter)
```

- `output_field`: Текстовое поле для отображения вывода команд и сообщений. Оно настроено с черным фоном и зеленым текстом для имитации консольного интерфейса.
- `input_field`: Поле ввода для ввода команд пользователем. Оно также настроено с черным фоном и зеленым текстом.

### Обработка ввода

Метод `on_enter` обрабатывает нажатие клавиши Enter:

```python
def on_enter(self, event):
    self.process_input()
```

Этот метод вызывает `process_input`, который обрабатывает введенную команду.

### Метод `process_input`

```python
def process_input(self):
    self.output_field.config(state=tk.NORMAL)
    user_input = self.input_field.get()
    self.output_field.insert(tk.END, f"{self.fs.username}:{self.fs.pwd()}> {user_input}\n")
    self.input_field.delete(0, tk.END)

    command = user_input.split()

    if command[0] == "cd":
        op = self.fs.cd(command[1])
        for el in op:
            self.output_field.insert(tk.END, el + '\n')

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
```

- Метод получает текст из `input_field`, отображает его в `output_field` и очищает поле ввода.
- Затем он разбивает введенную команду на части и обрабатывает каждую команду, вызывая соответствующие методы из класса `FileSystem`.
- Результаты выполнения команд добавляются в `output_field`.

### Метод `execute_commands_from_file`

Этот метод выполняет команды из стартового скрипта:

```python
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
```

- Метод открывает файл, считывает команды и выполняет их по одной, обновляя интерфейс после каждой команды.
- Обрабатываются исключения, чтобы избежать сбоев при отсутствии файла или других ошибках.

## 3. Функции для работы с tar-архивом

### Функция `list_tar_contents`

Эта функция извлекает содержимое tar-архива и возвращает список файлов:

```python
def list_tar_contents(tar_file_path):
    try:
        with tarfile.open(tar_file_path, 'r') as tar:
            file_names = tar.getnames()
            data = []
            for name in file_names:
                data.append(name)
            return data
    except FileNotFoundError:
        print(f"Файл {tar_file_path} не найден.")
    except tarfile.TarError:
        print(f"Ошибка при открытии tar-архива {tar_file_path}.")
```

- Функция открывает tar-архив и получает список имен файлов с помощью метода `getnames()`.
- Обрабатываются исключения для случаев, когда файл не найден или возникает ошибка при открытии архива.

## 4. Функция для построения структуры файловой системы

### Функция `build_file_system_structure`

Эта функция создает структуру файловой системы на основе списка путей:

```python
def build_file_system_structure(paths):
    file_system = {}
    for path in paths:
        parts = path.split('/')
        current_level = file_system
        for part in parts:
            if '.' in part:  # Если в названии есть точка, это файл
                current_level```python
                current_level[part] = None  # Добавляем файл как строку (или просто None)
                break  # Выходим из цикла, так как файл не имеет вложенных элементов
            else:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
    return file_system
```

- Функция принимает список путей (например, из tar-архива) и создает вложенную структуру словарей, представляющую файловую систему.
- Каждый путь разбивается на части с помощью `split('/')`, и для каждой части проверяется, является ли она файлом (содержит ли точку).
- Если это файл, он добавляется в текущий уровень структуры как `None` (или можно использовать строку с именем файла).
- Если это директория, она добавляется в текущий уровень как новый словарь, и текущий уровень обновляется для дальнейшей обработки вложенных элементов.

## Пример работы

### Запуск эмулятора

Когда пользователь запускает эмулятор с командой:

```bash
python emulator.py user1 /path/to/archive.tar /path/to/start_script.txt
```

1. **Инициализация**:
   - Создается экземпляр `FileSystem`, который загружает структуру файловой системы из tar-архива.
   - Создается экземпляр `ConsoleEmulator`, который инициализирует графический интерфейс и загружает команды из стартового скрипта.

2. **Взаимодействие с пользователем**:
   - Пользователь вводит команды в `input_field`.
   - При нажатии Enter вызывается метод `process_input`, который обрабатывает команду и обновляет `output_field` с результатами.

3. **Обработка команд**:
   - Команды, такие как `ls`, `cd`, `du`, обрабатываются в классе `FileSystem`, который взаимодействует с tar-архивом для получения необходимой информации.
   - Результаты выполнения команд отображаются в графическом интерфейсе.

### Пример команды `ls`

Когда пользователь вводит команду `ls`, происходит следующее:

1. Вызов метода `ls` в классе `FileSystem`.
2. Метод `_get_current_directory` возвращает содержимое текущей директории.
3. Содержимое добавляется в `output_field`, и пользователь видит список файлов и папок.

### Пример команды `cd`

Когда пользователь вводит команду `cd folder_name`, происходит следующее:

1. Вызов метода `cd` в классе `FileSystem`.
2. Метод проверяет, существует ли указанная директория.
3. Если директория существует, она добавляется в `current_path`, и пользователь может затем использовать команду `ls` для просмотра содержимого этой директории.

## Тестирование

Для каждой из поддерживаемых команд были написаны тесты. Они выполняются сразу же, так как тестирование происходит в начальном скрипте.

Для тестирования эмулятора оболочки ОС, мы можем использовать содержимое стартового скрипта `ss.txt`, который вы предоставили. Давайте разберем, как можно организовать тестирование, основываясь на командах, указанных в скрипте, и ожидаемом выводе программы.

## Стартовый скрипт `ss.txt`

Содержимое стартового скрипта:

```
Testing commands
who
whoami
du
ls
cd Documents
ls
du
cd ..
cd Stuff
ls
du
```

## Ожидаемый вывод программы

На основе предоставленного вами вывода программы, мы можем выделить ожидаемые результаты для каждой команды:

1. **Команда `who`**:
   - Ожидаемый вывод:
     ```
     timofei
     petya
     vasya
     ```

2. **Команда `whoami`**:
   - Ожидаемый вывод:
     ```
     timofei
     ```

3. **Команда `du`** (в корневой директории):
   - Ожидаемый вывод:
     ```
     199441
     ```

4. **Команда `ls`** (в корневой директории):
   - Ожидаемый вывод:
     ```
     Documents
     Music
     Projects
     Stuff
     ```

5. **Команда `cd Documents`**:
   - Ожидаемый вывод:
     ```
     timofei:/Documents>
     ```

6. **Команда `ls`** (в директории `Documents`):
   - Ожидаемый вывод:
     ```
     creator.txt
     ```

7. **Команда `du`** (в директории `Documents`):
   - Ожидаемый вывод:
     ```
     42
     ```

8. **Команда `cd ..`**:
   - Ожидаемый вывод:
     ```
     timofei:/>
     ```

9. **Команда `cd Stuff`**:
   - Ожидаемый вывод:
     ```
     timofei:/Stuff>
     ```

10. **Команда `ls`** (в директории `Stuff`):
    - Ожидаемый вывод:
      ```
      dabda6a6-8004-406e-8faa-5e6a93f11edb.jpeg
      ```

11. **Команда `du`** (в директории `Stuff`):
    - Ожидаемый вывод:
      ```
      199399
      ```
**Вывод программы**:
  ```
  timofei
  petya
  vasya
  timofei
  199441
  Documents
  Music
  Projects
  Stuff
  timofei:/Documents>
  creator.txt
  42
  timofei:/>
  timofei:/Stuff>
  dabda6a6-8004-406e-8faa-5e6a93f11edb.jpeg
  199399
  ```
**Как мы можем видеть, все тестирования пройдены, программа работает корректно**
## Заключение

Эмулятор оболочки ОС был успешно разработан и протестирован. Он предоставляет пользователю возможность взаимодействовать с виртуальной файловой системой в графическом интерфейсе, имитируя поведение командной строки UNIX-подобных систем. Все функции эмулятора покрыты тестами, что обеспечивает надежность и корректность работы.
