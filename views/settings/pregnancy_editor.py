from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QFrame
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from datetime import datetime
from utils.base_widgets import StyledDateEdit, StyledButton, TitleLabel
from utils.styles import Styles

class PregnancyEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_controller = DataController()
        self.setup_ui()
        self.load_pregnancy_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title = TitleLabel("Інформація про вагітність", 18)
        title.setStyleSheet(Styles.text_accent())
        main_layout.addWidget(title)

        form_frame = QFrame()
        form_frame.setStyleSheet(Styles.card_frame())
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 15, 15, 15)

        # Поля форми з лейблами
        period_label = QLabel("Дата останньої менструації:")
        period_label.setStyleSheet(Styles.text_primary())
        self.last_period_edit = StyledDateEdit()
        self.last_period_edit.setMinimumHeight(40)
        form_layout.addRow(period_label, self.last_period_edit)

        due_label = QLabel("Очікувана дата пологів:")
        due_label.setStyleSheet(Styles.text_primary())
        self.due_date_edit = StyledDateEdit()
        self.due_date_edit.setMinimumHeight(40)
        form_layout.addRow(due_label, self.due_date_edit)

        conception_label = QLabel("Дата зачаття (якщо відома):")
        conception_label.setStyleSheet(Styles.text_primary())
        self.conception_edit = StyledDateEdit()
        self.conception_edit.setMinimumHeight(40)
        form_layout.addRow(conception_label, self.conception_edit)

        main_layout.addWidget(form_frame)

        # Інформаційний блок
        info_frame = QFrame()
        info_frame.setStyleSheet(Styles.card_frame())
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        info_layout.setSpacing(10)

        info_title = QLabel("Поточна інформація")
        info_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        info_title.setStyleSheet(Styles.text_accent())
        info_layout.addWidget(info_title)

        self.week_label = QLabel("Поточний термін: ? тижнів")
        self.week_label.setFont(QFont('Arial', 14))
        self.week_label.setStyleSheet(Styles.text_primary())
        info_layout.addWidget(self.week_label)

        self.days_left_label = QLabel("До пологів залишилось: ? днів")
        self.days_left_label.setStyleSheet(Styles.text_primary())
        info_layout.addWidget(self.days_left_label)

        main_layout.addWidget(info_frame)

        save_btn = StyledButton("Зберегти зміни")
        save_btn.setMinimumHeight(50)
        save_btn.clicked.connect(self.save_pregnancy_data)
        main_layout.addWidget(save_btn)

        main_layout.addStretch(1)

    def load_pregnancy_data(self):
        pregnancy = self.data_controller.pregnancy_data

        if pregnancy.last_period_date:
            qdate = QDate(pregnancy.last_period_date.year, pregnancy.last_period_date.month,
                          pregnancy.last_period_date.day)
            self.last_period_edit.setDate(qdate)
        else:
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))

        if pregnancy.due_date:
            qdate = QDate(pregnancy.due_date.year, pregnancy.due_date.month, pregnancy.due_date.day)
            self.due_date_edit.setDate(qdate)
        else:
            self.due_date_edit.setDate(QDate.currentDate().addDays(280 - 40 * 7))

        if pregnancy.conception_date:
            qdate = QDate(pregnancy.conception_date.year, pregnancy.conception_date.month,
                          pregnancy.conception_date.day)
            self.conception_edit.setDate(qdate)
        else:
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))

        self.update_pregnancy_info()

    def update_pregnancy_info(self):
        current_week = self.data_controller.get_current_week()
        days_left = self.data_controller.get_days_left()

        if current_week:
            self.week_label.setText(f"Поточний термін: {current_week} тижнів")
        else:
            self.week_label.setText("Поточний термін: не визначено")

        if days_left:
            self.days_left_label.setText(f"До пологів залишилось: {days_left} днів")
        else:
            self.days_left_label.setText("До пологів: не визначено")

    def save_pregnancy_data(self):
        pregnancy = self.data_controller.pregnancy_data

        last_period = self.last_period_edit.date()
        pregnancy.last_period_date = datetime(last_period.year(), last_period.month(), last_period.day()).date()

        due_date = self.due_date_edit.date()
        pregnancy.due_date = datetime(due_date.year(), due_date.month(), due_date.day()).date()

        conception = self.conception_edit.date()
        pregnancy.conception_date = datetime(conception.year(), conception.month(), conception.day()).date()

        self.data_controller.save_pregnancy_data()
        self.update_pregnancy_info()

    def showEvent(self, event):
        super().showEvent(event)
        self.data_controller = DataController()
        self.load_pregnancy_data()