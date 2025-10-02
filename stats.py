import json
import sys
import os
from constants import SHAPE_NAMES


def get_app_data_path():
    # Возвращает путь к директории для хранения данных приложения
    if getattr(sys, 'frozen', False):
        # Если выполнение в исполняемом файле:
        if sys.platform == 'win32': # Для винды
            appdata_path = os.environ.get('APPDATA')
            if appdata_path:
                app_folder = os.path.join(appdata_path, "Ellatris")
            else:
                app_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Ellatris")
        elif sys.platform == 'darwin': # Для Mac
            app_folder = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Ellatris")
        else: # Для Linux
            app_folder = os.path.join(os.path.expanduser("~"), ".config", ".ellatris")
    else: # Если запущено из IDE напрямую
        app_folder = os.path.dirname(os.path.abspath(__file__))

    # Создание папки, если отсутствует
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)

    return app_folder

def get_stats_file_path():
    # Возврат полного пути к файлу статистики
    app_folder = get_app_data_path()
    return os.path.join(app_folder, "ellatris_stats.json")

#def get_resource_path(relative_path):
#    # Получает абсолютный путь к ресурсу, работает для dev и для PyInstaller
#    try:
#        # PyInstaller создает временную папку и хранит путь в _MEIPASS
#        base_path = sys._MEIPASS
#    except Exception:
#        base_path = os.path.abspath(".")
#
#    return os.path.join(base_path, relative_path)

def load_stats():
    stats_file_path = get_stats_file_path()
    # Загрузка статистики из файла
    stats = {
        "total_pieces": 0,
        "pieces": {name: 0 for name in SHAPE_NAMES},
        "games_played": 0,
        "total_score": 0,
        "max_score": 0
    }

    if os.path.exists(stats_file_path):
        try:
            with open(stats_file_path, 'r', encoding='utf-8') as f:
                saved_stats = json.load(f)
                stats.update(saved_stats)
        except (json.JSONDecodeError, IOError):
            print("Ошибка загрузки статистики. Используются значения по умолчанию.")

    return stats


def save_stats(stats,):
    # Сохранение статистики в файл
    stats_file_path = get_stats_file_path()
    try:
        with open(stats_file_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"Ошибка сохранения статистики: {e}")
        return False