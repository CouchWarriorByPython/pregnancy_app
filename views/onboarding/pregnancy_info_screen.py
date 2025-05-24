from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtGui import QFont
from utils.logger import get_logger
from utils.base_widgets import StyledDateEdit, StyledButton, TitleLabel
from styles.onboarding import OnboardingStyles
from styles.base import BaseStyles
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

        title = TitleLabel("Інформація про вагітність")
        title.setStyleSheet(OnboardingStyles.step_title())
        main_layout.addWidget(title)

        # Секція з формою
        form_section = QWidget()
        form_section.setStyleSheet(OnboardingStyles.form_section())
        form_layout = QVBoxLayout(form_section)
        form_layout.setSpacing(25)

        # Дата останньої менструації
        last_period_label = QLabel("Дата останньої менструації:")
        last_period_label.setStyleSheet(OnboardingStyles.field_label())
        last_period_label.setFont(QFont('Arial', 14))
        form_layout.addWidget(last_period_label)

        self.last_period_edit = StyledDateEdit()
        self.last_period_edit.setDate(QDate.currentDate().addDays(-30))
        self.last_period_edit.setMinimumHeight(60)
        self.last_period_edit.setStyleSheet(OnboardingStyles.onboarding_input())
        form_layout.addWidget(self.last_period_edit)

        # Дата зачаття
        conception_label = QLabel("Дата зачаття:")
        conception_label.setStyleSheet(OnboardingStyles.field_label())
        conception_label.setFont(QFont('Arial', 14))
        form_layout.addWidget(conception_label)

        self.conception_edit = StyledDateEdit()
        self.conception_edit.setDate(QDate.currentDate().addDays(-14))
        self.conception_edit.setMinimumHeight(60)
        self.conception_edit.setStyleSheet(OnboardingStyles.onboarding_input())
        form_layout.addWidget(self.conception_edit)

        # Пояснювальний текст
        info_label = QLabel("Дата пологів буде розрахована автоматично на основі дати зачаття")
        info_label.setStyleSheet(OnboardingStyles.field_label())
        info_label.setWordWrap(True)
        info_label.setFont(QFont('Arial', 13))
        form_layout.addWidget(info_label)

        main_layout.addWidget(form_section)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        next_btn = StyledButton("Продовжити")
        next_btn.setMinimumHeight(60)
        next_btn.setStyleSheet(OnboardingStyles.onboarding_button())
        next_btn.clicked.connect(self.on_next_clicked)
        main_layout.addWidget(next_btn)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

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
                                "Будь ласка, перевірте введені дати.")
            return

        pregnancy_data = {
            "last_period_date": last_period_date.toString("yyyy-MM-dd"),
            "conception_date": conception_date.toString("yyyy-MM-dd")
        }

        logger.info(f"Дані про вагітність зібрані: {pregnancy_data}")
        self.proceed_signal.emit(pregnancy_data)