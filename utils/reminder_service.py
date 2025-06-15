from PyQt6.QtCore import QTimer, QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMessageBox, QSystemTrayIcon, QMenu
from datetime import datetime, date
from utils.logger import get_logger
from utils.email_service import EmailService
import os


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
        self.tray_icon = None
        self._setup_system_tray()

    def _setup_system_tray(self):
        """Налаштовує системний трей з інтерактивним меню"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            # Встановлюємо іконку
            icon_path = "resources/images/icons/calendar.png"
            if os.path.exists(icon_path):
                self.tray_icon.setIcon(QIcon(icon_path))
            else:
                # Використовуємо стандартну іконку
                self.tray_icon.setIcon(self.parent().windowIcon() if self.parent() else QIcon())
            
            # Створюємо контекстне меню
            tray_menu = QMenu()
            
            show_action = QAction("Показати додаток", self)
            show_action.triggered.connect(self._show_main_window)
            tray_menu.addAction(show_action)
            
            tray_menu.addSeparator()
            
            quit_action = QAction("Вийти", self)
            quit_action.triggered.connect(self._quit_application)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.setToolTip("Додаток для вагітних - Нагадування")
            
            # Подвійний клік показує головне вікно
            self.tray_icon.activated.connect(self._tray_icon_activated)
            
            self.tray_icon.show()
            logger.info("Системний трей налаштовано")
        else:
            logger.warning("Системний трей недоступний")

    def _tray_icon_activated(self, reason):
        """Обробляє клік по іконці в треї"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._show_main_window()

    def _show_main_window(self):
        """Показує головне вікно додатку"""
        if self.parent():
            self.parent().show()
            self.parent().raise_()
            self.parent().activateWindow()

    def _quit_application(self):
        """Закриває додаток"""
        if self.parent():
            self.parent().close()

    def start(self):
        if not self.active:
            self.timer.start(60000)  # Перевіряємо кожну хвилину
            self.active = True
            logger.info("Сервіс нагадувань запущено")

    def stop(self):
        if self.active:
            self.timer.stop()
            self.active = False
            if self.tray_icon:
                self.tray_icon.hide()
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

            # Показуємо системне сповіщення через трей
            if self.tray_icon and self.tray_icon.isVisible():
                self.tray_icon.showMessage(
                    title,
                    description,
                    QSystemTrayIcon.MessageIcon.Information,
                    10000  # 10 секунд
                )

            # Показуємо інтерактивне діалогове вікно
            self._show_reminder_dialog(title, description)

            # Відправляємо email якщо є адреса
            if self.user_email:
                try:
                    user_profile = self.db.get_user_profile(self.user_id)
                    user_name = user_profile.name if user_profile else "Користувач"
                    self.email_service.send_reminder_email(
                        self.user_email,
                        user_name,
                        title,
                        description
                    )
                except Exception as e:
                    logger.error(f"Помилка відправки email: {str(e)}")

            logger.info(f"Показано нагадування: {title}")
            self.reminder_triggered.emit(reminder)

        except Exception as e:
            logger.error(f"Помилка при показі нагадування: {str(e)}")

    def _show_reminder_dialog(self, title, description):
        """Показує стилізоване діалогове вікно нагадування"""
        from utils.message_utils import show_info
        
        # Використовуємо наш стилізований message box
        if self.parent():
            show_info(self.parent(), title, description)
        else:
            # Fallback для випадку коли немає parent
            msg = QMessageBox()
            msg.setWindowTitle(title)
            msg.setText(description)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStyleSheet("""
                QMessageBox {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1E1B4B, stop:1 #312E81);
                    color: white;
                    border-radius: 12px;
                }
                QMessageBox QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #EC4899);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: 600;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #DB2777);
                }
            """)
            msg.exec()

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