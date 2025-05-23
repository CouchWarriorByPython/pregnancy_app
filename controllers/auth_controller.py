from models.database import Database
from models.base import UserProfile
from utils.email_service import EmailService
from utils.logger import get_logger

logger = get_logger('auth_controller')


class AuthController:
    def __init__(self):
        self.db = Database()
        self.email_service = EmailService()

    def register(self, email, name):
        existing_user = self.db.session.query(UserProfile).filter_by(email=email).first()
        if existing_user:
            return False

        verification_code = self.email_service.send_verification_code(email)

        user = UserProfile(
            email=email,
            name=name,
            verification_code=verification_code,
            is_verified=False
        )

        self.db.session.add(user)
        self.db.session.commit()
        logger.info(f"Створено користувача {email} з кодом {verification_code}")
        return True

    def login(self, email):
        user = self.db.session.query(UserProfile).filter_by(email=email).first()
        return user

    def verify_email(self, email, code):
        user = self.db.session.query(UserProfile).filter_by(email=email).first()
        if user and user.verification_code == code:
            user.is_verified = True
            user.verification_code = None
            self.db.session.commit()

            # Відправляємо вітальний email
            self.email_service.send_welcome_email(email, user.name)

            return user
        return None

    def resend_verification_code(self, email):
        user = self.db.session.query(UserProfile).filter_by(email=email).first()
        if user and not user.is_verified:
            verification_code = self.email_service.send_verification_code(email)
            user.verification_code = verification_code
            self.db.session.commit()
            return True
        return False

    def logout(self):
        logger.info("Користувач вийшов з системи")
        return True