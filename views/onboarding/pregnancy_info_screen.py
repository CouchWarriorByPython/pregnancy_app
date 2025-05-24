from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtCore import Qt
from utils.logger import get_logger
from utils.base_widgets import StyledDateEdit, StyledButton, TitleLabel
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
        title.setStyleSheet(OnboardingStyles.step_title())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("Вкажіть дати для розрахунку терміну вагітності")
        subtitle.setStyleSheet(OnboardingStyles.step_subtitle())
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        # Секція з формою
        form_section = QWidget()
        form_section.setStyleSheet(OnboardingStyles.form_section())
        form_layout = QVBoxLayout(form_section)
        form_layout.setSpacing(20)

        # Дата останньої менструації
        last_period_container = QWidget()
        last_period_layout = QVBoxLayout(last_period_container)
        last_period_layout.setContentsMargins(0, 0, 0, 0)
        last_period_layout.setSpacing(8)

        last_period_label = QLabel("Дата останньої менструації:")
        last_period_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """)
        last_period_layout.addWidget(last_period_label)

        self.last_period_edit = StyledDateEdit()
        self.last_period_edit.setDate(QDate.currentDate().addDays(-280))
        self.last_period_edit.setMinimumHeight(60)
        self.last_period_edit.setStyleSheet(OnboardingStyles.onboarding_input())
        self.last_period_edit.dateChanged.connect(self.update_conception_date)
        last_period_layout.addWidget(self.last_period_edit)

        last_period_hint = QLabel("Перший день останнього менструального циклу")
        last_period_hint.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
                font-weight: 400;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """)
        last_period_layout.addWidget(last_period_hint)

        form_layout.addWidget(last_period_container)

        # Дата зачаття
        conception_container = QWidget()
        conception_layout = QVBoxLayout(conception_container)
        conception_layout.setContentsMargins(0, 0, 0, 0)
        conception_layout.setSpacing(8)

        conception_label = QLabel("Дата зачаття (приблизно):")
        conception_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """)
        conception_layout.addWidget(conception_label)

        self.conception_edit = StyledDateEdit()
        self.conception_edit.setDate(QDate.currentDate().addDays(-266))
        self.conception_edit.setMinimumHeight(60)
        self.conception_edit.setStyleSheet(OnboardingStyles.onboarding_input())
        conception_layout.addWidget(self.conception_edit)

        conception_hint = QLabel("Зазвичай відбувається через 14 днів після початку менструації")
        conception_hint.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
                font-weight: 400;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """)
        conception_layout.addWidget(conception_hint)

        form_layout.addWidget(conception_container)

        # Інформаційний блок
        info_frame = QWidget()
        info_frame.setStyleSheet(f"""
            QWidget {{
                background: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 16px;
                padding: 16px;
            }}
        """)
        info_layout = QVBoxLayout(info_frame)

        info_icon_label = QLabel("ℹ️ Як розраховується термін?")
        info_icon_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 15px;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """)
        info_layout.addWidget(info_icon_label)

        info_text = QLabel(
            "Дата пологів розраховується як дата останньої менструації + 280 днів (40 тижнів). Це стандартний акушерський метод підрахунку.")
        info_text.setWordWrap(True)
        info_text.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 400;
                line-height: 1.5;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """)
        info_layout.addWidget(info_text)

        form_layout.addWidget(info_frame)

        main_layout.addWidget(form_section)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        next_btn = StyledButton("Продовжити")
        next_btn.setMinimumHeight(60)
        next_btn.setStyleSheet(OnboardingStyles.onboarding_button())
        next_btn.clicked.connect(self.on_next_clicked)
        main_layout.addWidget(next_btn)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

    def update_conception_date(self, date):
        # Автоматично оновлюємо дату зачаття на 14 днів після останніх місячних
        new_conception_date = date.addDays(14)
        self.conception_edit.setDate(new_conception_date)

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