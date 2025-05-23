import json
import os
from utils.logger import get_logger

logger = get_logger('session_manager')


class SessionManager:
    def __init__(self, session_file='session.json'):
        self.session_file = session_file

    def save_session(self, user_id, email):
        """Збереження сесії користувача"""
        session_data = {
            'user_id': user_id,
            'email': email,
            'logged_in': True
        }
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f)
            logger.info(f"Сесія збережена для користувача {email}")
            return True
        except Exception as e:
            logger.error(f"Помилка збереження сесії: {str(e)}")
            return False

    def load_session(self):
        """Завантаження сесії користувача"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                if session_data.get('logged_in'):
                    logger.info(f"Сесія відновлена для користувача {session_data.get('email')}")
                    return {
                        'user_id': session_data['user_id'],
                        'email': session_data['email']
                    }
        except Exception as e:
            logger.error(f"Помилка завантаження сесії: {str(e)}")
        return None

    def clear_session(self):
        """Очищення сесії користувача"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logger.info("Сесія очищена")
            return True
        except Exception as e:
            logger.error(f"Помилка очищення сесії: {str(e)}")
            return False

    def is_logged_in(self):
        """Перевірка чи користувач увійшов в систему"""
        session = self.load_session()
        return session is not None