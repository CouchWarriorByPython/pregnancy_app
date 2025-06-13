from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDateEdit, QFrame, QMessageBox
from utils.base_widgets import TitleLabel
from styles import PregnancyEditorStyles
from utils.user_mixin import UserMixin
from utils.logger import get_logger

logger = get_logger('pregnancy_editor')


class PregnancyEditor(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_container = QWidget()
        title_container.setStyleSheet(PregnancyEditorStyles.title_container())

        title_layout = QVBoxLayout(title_container)
        title = TitleLabel("🤰 Інформація про вагітність", 20)
        title.setStyleSheet(PregnancyEditorStyles.section_title())
        title_layout.addWidget(title)

        subtitle = QLabel("Терміни та важливі дати")
        subtitle.setStyleSheet(PregnancyEditorStyles.section_subtitle())
        title_layout.addWidget(subtitle)

        main_layout.addWidget(title_container)

        form_frame = QFrame()
        form_frame.setStyleSheet(PregnancyEditorStyles.form_frame())
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)

        last_period_label = QLabel("📅 Дата останньої менструації:")
        last_period_label.setStyleSheet(PregnancyEditorStyles.field_label())
        form_layout.addWidget(last_period_label)

        self.last_period_edit = QDateEdit()
        self.last_period_edit.setMinimumHeight(56)
        self.last_period_edit.setDisplayFormat("dd.MM.yyyy")
        self.last_period_edit.setCalendarPopup(True)
        self.last_period_edit.setStyleSheet(PregnancyEditorStyles.date_edit())
        form_layout.addWidget(self.last_period_edit)

        due_date_label = QLabel("🍼 Очікувана дата пологів (розраховується автоматично):")
        due_date_label.setStyleSheet(PregnancyEditorStyles.field_label())
        form_layout.addWidget(due_date_label)

        self.due_date_label_value = QLabel()
        self.due_date_label_value.setMinimumHeight(56)
        self.due_date_label_value.setStyleSheet(PregnancyEditorStyles.due_date_label())
        form_layout.addWidget(self.due_date_label_value)

        conception_label = QLabel("💫 Дата зачаття (якщо відома):")
        conception_label.setStyleSheet(PregnancyEditorStyles.field_label())
        form_layout.addWidget(conception_label)

        self.conception_edit = QDateEdit()
        self.conception_edit.setMinimumHeight(56)
        self.conception_edit.setDisplayFormat("dd.MM.yyyy")
        self.conception_edit.setCalendarPopup(True)
        self.conception_edit.setStyleSheet(PregnancyEditorStyles.date_edit())
        form_layout.addWidget(self.conception_edit)

        main_layout.addWidget(form_frame)

        info_frame = QFrame()
        info_frame.setStyleSheet(PregnancyEditorStyles.info_frame())
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(12)

        info_title = QLabel("📊 Поточна інформація")
        info_title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        info_title.setStyleSheet(PregnancyEditorStyles.info_title())
        info_layout.addWidget(info_title)

        self.week_label = QLabel("⏱️ Поточний термін: не визначено")
        self.week_label.setFont(QFont('Segoe UI', 15, QFont.Weight.Normal))
        self.week_label.setStyleSheet(PregnancyEditorStyles.info_label())
        info_layout.addWidget(self.week_label)

        self.days_left_label = QLabel("⏳ До пологів: не визначено")
        self.days_left_label.setFont(QFont('Segoe UI', 15, QFont.Weight.Normal))
        self.days_left_label.setStyleSheet(PregnancyEditorStyles.info_label())
        info_layout.addWidget(self.days_left_label)

        main_layout.addWidget(info_frame)

        save_btn = QPushButton("💾 Зберегти зміни")
        save_btn.setMinimumHeight(58)
        save_btn.setStyleSheet(PregnancyEditorStyles.save_button())
        save_btn.clicked.connect(self.save_pregnancy_data)
        main_layout.addWidget(save_btn)

        self.last_period_edit.dateChanged.connect(self.on_dates_changed)
        self.conception_edit.dateChanged.connect(self.on_dates_changed)

    def on_dates_changed(self):
        self.update_due_date()
        self.update_pregnancy_info()

    def update_due_date(self):
        conception_date = self.conception_edit.date()
        due_date = conception_date.addDays(266)
        self.due_date_label_value.setText(f"🎯 {due_date.toString('dd.MM.yyyy')}")

    def validate_dates(self):
        last_period_date = self.last_period_edit.date()
        conception_date = self.conception_edit.date()

        last_period_py = datetime(last_period_date.year(), last_period_date.month(), last_period_date.day()).date()
        conception_py = datetime(conception_date.year(), conception_date.month(), conception_date.day()).date()

        if last_period_py > conception_py:
            QMessageBox.warning(self, "⚠️ Помилка дат",
                                "Дата останньої менструації не може бути пізніше дати зачаття.\n\n"
                                "💡 Зачаття зазвичай відбувається приблизно через 14 днів після початку останньої менструації.")
            return False

        days_diff = (conception_py - last_period_py).days
        if days_diff > 28:
            result = QMessageBox.question(self, "🤔 Перевірте дати",
                                          "Дата зачаття виглядає занадто пізньою.\n\n"
                                          "💡 Зазвичай зачаття відбувається протягом 2-3 тижнів після початку останньої менструації.\n\n"
                                          "Продовжити зі збереженням?",
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if result == QMessageBox.StandardButton.No:
                return False

        return True

    def load_pregnancy_data(self):
        if not self.init_data_controller():
            logger.warning("Не вдалося ініціалізувати DataController")
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))
            self.update_due_date()
            self.week_label.setText("⏱️ Поточний термін: не визначено")
            self.days_left_label.setText("⏳ До пологів: не визначено")
            return

        pregnancy = self.data_controller.pregnancy_data

        if pregnancy and pregnancy.last_period_date:
            qdate = QDate(pregnancy.last_period_date.year, pregnancy.last_period_date.month,
                          pregnancy.last_period_date.day)
            self.last_period_edit.setDate(qdate)
        else:
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))

        if pregnancy and pregnancy.conception_date:
            qdate = QDate(pregnancy.conception_date.year, pregnancy.conception_date.month,
                          pregnancy.conception_date.day)
            self.conception_edit.setDate(qdate)
        else:
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))

        self.update_due_date()
        self.update_pregnancy_info()

    def update_pregnancy_info(self):
        if not self.data_controller:
            if not self.init_data_controller():
                self.week_label.setText("⏱️ Поточний термін: не визначено")
                self.days_left_label.setText("⏳ До пологів: не визначено")
                return

        current_week = self.data_controller.get_current_week()

        conception_date = self.conception_edit.date()
        due_date = conception_date.addDays(266)
        due_date_py = datetime(due_date.year(), due_date.month(), due_date.day()).date()
        days_left = (due_date_py - datetime.now().date()).days

        if current_week:
            self.week_label.setText(f"⏱️ Поточний термін: {current_week} тижнів")
        else:
            self.week_label.setText("⏱️ Поточний термін: не визначено")

        if days_left >= 0:
            self.days_left_label.setText(f"⏳ До пологів залишилось: {days_left} днів")
        else:
            self.days_left_label.setText("⏳ До пологів: не визначено")

    def save_pregnancy_data(self):
        if not self.data_controller or not self.data_controller.pregnancy_data:
            QMessageBox.warning(self, "❌ Помилка", "Неможливо зберегти дані - користувач не авторизований")
            return

        if not self.validate_dates():
            return

        pregnancy = self.data_controller.pregnancy_data

        last_period = self.last_period_edit.date()
        pregnancy.last_period_date = datetime(last_period.year(), last_period.month(), last_period.day()).date()

        conception = self.conception_edit.date()
        pregnancy.conception_date = datetime(conception.year(), conception.month(), conception.day()).date()

        try:
            self.data_controller.save_pregnancy_data()
            self.update_pregnancy_info()
            QMessageBox.information(self, "✅ Успіх", "Дані про вагітність успішно збережено!")
            logger.info("Дані про вагітність збережено")
        except Exception as e:
            QMessageBox.critical(self, "❌ Помилка", f"Помилка збереження: {str(e)}")
            logger.error(f"Помилка збереження даних про вагітність: {str(e)}")

    def showEvent(self, event):
        super().showEvent(event)
        self.load_pregnancy_data()