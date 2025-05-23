from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFormLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal, QDate
from utils.logger import get_logger
from utils.base_widgets import StyledDateEdit, StyledButton, TitleLabel
from utils.styles import Styles
from datetime import datetime

logger = get_logger('pregnancy_info_screen')

class PregnancyInfoScreen(QWidget):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = TitleLabel("Інформація про вагітність", 22)
        main_layout.addWidget(title)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(0, 0, 0, 0)

        last_period_label = QLabel("Дата останньої менструації:")
        last_period_label.setStyleSheet(Styles.text_primary())

        self.last_period_edit = StyledDateEdit()
        self.last_period_edit.setDate(QDate.currentDate().addDays(-30))
        form_layout.addRow(last_period_label, self.last_period_edit)

        conception_label = QLabel("Дата зачаття:")
        conception_label.setStyleSheet(Styles.text_primary())

        self.conception_edit = StyledDateEdit()
        self.conception_edit.setDate(QDate.currentDate().addDays(-14))
        form_layout.addRow(conception_label, self.conception_edit)

        info_label = QLabel("Дата пологів буде розрахована автоматично на основі дати зачаття")
        info_label.setStyleSheet(Styles.text_secondary())
        info_label.setWordWrap(True)
        form_layout.addRow("", info_label)

        main_layout.addLayout(form_layout)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        next_btn = StyledButton("Продовжити")
        next_btn.setMinimumHeight(70)
        next_btn.clicked.connect(self.on_next_clicked)
        main_layout.addWidget(next_btn)

    def _get_current_user_id(self):
        """Отримуємо ID поточного користувача"""
        if hasattr(self.parent, 'current_user_id') and self.parent.current_user_id:
            return self.parent.current_user_id
        return None

    def on_next_clicked(self):
        user_id = self._get_current_user_id()
        if not user_id:
            QMessageBox.critical(self, "Помилка", "Користувач не авторизований")
            return

        last_period_date = self.last_period_edit.date()
        conception_date = self.conception_edit.date()

        last_period_date_obj = datetime(last_period_date.year(), last_period_date.month(), last_period_date.day()).date()
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