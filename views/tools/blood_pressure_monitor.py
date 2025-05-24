from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                             QMessageBox, QSplitter, QFormLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QDate, QTime
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledDateEdit, StyledTimeEdit, StyledSpinBox,
                               StyledInput, StyledButton, StyledListWidget, TitleLabel)
from styles.tools import BloodPressureStyles
from styles.base import BaseStyles

logger = get_logger('blood_pressure_monitor')


class BloodPressureMonitorScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_pressure_records()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = TitleLabel("Моніторинг артеріального тиску", 22)
        title.setStyleSheet("color: #E91E63; font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = StyledCard("Додати новий запис")
        form_frame.setStyleSheet(BloodPressureStyles.pressure_card())

        info_text = """
        <p>Регулярне вимірювання артеріального тиску важливе під час вагітності для раннього виявлення 
        можливих ускладнень.</p>
        <p>Нормальний тиск під час вагітності: 110-120/70-80 мм рт.ст.</p>
        <p>Підвищений тиск може бути ознакою прееклампсії і потребує консультації лікаря.</p>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet(BaseStyles.text_secondary())
        form_frame.layout.addWidget(info_label)

        input_form = QFormLayout()

        self.date_edit = StyledDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        input_form.addRow("Дата:", self.date_edit)

        self.time_edit = StyledTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        input_form.addRow("Час:", self.time_edit)

        self.systolic_spin = StyledSpinBox(80, 200)
        self.systolic_spin.setValue(120)
        input_form.addRow("Верхній тиск:", self.systolic_spin)

        self.diastolic_spin = StyledSpinBox(40, 120)
        self.diastolic_spin.setValue(80)
        input_form.addRow("Нижній тиск:", self.diastolic_spin)

        self.pulse_spin = StyledSpinBox(40, 200)
        self.pulse_spin.setValue(75)
        input_form.addRow("Пульс:", self.pulse_spin)

        self.notes_edit = StyledInput("Додаткові нотатки (необов'язково)")
        input_form.addRow("Нотатки:", self.notes_edit)

        form_frame.layout.addLayout(input_form)
        form_frame.layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        save_btn = StyledButton("Зберегти запис")
        save_btn.setStyleSheet(BloodPressureStyles.pressure_button())
        save_btn.clicked.connect(self.save_pressure)
        form_frame.layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = StyledCard("Історія вимірювань")
        list_frame.setStyleSheet(BloodPressureStyles.pressure_card())

        self.pressure_list = StyledListWidget()
        list_frame.layout.addWidget(self.pressure_list)

        buttons_layout = QHBoxLayout()

        refresh_btn = StyledButton("Оновити список", "secondary")
        refresh_btn.clicked.connect(self.load_pressure_records)

        period_label = QLabel("Показати за:")
        period_label.setStyleSheet(BaseStyles.text_primary())

        self.period_spin = StyledSpinBox(7, 90, " днів")
        self.period_spin.setValue(30)
        self.period_spin.valueChanged.connect(self.load_pressure_records)

        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(period_label)
        buttons_layout.addWidget(self.period_spin)

        list_frame.layout.addLayout(buttons_layout)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_pressure_records(self):
        try:
            days = self.period_spin.value() if hasattr(self, 'period_spin') else 30
            records = self.data_controller.db.get_blood_pressure(days)
            self.pressure_list.clear()

            for record in records:
                item_text = f"{record['date']} {record['time']}: {record['systolic']}/{record['diastolic']} мм рт.ст."
                if record['pulse']:
                    item_text += f", пульс: {record['pulse']}"
                if record['notes']:
                    item_text += f" - {record['notes']}"
                self.pressure_list.addItem(item_text)

            logger.info(f"Завантажено {len(records)} записів про тиск за {days} днів")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити записи про тиск: {str(e)}")
            logger.error(f"Помилка при завантаженні записів про тиск: {str(e)}")

    def save_pressure(self):
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            time_str = self.time_edit.time().toString("HH:mm")
            systolic = self.systolic_spin.value()
            diastolic = self.diastolic_spin.value()
            pulse = self.pulse_spin.value()
            notes = self.notes_edit.text().strip()

            if systolic <= diastolic:
                QMessageBox.warning(self, "Попередження",
                                    "Верхній тиск повинен бути більшим за нижній.\nПеревірте правильність введених значень.")
                return

            self.data_controller.db.add_blood_pressure(date_str, time_str, systolic, diastolic, pulse, notes)
            self.notes_edit.clear()
            self.load_pressure_records()

            QMessageBox.information(self, "Успіх", "Запис тиску успішно збережено")
            logger.info(f"Збережено новий запис тиску: {date_str} {time_str}, {systolic}/{diastolic}, пульс: {pulse}")

            if systolic >= 140 or diastolic >= 90:
                QMessageBox.warning(self, "Увага! Підвищений тиск",
                                    f"Ваш тиск {systolic}/{diastolic} мм рт.ст. перевищує норму.\n"
                                    "Рекомендується проконсультуватися з лікарем.")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису тиску: {str(e)}")