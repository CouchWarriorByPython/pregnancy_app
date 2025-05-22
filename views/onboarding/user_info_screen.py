from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QAbstractSpinBox,
                             QLineEdit, QCheckBox, QPushButton, QDateEdit,
                             QDoubleSpinBox, QSpinBox, QFormLayout, QScrollArea)
from PyQt6.QtCore import pyqtSignal, QDate, Qt
from utils.logger import get_logger
from datetime import datetime
from controllers.data_controller import DataController

logger = get_logger('user_info_screen')

class UserInfoScreen(QWidget):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.user_name_input = None
        self.birth_date_edit = None
        self.weight_spin = None
        self.height_spin = None
        self.cycle_spin = None
        self.diet_checkboxes = {}
        self.setup_ui()
        self.load_user_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)

        user_title = QLabel("Інформація про вас")
        user_title.setStyleSheet("color: #FF8C00; font-size: 18px; font-weight: bold;")
        form_layout.addWidget(user_title)

        profile_form = QFormLayout()
        profile_form.setSpacing(15)

        self.user_name_input = QLineEdit()
        self.user_name_input.setObjectName("user_name_input")
        self.user_name_input.setPlaceholderText("Введіть ваше ім'я")
        self.user_name_input.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
            min-height: 30px;
        """)
        profile_form.addRow("Ваше ім'я:", self.user_name_input)

        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setObjectName("birth_date_edit")
        self.birth_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.birth_date_edit.setMinimumHeight(40)
        self.birth_date_edit.setDate(QDate.currentDate().addYears(-25))
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        profile_form.addRow("Дата народження:", self.birth_date_edit)

        spinbox_style = """
            {widget_type} {{
                background-color: #222222;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
                color: white;
            }}
        """

        def setup_spinbox_common_properties(spinbox):
            spinbox.setMinimumHeight(40)
            spinbox.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)

        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setObjectName("weight_spin")
        self.weight_spin.setRange(30.0, 150.0)
        self.weight_spin.setDecimals(1)
        self.weight_spin.setValue(60.0)
        self.weight_spin.setSuffix(" кг")
        self.weight_spin.setSingleStep(0.1)
        setup_spinbox_common_properties(self.weight_spin)
        self.weight_spin.setStyleSheet(spinbox_style.format(widget_type="QDoubleSpinBox"))
        profile_form.addRow("Вага до вагітності:", self.weight_spin)

        self.height_spin = QSpinBox()
        self.height_spin.setObjectName("height_spin")
        self.height_spin.setRange(100, 220)
        self.height_spin.setValue(165)
        self.height_spin.setSuffix(" см")
        self.height_spin.setSingleStep(1)
        setup_spinbox_common_properties(self.height_spin)
        self.height_spin.setStyleSheet(spinbox_style.format(widget_type="QSpinBox"))
        profile_form.addRow("Зріст:", self.height_spin)

        self.cycle_spin = QSpinBox()
        self.cycle_spin.setObjectName("cycle_spin")
        self.cycle_spin.setRange(21, 35)
        self.cycle_spin.setValue(28)
        self.cycle_spin.setSuffix(" днів")
        self.cycle_spin.setSingleStep(1)
        setup_spinbox_common_properties(self.cycle_spin)
        self.cycle_spin.setStyleSheet(spinbox_style.format(widget_type="QSpinBox"))
        profile_form.addRow("Середня тривалість циклу:", self.cycle_spin)

        diet_label = QLabel("Дієтичні вподобання:")
        diet_label.setStyleSheet("color: white;")
        form_layout.addLayout(profile_form)
        form_layout.addWidget(diet_label)

        diet_options = ["Вегетаріанство", "Веганство", "Безглютенова дієта", "Низьколактозна дієта"]

        for option in diet_options:
            box = QCheckBox(option)
            box.setObjectName(f"diet_{option.lower().replace(' ', '_')}")
            box.setStyleSheet("""
                QCheckBox {
                    color: white;
                    font-size: 14px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border-radius: 4px;
                    border: 2px solid #444444;
                }
                QCheckBox::indicator:checked {
                    background-color: #4CAF50;
                    border: 2px solid #4CAF50;
                }
            """)
            self.diet_checkboxes[option] = box
            form_layout.addWidget(box)

        form_layout.addStretch(1)

        finish_btn = QPushButton("Завершити")
        finish_btn.setObjectName("finish_btn")
        finish_btn.setMinimumHeight(50)
        finish_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF8C00;
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
        """)
        finish_btn.clicked.connect(self.on_finish_clicked)
        form_layout.addWidget(finish_btn)

        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)

    def load_user_data(self):
        try:
            profile = self.data_controller.user_profile
            if profile:
                self.user_name_input.setText(profile.name or "")

                if profile.birth_date:
                    qdate = QDate(profile.birth_date.year, profile.birth_date.month, profile.birth_date.day)
                    self.birth_date_edit.setDate(qdate)

                self.weight_spin.setValue(profile.weight_before_pregnancy or 60.0)
                self.height_spin.setValue(profile.height or 165)
                self.cycle_spin.setValue(profile.cycle_length or 28)

                diet_preferences = self.data_controller.db.get_diet_preferences()
                for option, checkbox in self.diet_checkboxes.items():
                    checkbox.setChecked(option in diet_preferences)

                logger.info(f"Дані користувача {profile.name} завантажено")
        except Exception as e:
            logger.error(f"Помилка при завантаженні даних користувача: {e}")

    def on_finish_clicked(self):
        logger.info("Натиснуто кнопку 'Завершити'")
        birth_date = self.birth_date_edit.date()
        birth_date_obj = datetime(birth_date.year(), birth_date.month(), birth_date.day()).date()

        diet_preferences = [option for option, checkbox in self.diet_checkboxes.items()
                           if checkbox.isChecked()]

        user_data = {
            "name": self.user_name_input.text().strip(),
            "birth_date": birth_date_obj.isoformat(),
            "weight_before_pregnancy": self.weight_spin.value(),
            "height": self.height_spin.value(),
            "cycle_length": self.cycle_spin.value(),
            "diet_preferences": diet_preferences
        }

        logger.info(f"Дані користувача зібрані: {user_data}")

        try:
            profile = self.data_controller.user_profile
            profile.name = user_data["name"]
            profile.birth_date = birth_date_obj
            profile.weight_before_pregnancy = user_data["weight_before_pregnancy"]
            profile.height = user_data["height"]
            profile.cycle_length = user_data["cycle_length"]

            self.data_controller.db.update_diet_preferences(user_data["diet_preferences"])
            self.data_controller.save_user_profile()
            logger.info("Профіль користувача збережено")

            self.proceed_signal.emit(user_data)
        except Exception as e:
            logger.error(f"Помилка при збереженні даних користувача: {e}")