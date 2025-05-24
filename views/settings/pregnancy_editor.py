from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDateEdit, QFrame, QMessageBox
from utils.base_widgets import TitleLabel

class PregnancyEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        title = TitleLabel("Інформація про вагітність", 18)
        main_layout.addWidget(title)

        # Основний фрейм з формою
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 0px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(20, 15, 20, 15)
        form_layout.setSpacing(12)

        # Стиль для лейблів - більш яскравий білий
        label_style = """
            color: #FFFFFF;
            font-size: 15px;
            font-weight: 600;
            background: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """

        # Стиль для QDateEdit
        date_edit_style = """
            QDateEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 16px 20px;
                color: white;
                font-size: 14px;
                min-height: 20px;
            }
            QDateEdit:focus {
                border: 2px solid #8B5CF6;
                background: rgba(255, 255, 255, 0.12);
            }
            QDateEdit::drop-down {
                border: none;
                width: 30px;
                background: transparent;
            }
            QDateEdit::down-arrow {
                image: none;
                border: 5px solid transparent;
                border-top: 8px solid white;
                margin-right: 10px;
            }
            QCalendarWidget {
                background-color: #1E1B4B;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 4px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QCalendarWidget QMenu {
                background-color: #1E1B4B;
                color: white;
            }
            QCalendarWidget QSpinBox {
                background-color: transparent;
                color: white;
                border: none;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #1E1B4B;
                color: white;
                selection-background-color: #8B5CF6;
                selection-color: white;
            }
        """

        # Дата останньої менструації
        last_period_label = QLabel("Дата останньої менструації:")
        last_period_label.setStyleSheet(label_style)
        form_layout.addWidget(last_period_label)

        self.last_period_edit = QDateEdit()
        self.last_period_edit.setMinimumHeight(50)
        self.last_period_edit.setDisplayFormat("dd.MM.yyyy")
        self.last_period_edit.setCalendarPopup(True)
        self.last_period_edit.setStyleSheet(date_edit_style)
        form_layout.addWidget(self.last_period_edit)

        # Очікувана дата пологів
        due_date_label = QLabel("Очікувана дата пологів:")
        due_date_label.setStyleSheet(label_style)
        form_layout.addWidget(due_date_label)

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setMinimumHeight(50)
        self.due_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setStyleSheet(date_edit_style)
        form_layout.addWidget(self.due_date_edit)

        # Дата зачаття
        conception_label = QLabel("Дата зачаття (якщо відома):")
        conception_label.setStyleSheet(label_style)
        form_layout.addWidget(conception_label)

        self.conception_edit = QDateEdit()
        self.conception_edit.setMinimumHeight(50)
        self.conception_edit.setDisplayFormat("dd.MM.yyyy")
        self.conception_edit.setCalendarPopup(True)
        self.conception_edit.setStyleSheet(date_edit_style)
        form_layout.addWidget(self.conception_edit)

        main_layout.addWidget(form_frame)

        # Інформаційний фрейм - той самий стиль що й основний
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 0px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 15, 20, 15)
        info_layout.setSpacing(8)

        self.week_label = QLabel("Поточний термін: не визначено")
        self.week_label.setFont(QFont('Arial', 16, QFont.Weight.Normal))
        self.week_label.setStyleSheet("color: #FFFFFF; background: transparent; border: none; font-weight: 500;")
        info_layout.addWidget(self.week_label)

        self.days_left_label = QLabel("До пологів: не визначено")
        self.days_left_label.setFont(QFont('Arial', 16, QFont.Weight.Normal))
        self.days_left_label.setStyleSheet("color: #FFFFFF; background: transparent; border: none; font-weight: 500;")
        info_layout.addWidget(self.days_left_label)

        main_layout.addWidget(info_frame)

        # Кнопка збереження
        save_btn = QPushButton("Зберегти зміни")
        save_btn.setMinimumHeight(55)
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #EC4899);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 15px 25px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #DB2777);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6D28D9, stop:1 #BE185D);
            }
        """)
        save_btn.clicked.connect(self.save_pregnancy_data)
        main_layout.addWidget(save_btn)

        # Зв'язуємо обробники для автоматичного оновлення дат
        self.last_period_edit.dateChanged.connect(self.on_last_period_changed)
        self.conception_edit.dateChanged.connect(self.on_conception_changed)

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id'):
            if callable(self.parent.current_user_id):
                return self.parent.current_user_id()
            else:
                return self.parent.current_user_id
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'current_user_id'):
            return self.parent.parent.current_user_id
        return None

    def on_last_period_changed(self, date):
        # Автоматично розраховуємо очікувану дату пологів (додаємо 280 днів)
        due_date = date.addDays(280)
        self.due_date_edit.setDate(due_date)
        # Оновлюємо дату зачаття (додаємо 14 днів)
        conception_date = date.addDays(14)
        self.conception_edit.setDate(conception_date)
        self.update_pregnancy_info()

    def on_conception_changed(self, date):
        self.update_pregnancy_info()

    def load_pregnancy_data(self):
        user_id = self._get_current_user_id()
        if not user_id:
            # Встановлюємо дефолтні значення
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))
            self.due_date_edit.setDate(QDate.currentDate().addDays(0))
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))
            self.week_label.setText("Поточний термін: не визначено")
            self.days_left_label.setText("До пологів: не визначено")
            return

        self.data_controller = DataController(user_id)
        pregnancy = self.data_controller.pregnancy_data

        if pregnancy and pregnancy.last_period_date:
            qdate = QDate(pregnancy.last_period_date.year, pregnancy.last_period_date.month,
                          pregnancy.last_period_date.day)
            self.last_period_edit.setDate(qdate)
        else:
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))

        if pregnancy and pregnancy.due_date:
            qdate = QDate(pregnancy.due_date.year, pregnancy.due_date.month, pregnancy.due_date.day)
            self.due_date_edit.setDate(qdate)
        elif pregnancy and pregnancy.last_period_date:
            # Розраховуємо на основі останньої менструації
            self.due_date_edit.setDate(self.last_period_edit.date().addDays(280))
        else:
            self.due_date_edit.setDate(QDate.currentDate().addDays(0))

        if pregnancy and pregnancy.conception_date:
            qdate = QDate(pregnancy.conception_date.year, pregnancy.conception_date.month,
                          pregnancy.conception_date.day)
            self.conception_edit.setDate(qdate)
        else:
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))

        self.update_pregnancy_info()

    def update_pregnancy_info(self):
        if not self.data_controller:
            user_id = self._get_current_user_id()
            if user_id:
                self.data_controller = DataController(user_id)
            else:
                self.week_label.setText("Поточний термін: не визначено")
                self.days_left_label.setText("До пологів: не визначено")
                return

        current_week = self.data_controller.get_current_week()
        days_left = self.data_controller.get_days_left()

        if current_week:
            self.week_label.setText(f"Поточний термін: {current_week} тижнів")
        else:
            self.week_label.setText("Поточний термін: не визначено")

        if days_left is not None and days_left >= 0:
            self.days_left_label.setText(f"До пологів залишилось: {days_left} днів")
        else:
            self.days_left_label.setText("До пологів: не визначено")

    def save_pregnancy_data(self):
        if not self.data_controller or not self.data_controller.pregnancy_data:
            QMessageBox.warning(self, "Помилка", "Неможливо зберегти дані - користувач не авторизований")
            return

        pregnancy = self.data_controller.pregnancy_data

        last_period = self.last_period_edit.date()
        pregnancy.last_period_date = datetime(last_period.year(), last_period.month(), last_period.day()).date()

        due_date = self.due_date_edit.date()
        pregnancy.due_date = datetime(due_date.year(), due_date.month(), due_date.day()).date()

        conception = self.conception_edit.date()
        pregnancy.conception_date = datetime(conception.year(), conception.month(), conception.day()).date()

        try:
            self.data_controller.save_pregnancy_data()
            self.update_pregnancy_info()
            QMessageBox.information(self, "Успіх", "Дані про вагітність успішно збережено")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка збереження: {str(e)}")

    def showEvent(self, event):
        super().showEvent(event)
        self.load_pregnancy_data()