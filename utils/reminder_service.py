from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QSystemTrayIcon
from datetime import datetime, date, time
from utils.logger import get_logger
from utils.email_service import EmailService

logger = get_logger('reminder_service')


class ReminderService(QObject):
    reminder_triggered = pyqtSignal(dict)

    def __init__(self, database, user_id, user_email=None, parent=None):
        super().__init__(parent)
        self.db = database
        self.user_id = user_id
        self.user_email = user_email
        self.email_service = EmailService()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reminders)
        self.active = False

    def start(self):
        if not self.active:
            self.timer.start(60000)  # Перевіряємо кожну хвилину
            self.active = True
            logger.info("Сервіс нагадувань запущено")

    def stop(self):
        if self.active:
            self.timer.stop()
            self.active = False
            logger.info("Сервіс нагадувань зупинено")

    def check_reminders(self):
        try:
            current_date = date.today()
            current_time = datetime.now().time()

            reminders = self.db.get_active_reminders(self.user_id)

            for reminder in reminders:
                reminder_date = datetime.strptime(reminder['reminder_date'], '%Y-%m-%d').date()
                reminder_time = datetime.strptime(reminder['reminder_time'], '%H:%M').time()

                if (reminder_date == current_date and
                        abs((datetime.combine(current_date, current_time) -
                             datetime.combine(current_date, reminder_time)).total_seconds()) < 60):
                    self.show_reminder(reminder)
                    self.db.complete_reminder(reminder['id'], self.user_id)

        except Exception as e:
            logger.error(f"Помилка при перевірці нагадувань: {str(e)}")

    def show_reminder(self, reminder):
        try:
            title = reminder['title']
            description = reminder.get('description', '')

            # Показуємо системне сповіщення
            if QSystemTrayIcon.isSystemTrayAvailable():
                tray_icon = QSystemTrayIcon()
                tray_icon.showMessage(
                    f"Нагадування: {title}",
                    description,
                    QSystemTrayIcon.MessageIcon.Information,
                    5000
                )
            else:
                QMessageBox.information(
                    None,
                    f"Нагадування: {title}",
                    description
                )

            # Відправляємо email нагадування якщо є email
            if self.user_email:
                user_profile = self.db.get_user_profile(self.user_id)
                user_name = user_profile.name if user_profile else "Користувач"
                self.email_service.send_reminder_email(
                    self.user_email,
                    user_name,
                    title,
                    description
                )

            logger.info(f"Показано нагадування: {title}")
            self.reminder_triggered.emit(reminder)

        except Exception as e:
            logger.error(f"Помилка при показі нагадування: {str(e)}")

    def add_reminder(self, title, description, reminder_date, reminder_time, reminder_type='custom'):
        try:
            self.db.add_reminder(
                title=title,
                description=description,
                reminder_date=reminder_date,
                reminder_time=reminder_time,
                reminder_type=reminder_type,
                user_id=self.user_id
            )
            logger.info(f"Додано нагадування: {title} на {reminder_date} {reminder_time}")
            return True
        except Exception as e:
            logger.error(f"Помилка при додаванні нагадування: {str(e)}")
            return False