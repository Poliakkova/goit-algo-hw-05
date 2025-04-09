"""
Розробіть Python-скрипт для аналізу файлів логів.
Скрипт повинен вміти читати лог-файл, переданий як аргумент командного рядка,
і виводити статистику за рівнями логування наприклад, INFO, ERROR, DEBUG.
Також користувач може вказати рівень логування як другий аргумент командного рядка,
щоб отримати всі записи цього рівня.
"""
import sys
from collections import Counter
from colorama import Fore, init

init(autoreset=True)

def parse_log_line(line: str) -> dict:
    """
    парсинг рядків логу
    :param line: str
    :return: dict - словник з розібраними компонентами: дата, час, рівень, повідомлення
    """
    logs_dict = {}
    try:
        (logs_dict['date'],
         logs_dict['time'],
         logs_dict['level'],
         logs_dict['message']) = line.split(maxsplit=3)
    except ValueError:
        print(Fore.RED + f"Error parsing the line: {line}")
        return None
    return logs_dict


def load_logs(file_path: str) -> list:
    """
    завантаження логів з файлу
    :param file_path: str
    :return: list(dict()) - parsed logs
    """
    parsed_logs = []
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            # parsed_logs = map(parse_log_line, (line.strip() for line in file.readlines()))
            parsed_logs = [
                parsed for line in file.readlines()
                if line.strip()
                and (parsed := parse_log_line(line.strip())) # пройдуть лише не None рядки
            ]
    except FileNotFoundError:
        print(Fore.RED + "Error! No such file found")
    except IsADirectoryError:
        print(Fore.RED + "Error! Path is a directory, but file needed")
    except Exception as e:
        print(Fore.RED + f"Error! {e}")
    return parsed_logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    фільтрація логів за рівнем
    :param logs: list
    :param level: str
    :return: list - filtered logs by level
    """
    # filtered_logs = [log for log in logs if log['level'].lower() == level.lower()]
    filtered_logs = filter(lambda log: log['level'].lower() == level.lower(), logs)
    return list(filtered_logs)


def count_logs_by_level(logs: list) -> dict:
    """
    підрахунок записів за рівнем логування
    :param logs: list
    :return: dict - count of every level
    """
    counted_logs_by_level = Counter(map(lambda log: log['level'], logs))
    return dict(counted_logs_by_level)


def display_log_counts(counts: dict):
    """
    форматує та виводить результати підрахунку
    :param counts: dict
    """
    if len(counts) == 0:
        print(Fore.YELLOW + "No data found for display log counts")
        return
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    print("INFO             | ", counts.get('INFO', 0))
    print("DEBUG            | ", counts.get('DEBUG', 0))
    print("ERROR            | ", counts.get('ERROR', 0))
    print("WARNING          | ", counts.get('WARNING', 0))


def display_log_detail(logs:list):
    """
    форматує та виводить результати конкретного рівня, якщо потрібно
    :param logs:
    """
    if len(logs) == 0:
        print(Fore.YELLOW + "No data found for display log detail")
        return

    if len(sys.argv) == 3:
        filtered_logs = filter_logs_by_level(logs, sys.argv[2])
        print(f"\nДеталі логів для рівня '{sys.argv[2].upper()}':")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")


# (.venv) anastasiapolakova@MacBook-Air-Anastasia goit-algo-hw-05 % python task3.py logs.txt info
logs_list = load_logs(sys.argv[1])
log_counts = count_logs_by_level(logs_list)

display_log_counts(log_counts)
display_log_detail(logs_list)
