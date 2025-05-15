import logging
import os

# Перевірка наявності директорії для логів
if not os.path.exists('logs'):
    os.makedirs('logs')

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/app.log')
    ]
)

def get_logger(name):
    """Отримати логер з вказаним ім'ям"""
    return logging.getLogger(name) 