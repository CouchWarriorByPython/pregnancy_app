"""Утиліти для роботи з даними"""
import os
import json
from utils.logger import get_logger

logger = get_logger('data_utils')


def ensure_directory_exists(directory):
    """Переконується, що директорія існує, створює її, якщо ні"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Створено директорію: {directory}")


def save_json_data(data, filepath):
    """Зберігає дані у JSON-файл"""
    try:
        # Переконуємося, що директорія існує
        directory = os.path.dirname(filepath)
        ensure_directory_exists(directory)

        # Зберігаємо дані
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Дані успішно збережено у файл: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Помилка збереження даних у файл {filepath}: {e}")
        return False


def load_json_data(filepath, default=None):
    """Завантажує дані з JSON-файлу"""
    if default is None:
        default = {}

    try:
        if not os.path.exists(filepath):
            logger.warning(f"Файл не знайдено: {filepath}, повертаємо значення за замовчуванням")
            return default

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Дані успішно завантажено з файлу: {filepath}")
        return data
    except Exception as e:
        logger.error(f"Помилка завантаження даних з файлу {filepath}: {e}")
        return default