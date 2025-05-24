from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtCore import Qt
from utils.logger import get_logger
from utils.base_widgets import StyledButton, TitleLabel, QDateEdit
from styles.onboarding import OnboardingStyles
from styles.base import Colors
from datetime import datetime

logger = get_logger('pregnancy_info_screen')


class PregnancyInfoScreen(QWidget):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(OnboardingStyles.main_container())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        title = TitleLabel("Інформація про вагітність", 28)
        title.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 28px;
                font-weight: 700;
                text-align: center;
            }}
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("Вкажіть дати для розрахунку терміну вагітності")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 16px;
                font-weight: 500;
                text-align: center;
                line-height: 1.4;
            }}
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        main_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Стиль для DateEdit віджетів
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
        last_period_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        main_layout.addWidget(last_period_label)

        self.last_period_edit = QDateEdit()
        self.last_period_edit.setDate(QDate.currentDate().addDays(-280))
        self.last_period_edit.setMinimumHeight(50)
        self.last_period_edit.setDisplayFormat("dd.MM.yyyy")
        self.last_period_edit.setCalendarPopup(True)
        self.last_period_edit.setStyleSheet(date_edit_style)
        self.last_period_edit.dateChanged.connect(self.update_due_date)
        main_layout.addWidget(self.last_period_edit)

        last_period_hint = QLabel("Перший день останнього менструального циклу")
        last_period_hint.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
                font-weight: 400;
            }}
        """)
        main_layout.addWidget(last_period_hint)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Очікувана дата пологів
        due_date_label = QLabel("Очікувана дата пологів (розраховується автоматично):")
        due_date_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        main_layout.addWidget(due_date_label)

        self.due_date_label_value = QLabel()
        self.due_date_label_value.setMinimumHeight(50)
        self.due_date_label_value.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 16px 20px;
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
            }
        """)
        main_layout.addWidget(self.due_date_label_value)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Дата зачаття
        conception_label = QLabel("Дата зачаття (якщо відома):")
        conception_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        main_layout.addWidget(conception_label)

        self.conception_edit = QDateEdit()
        self.conception_edit.setDate(QDate.currentDate().addDays(-266))
        self.conception_edit.setMinimumHeight(50)
        self.conception_edit.setDisplayFormat("dd.MM.yyyy")
        self.conception_edit.setCalendarPopup(True)
        self.conception_edit.setStyleSheet(date_edit_style)
        main_layout.addWidget(self.conception_edit)

        conception_hint = QLabel("Зазвичай відбувається через 14 днів після початку менструації")
        conception_hint.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
                font-weight: 400;
            }}
        """)
        main_layout.addWidget(conception_hint)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        next_btn = StyledButton("Продовжити")
        next_btn.setMinimumHeight(60)
        next_btn.setStyleSheet(OnboardingStyles.onboarding_button())
        next_btn.clicked.connect(self.on_next_clicked)
        main_layout.addWidget(next_btn)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Встановлюємо початкову дату пологів
        self.update_due_date()

    def update_due_date(self):
        last_period_date = self.last_period_edit.date()
        due_date = last_period_date.addDays(280)
        self.due_date_label_value.setText(due_date.toString("dd.MM.yyyy"))

        # Оновлюємо дату зачаття на 14 днів після місячних
        conception_date = last_period_date.addDays(14)
        self.conception_edit.setDate(conception_date)

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id'):
            if callable(self.parent.current_user_id):
                return self.parent.current_user_id()
            else:
                return self.parent.current_user_id
        return None

    def on_next_clicked(self):
        user_id = self._get_current_user_id()
        if not user_id:
            QMessageBox.critical(self, "Помилка", "Користувач не авторизований")
            return

        last_period_date = self.last_period_edit.date()
        conception_date = self.conception_edit.date()

        last_period_date_obj = datetime(last_period_date.year(), last_period_date.month(),
                                        last_period_date.day()).date()
        conception_date_obj = datetime(conception_date.year(), conception_date.month(), conception_date.day()).date()

        if last_period_date_obj > conception_date_obj:
            QMessageBox.warning(self, "Помилка",
                                "Дата останньої менструації не може бути пізніше дати зачаття.\n"
                                "Зачаття зазвичай відбувається приблизно через 14 днів після початку останньої менструації.")
            return

        # Перевіряємо що дата зачаття не занадто пізня (більше 4 тижнів після місячних)
        days_diff = (conception_date_obj - last_period_date_obj).days
        if days_diff > 28:
            QMessageBox.warning(self, "Увага",
                                "Дата зачаття виглядає занадто пізньою.\n"
                                "Зазвичай зачаття відбувається протягом 2-3 тижнів після початку останньої менструації.")

        pregnancy_data = {
            "last_period_date": last_period_date.toString("yyyy-MM-dd"),
            "conception_date": conception_date.toString("yyyy-MM-dd")
        }

        logger.info(f"Дані про вагітність зібрані: {pregnancy_data}")
        self.proceed_signal.emit(pregnancy_data)