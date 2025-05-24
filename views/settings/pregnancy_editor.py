from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QFrame, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from datetime import datetime
from utils.base_widgets import StyledDateEdit, StyledButton, TitleLabel
from styles.base import BaseStyles
from utils.logger import get_logger

logger = get_logger('pregnancy_editor')


class PregnancyEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.last_period_edit = StyledDateEdit()
        self.conception_edit = StyledDateEdit()
        self.week_label = QLabel("Поточний термін: ? тижнів")
        self.days_left_label = QLabel("До пологів залишилось: ? днів")
        self.due_date_label = QLabel("Очікувана дата пологів: ?")

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
        form_frame.setStyleSheet(BaseStyles.card_frame())
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(20, 20, 20, 20)

        # Дата останньої менструації
        last_period_label = QLabel("Дата останньої менструації:")
        last_period_label.setStyleSheet(BaseStyles.text_primary())
        last_period_label.setFont(QFont('Arial', 14))
        form_layout.addWidget(last_period_label)

        self.last_period_edit.setMinimumHeight(50)
        form_layout.addWidget(self.last_period_edit)

        # Дата зачаття
        conception_label = QLabel("Дата зачаття:")
        conception_label.setStyleSheet(BaseStyles.text_primary())
        conception_label.setFont(QFont('Arial', 14))
        form_layout.addWidget(conception_label)

        self.conception_edit.setMinimumHeight(50)
        form_layout.addWidget(self.conception_edit)

        return form_frame

    def _create_info_frame(self):
        info_frame = QFrame()
        info_frame.setStyleSheet(BaseStyles.card_frame())
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(15)

        info_title = QLabel("Поточна інформація")
        info_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        info_title.setStyleSheet(BaseStyles.text_accent())
        info_layout.addWidget(info_title)

        self.week_label.setFont(QFont('Arial', 14))
        self.week_label.setStyleSheet(BaseStyles.text_primary())
        info_layout.addWidget(self.week_label)

        self.due_date_label.setFont(QFont('Arial', 14))
        self.due_date_label.setStyleSheet(BaseStyles.text_primary())
        info_layout.addWidget(self.due_date_label)

        self.days_left_label.setFont(QFont('Arial', 14))
        self.days_left_label.setStyleSheet(BaseStyles.text_primary())
        info_layout.addWidget(self.days_left_label)

        return info_frame

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id'):
            if callable(self.parent.current_user_id):
                return self.parent.current_user_id()
            else:
                return self.parent.current_user_id
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'current_user_id'):
            return self.parent.parent.current_user_id
        return None

    def load_pregnancy_data(self):
        user_id = self._get_current_user_id()
        if not user_id:
            logger.warning("Користувач не авторизований")
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))
            self.update_pregnancy_info()
            return

        self.data_controller = DataController(user_id)
        pregnancy = self.data_controller.pregnancy_data

        if not pregnancy:
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))
            self.update_pregnancy_info()
            return

        if pregnancy.last_period_date:
            qdate = QDate(pregnancy.last_period_date.year, pregnancy.last_period_date.month,
                          pregnancy.last_period_date.day)
            self.last_period_edit.setDate(qdate)
        else:
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))

        if pregnancy.conception_date:
            qdate = QDate(pregnancy.conception_date.year, pregnancy.conception_date.month,
                          pregnancy.conception_date.day)
            self.conception_edit.setDate(qdate)
        else:
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))

        self.update_pregnancy_info()

    def update_pregnancy_info(self):
        if not self.data_controller or not self.data_controller.pregnancy_data:
            self.week_label.setText("Поточний термін: не визначено")
            self.due_date_label.setText("Очікувана дата пологів: не визначено")
            self.days_left_label.setText("До пологів залишилось: не визначено")
            return

        current_week = self.data_controller.get_current_week()
        days_left = self.data_controller.get_days_left()
        due_date = self.data_controller.pregnancy_data.due_date

        self.week_label.setText(f"Поточний термін: {current_week or 'не визначено'} тижнів")
        self.days_left_label.setText(f"До пологів залишилось: {days_left or 'не визначено'} днів")

        if due_date:
            self.due_date_label.setText(f"Очікувана дата пологів: {due_date.strftime('%d.%m.%Y')}")
        else:
            self.due_date_label.setText("Очікувана дата пологів: не визначено")

    def save_pregnancy_data(self):
        if not self.data_controller or not self.data_controller.pregnancy_data:
            QMessageBox.warning(self, "Помилка", "Неможливо зберегти дані - користувач не авторизований")
            return

        pregnancy = self.data_controller.pregnancy_data

        last_period_date = self.last_period_edit.date()
        conception_date = self.conception_edit.date()

        last_period_date_obj = datetime(last_period_date.year(), last_period_date.month(),
                                        last_period_date.day()).date()
        conception_date_obj = datetime(conception_date.year(), conception_date.month(), conception_date.day()).date()

        if last_period_date_obj > conception_date_obj:
            QMessageBox.warning(self, "Помилка",
                                "Дата останньої менструації не може бути пізніше дати зачаття")
            return

        pregnancy.last_period_date = last_period_date_obj
        pregnancy.conception_date = conception_date_obj

        try:
            self.data_controller.save_pregnancy_data()
            self.update_pregnancy_info()
            QMessageBox.information(self, "Успіх", "Дані успішно збережено")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка збереження: {str(e)}")
            logger.error(f"Помилка збереження даних про вагітність: {str(e)}")

    def showEvent(self, event):
        super().showEvent(event)
        self.load_pregnancy_data()