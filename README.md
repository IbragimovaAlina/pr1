Эмулятор командной оболочки на Python

Это консольное приложение, эмулирующее работу командной строки UNIX-подобной операционной системы. Проект реализован на Python и включает в себя виртуальную файловую систему (VFS), работающую полностью в оперативной памяти.

Использование

Программа запускается из консоли.
При запуске программа сначала в интерактивном режиме спросит имя стартового скрипта.
Введите имя файла (например, myscript.esh), чтобы выполнить его.
Введите -, если стартовый скрипт не нужен, и вы хотите сразу перейти в интерактивный режим.


Виртуальная файловая система (VFS)

VFS описывается в файле формата JSON. Структура должна соответствовать следующему формату:
Каждый узел (файл или каталог) является объектом с полем "type".
Каталоги ("type": "directory") содержат поле "children", которое является словарем дочерних узлов.
Файлы ("type": "file") содержат поле "content" с содержимым, закодированным в Base64.

Поддерживаемые команды
1) ls [путь]

> Описание: Показывает содержимое каталога.
> Синтаксис: ls [путь]
> Пример: ls /home/user

2) cd <путь>

> Описание: Изменяет текущий рабочий каталог.
> Синтаксис: cd <путь>
> Пример: cd /home/user

3) mkdir [-p] <имя_каталога...>

> Описание: Создает один или несколько новых каталогов.
> Синтаксис: mkdir [-p] <имя_1> <имя_2> ...
> Опция -p: Позволяет создавать вложенные каталоги рекурсивно (например, mkdir -p a/b/c).
> Пример: mkdir new_folder

4) echo [текст...]

> Описание: Выводит переданный текст на экран.
> Синтаксис: echo [текст]
> Пример: echo Hello from the emulator!

5) tail [-n <число>] <файл>

> Описание: Выводит последние строки файла.
> Синтаксис: tail [-n <число>] <файл>
> Опция -n: Указывает количество выводимых строк. По умолчанию 10.
> Пример: tail -n 5 /home/user/readme.txt

6) clear

> Описание: Очищает экран терминала.
> Синтаксис: clear

7) vfs-init

> Описание: Сбрасывает VFS в памяти к пустому состоянию.
> Эта команда также удаляет физический JSON-файл, который был загружен при старте.
> Синтаксис: vfs-init

8) exit

> Описание: Завершает работу эмулятора.
> Синтаксис: exit

Примеры использования

Содержимое файла .esh:

echo "====== ЗАПУСК КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ ======"
echo "--> Тест раскрытия переменной окружения"
echo "Hello, $USER!"
echo "--> Тест обработки неизвестной команды"
this-is-not-a-real-command with args
echo "--> Сам факт выполнения этого скрипта уже тестирует функциональность Этапа 2."
echo "--> Начальное состояние VFS:"
ls
echo "--> Навигация (cd) (ls):"
cd /home/user/docs
ls
echo "--> Навигация вверх (cd ..):"
cd ../..
echo "--> Текущий каталог после cd ../.. :"
ls
echo "--> Тест ошибок VFS:"
ls /no/such/directory
cd /etc/os.conf
echo "--> Тест команды tail (по умолчанию 10 строк):"
tail /home/user/docs/report.txt
echo "--> Тест команды tail с флагом -n:"
tail -n 4 /home/user/docs/report.txt
echo "--> Тест ошибок команды tail:"
tail -n not_a_number /etc/os.conf
tail /home/user
echo "--> Тест команды clear:"
clear
echo "Экран был очищен. Но консоль PyCharm не поддерживает clear, поэтому были выведены просто пробелы."
cd /
echo "--> Тест mkdir:"
mkdir test_dir
echo "--> VFS после создания test_dir:"
ls
echo "--> Тест mkdir -p:"
mkdir -p /var/data/logs
echo "--> VFS после создания /var/data/logs:"
ls /var/data
echo "--> Тест ошибок mkdir:"
mkdir test_dir
mkdir /etc/os.conf/new
mkdir /no/such/parent/new_dir
echo "--> Финальное состояние VFS перед сбросом:"
ls
ls /var/data
echo "--> Тест vfs-init:"
vfs-init
echo "--> Состояние VFS после сброса:"
ls
echo "====== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ======"

VFS файл:
{
  "type": "directory",
  "children": {
    "home": {
      "type": "directory",
      "children": {
        "user": {
          "type": "directory",
          "children": {
            "docs": {
              "type": "directory",
              "children": {
                "report.txt": {
                  "type": "file",
                  "content": "QQpCCkMKRApFCkYKRwpICkkKSgpLCkwKTQpOCk8KUApRClIKUwpUClUKVgpXClgKWQpa="
                }
              }
            },
            "readme.txt": {
              "type": "file",
              "content": "UmVhZCBNRQ=="
            }
          }
        }
      }
    },
    "etc": {
      "type": "directory",
      "children": {
        "os.conf": {
          "type": "file",
          "content": "U0hFTEw9L2Jpbi9tc3No"
        }
      }
    }
  }
}

Вывод программы:
Enter the name of the file with the startup script (if you don't need it, enter
'-')
test_all.esh
VFS Path: C:\Users\Alina\PycharmProjects\pr_1_Ibragimova\vfs_max.json
Startup Script: test_all.esh
--------------------------------------------------
Running from script: test_all.esh
[vfs_max.json/]$ echo "====== ЗАПУСК КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ ======"
"====== ЗАПУСК КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ ======"
[vfs_max.json/]$ echo "--> Тест раскрытия переменной окружения"
"--> Тест раскрытия переменной окружения"
[vfs_max.json/]$ echo "Hello, $USER!"
"Hello, Alina!"
[vfs_max.json/]$ echo "--> Тест обработки неизвестной команды"
"--> Тест обработки неизвестной команды"
[vfs_max.json/]$ this-is-not-a-real-command with args
Error: command not found: this-is-not-a-real-command
[vfs_max.json/]$ echo "--> Сам факт выполнения этого скрипта уже тестирует функциональность Этапа 2."
"--> Сам факт выполнения этого скрипта уже тестирует функциональность Этапа 2."
[vfs_max.json/]$ echo "--> Начальное состояние VFS:"
"--> Начальное состояние VFS:"
[vfs_max.json/]$ ls
etc/
home/
[vfs_max.json/]$ echo "--> Навигация (cd) (ls):"
"--> Навигация (cd) (ls):"
[vfs_max.json/]$ cd /home/user/docs
[vfs_max.json/home/user/docs]$ ls
report.txt
[vfs_max.json/home/user/docs]$ echo "--> Навигация вверх (cd ..):"
"--> Навигация вверх (cd ..):"
[vfs_max.json/home/user/docs]$ cd ../..
[vfs_max.json/home]$ echo "--> Текущий каталог после cd ../.. :"
"--> Текущий каталог после cd ../.. :"
[vfs_max.json/home]$ ls
user/
[vfs_max.json/home]$ echo "--> Тест ошибок VFS:"
"--> Тест ошибок VFS:"
[vfs_max.json/home]$ ls /no/such/directory
ls: cannot access '/no/such/directory': No such file or directory
[vfs_max.json/home]$ cd /etc/os.conf
cd: not a directory: /etc/os.conf
[vfs_max.json/home]$ echo "--> Тест команды tail (по умолчанию 10 строк):"
"--> Тест команды tail (по умолчанию 10 строк):"
[vfs_max.json/home]$ tail /home/user/docs/report.txt
Q
R
S
T
U
V
W
X
Y
Z
[vfs_max.json/home]$ echo "--> Тест команды tail с флагом -n:"
"--> Тест команды tail с флагом -n:"
[vfs_max.json/home]$ tail -n 4 /home/user/docs/report.txt
W
X
Y
Z
[vfs_max.json/home]$ echo "--> Тест ошибок команды tail:"
"--> Тест ошибок команды tail:"
[vfs_max.json/home]$ tail -n not_a_number /etc/os.conf
tail: invalid number of lines: 'not_a_number'
[vfs_max.json/home]$ tail /home/user
tail: error reading '/home/user': Is a directory
[vfs_max.json/home]$ echo "--> Тест команды clear:"
"--> Тест команды clear:"
[vfs_max.json/home]$ clear



















































[vfs_max.json/home]$ echo "Экран был очищен. Но консоль PyCharm не поддерживает clear, поэтому были выведены просто пробелы."
"Экран был очищен. Но консоль PyCharm не поддерживает clear, поэтому были выведены просто пробелы."
[vfs_max.json/home]$ cd /
[vfs_max.json/]$ echo "--> Тест mkdir:"
"--> Тест mkdir:"
[vfs_max.json/]$ mkdir test_dir
[vfs_max.json/]$ echo "--> VFS после создания test_dir:"
"--> VFS после создания test_dir:"
[vfs_max.json/]$ ls
etc/
home/
test_dir/
[vfs_max.json/]$ echo "--> Тест mkdir -p:"
"--> Тест mkdir -p:"
[vfs_max.json/]$ mkdir -p /var/data/logs
[vfs_max.json/]$ echo "--> VFS после создания /var/data/logs:"
"--> VFS после создания /var/data/logs:"
[vfs_max.json/]$ ls /var/data
logs/
[vfs_max.json/]$ echo "--> Тест ошибок mkdir:"
"--> Тест ошибок mkdir:"
[vfs_max.json/]$ mkdir test_dir
mkdir: cannot create directory ‘test_dir’: File exists
[vfs_max.json/]$ mkdir /etc/os.conf/new
mkdir: cannot create directory ‘/etc/os.conf/new’: No such file or directory
[vfs_max.json/]$ mkdir /no/such/parent/new_dir
mkdir: cannot create directory ‘/no/such/parent/new_dir’: No such file or directory
[vfs_max.json/]$ echo "--> Финальное состояние VFS перед сбросом:"
"--> Финальное состояние VFS перед сбросом:"
[vfs_max.json/]$ ls
etc/
home/
test_dir/
var/
[vfs_max.json/]$ ls /var/data
logs/
[vfs_max.json/]$ echo "--> Тест vfs-init:"
"--> Тест vfs-init:"
[vfs_max.json/]$ vfs-init
Initializing VFS to default state.
Removed physical VFS file: C:\Users\Alina\PycharmProjects\pr_1_Ibragimova\vfs_max.json
VFS has been reset.
[vfs_max.json/]$ echo "--> Состояние VFS после сброса:"
"--> Состояние VFS после сброса:"
[vfs_max.json/]$ ls
[vfs_max.json/]$ echo "====== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ======"
"====== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ======"
Startup script finished

Welcome to the simple shell emulator! Type 'exit' to quit.
[vfs_max.json/]$
