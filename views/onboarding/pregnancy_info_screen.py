from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFormLayout
from PyQt6.QtCore import pyqtSignal, QDate
from utils.logger import get_logger
from utils.base_widgets import StyledDateEdit, StyledButton, TitleLabel
from utils.styles import Styles

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

        conception_label = QLabel("Дата зачаття (якщо відома):")
        conception_label.setStyleSheet(Styles.text_primary())

        self.conception_edit = StyledDateEdit()
        self.conception_edit.setDate(QDate.currentDate().addDays(-14))
        form_layout.addRow(conception_label, self.conception_edit)

        main_layout.addLayout(form_layout)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        next_btn = StyledButton("Продовжити")
        next_btn.setMinimumHeight(70)
        next_btn.clicked.connect(self.on_next_clicked)
        main_layout.addWidget(next_btn)

    def on_next_clicked(self):
        pregnancy_data = {
            "last_period_date": self.last_period_edit.date().toString("yyyy-MM-dd"),
            "conception_date": self.conception_edit.date().toString("yyyy-MM-dd")
        }

        logger.info(f"Дані про вагітність зібрані: {pregnancy_data}")
        self.proceed_signal.emit(pregnancy_data)