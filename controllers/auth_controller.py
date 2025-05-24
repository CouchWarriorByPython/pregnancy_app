import hashlib
import json
import os
from models.database import Database
from models.base import UserProfile
from utils.email_service import EmailService
from utils.logger import get_logger

logger = get_logger('auth_controller')


class AuthController:
    def __init__(self):
        self.db = Database()
        self.email_service = EmailService()
        self.session_file = 'session.json'

    def hash_password(self, password):
        """Хешування паролю"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password, password_hash):
        """Перевірка паролю"""
        return self.hash_password(password) == password_hash

    def register(self, email, name, password):
        """Реєстрація нового користувача"""
        existing_user = self.db.session.query(UserProfile).filter_by(email=email).first()
        if existing_user:
            return False

        verification_code = self.email_service.send_verification_code(email)
        password_hash = self.hash_password(password)

        user = UserProfile(
            email=email,
            name=name,
            password_hash=password_hash,
            verification_code=verification_code,
            is_verified=False
        )

        self.db.session.add(user)
        self.db.session.commit()
        logger.info(f"Створено користувача {email} з кодом {verification_code}")
        return True

    def login(self, email, password):
        """Вхід користувача"""
        user = self.db.session.query(UserProfile).filter_by(email=email).first()
        if user and user.is_verified and self.verify_password(password, user.password_hash):
            self.save_session(user.id, user.email)
            return user
        return None

    def verify_email(self, email, code):
        """Підтвердження email"""
        user = self.db.session.query(UserProfile).filter_by(email=email).first()
        if user and user.verification_code == code:
            user.is_verified = True
            user.verification_code = None
            self.db.session.commit()

            self.email_service.send_welcome_email(email, user.name)
            return user
        return None

    def resend_verification_code(self, email):
        """Повторне надсилання коду підтвердження"""
        user = self.db.session.query(UserProfile).filter_by(email=email).first()
        if user and not user.is_verified:
            verification_code = self.email_service.send_verification_code(email)
            user.verification_code = verification_code
            self.db.session.commit()
            return True
        return False

    def change_password(self, user_id, current_password, new_password):
        """Зміна паролю користувача"""
        user = self.db.session.query(UserProfile).filter_by(id=user_id).first()
        if user and self.verify_password(current_password, user.password_hash):
            user.password_hash = self.hash_password(new_password)
            self.db.session.commit()
            logger.info(f"Пароль змінено для користувача {user.email}")
            return True
        return False

    def save_session(self, user_id, email):
        """Збереження сесії"""
        session_data = {
            'user_id': user_id,
            'email': email,
            'logged_in': True
        }
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f)
            logger.info(f"Сесія збережена для користувача {email}")
        except Exception as e:
            logger.error(f"Помилка збереження сесії: {str(e)}")

    def load_session(self):
        """Завантаження сесії"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                if session_data.get('logged_in'):
                    user = self.db.session.query(UserProfile).filter_by(id=session_data['user_id']).first()
                    if user:
                        logger.info(f"Сесія відновлена для користувача {user.email}")
                        return {
                            'user_id': user.id,
                            'email': user.email
                        }
        except Exception as e:
            logger.error(f"Помилка завантаження сесії: {str(e)}")
        return None

    def logout(self):
        """Вихід користувача"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logger.info("Користувач вийшов з системи, сесія видалена")
        except Exception as e:
            logger.error(f"Помилка при виході: {str(e)}")
        return True