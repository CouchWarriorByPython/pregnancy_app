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
        self._init_controls()
        self._setup_ui()
        self.load_pregnancy_data()

    def _init_controls(self):
        self.last_period_edit = StyledDateEdit()
        self.due_date_edit = StyledDateEdit()
        self.conception_edit = StyledDateEdit()
        self.week_label = QLabel("Поточний термін: ? тижнів")
        self.days_left_label = QLabel("До пологів залишилось: ? днів")

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title = TitleLabel("Інформація про вагітність", 18)
        main_layout.addWidget(title)

        main_layout.addWidget(self._create_form_frame())
        main_layout.addWidget(self._create_info_frame())

        save_btn = StyledButton("Зберегти зміни")
        save_btn.setMinimumHeight(50)
        save_btn.clicked.connect(self.save_pregnancy_data)
        main_layout.addWidget(save_btn)
        main_layout.addStretch(1)

    def _create_form_frame(self):
        form_frame = QFrame()
        form_frame.setStyleSheet(Styles.card_frame())
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 15, 15, 15)

        fields = [
            ("Дата останньої менструації:", self.last_period_edit),
            ("Очікувана дата пологів:", self.due_date_edit),
            ("Дата зачаття (якщо відома):", self.conception_edit)
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet(Styles.text_primary())
            widget.setMinimumHeight(40)
            form_layout.addRow(label, widget)

        return form_frame

    def _create_info_frame(self):
        info_frame = QFrame()
        info_frame.setStyleSheet(Styles.card_frame())
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        info_layout.setSpacing(10)

        info_title = QLabel("Поточна інформація")
        info_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        info_title.setStyleSheet(Styles.text_accent())
        info_layout.addWidget(info_title)

        self.week_label.setFont(QFont('Arial', 14))
        self.week_label.setStyleSheet(Styles.text_primary())
        info_layout.addWidget(self.week_label)

        self.days_left_label.setStyleSheet(Styles.text_primary())
        info_layout.addWidget(self.days_left_label)

        return info_frame

    def load_pregnancy_data(self):
        pregnancy = self.data_controller.pregnancy_data

        dates = [
            (pregnancy.last_period_date, self.last_period_edit, -280),
            (pregnancy.due_date, self.due_date_edit, 280 - 40 * 7),
            (pregnancy.conception_date, self.conception_edit, -266)
        ]

        for date_val, widget, default_offset in dates:
            if date_val:
                qdate = QDate(date_val.year, date_val.month, date_val.day)
                widget.setDate(qdate)
            else:
                widget.setDate(QDate.currentDate().addDays(default_offset))

        self.update_pregnancy_info()

    def update_pregnancy_info(self):
        current_week = self.data_controller.get_current_week()
        days_left = self.data_controller.get_days_left()

        self.week_label.setText(f"Поточний термін: {current_week or 'не визначено'} тижнів")
        self.days_left_label.setText(f"До пологів залишилось: {days_left or 'не визначено'} днів")

    def save_pregnancy_data(self):
        pregnancy = self.data_controller.pregnancy_data

        dates = [
            (self.last_period_edit, 'last_period_date'),
            (self.due_date_edit, 'due_date'),
            (self.conception_edit, 'conception_date')
        ]

        for widget, attr in dates:
            date_val = widget.date()
            setattr(pregnancy, attr, datetime(date_val.year(), date_val.month(), date_val.day()).date())

        self.data_controller.save_pregnancy_data()
        self.update_pregnancy_info()

    def showEvent(self, event):
        super().showEvent(event)
        self.data_controller = DataController()
        self.load_pregnancy_data()