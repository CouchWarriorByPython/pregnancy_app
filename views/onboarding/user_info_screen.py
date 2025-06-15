from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLabel, QMessageBox, 
                             QSpacerItem, QSizePolicy, QScrollArea, QFrame)
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtCore import pyqtSignal, QDate, Qt
from PyQt6.QtWidgets import QAbstractSpinBox
from utils.logger import get_logger
from utils.base_widgets import (StyledInput, StyledDateEdit, StyledDoubleSpinBox, StyledSpinBox,
                                StyledButton, TitleLabel)
from datetime import datetime
from controllers.data_controller import DataController
from styles import OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('user_info_screen')


class UserInfoScreen(QWidget, UserMixin):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.user_name_input = StyledInput("Введіть ваше ім'я")
        self.user_name_input.setStyleSheet(OnboardingScreenStyles.elegant_input())
        
        self.birth_date_input = StyledDateEdit()
        self.birth_date_input.setDate(QDate.currentDate().addYears(-25))
        self.birth_date_input.setCalendarPopup(False)
        self.birth_date_input.setStyleSheet(OnboardingScreenStyles.date_field_clean())

        self.weight_spin = StyledDoubleSpinBox(30.0, 150.0, 1, " кг")
        self.weight_spin.setValue(60.0)
        self.weight_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.weight_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.height_spin = StyledSpinBox(100, 220, " см")
        self.height_spin.setValue(165)
        self.height_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.height_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.cycle_spin = StyledSpinBox(21, 35, " днів")
        self.cycle_spin.setValue(28)
        self.cycle_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.cycle_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

    def _setup_ui(self):
        self.setStyleSheet(OnboardingScreenStyles.main_container())
        
        # Встановлюємо адаптивну політику розміру
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Основний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area для контенту
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # Контейнер для контенту
        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 20)
        content_layout.setSpacing(16)

        # Заголовок
        title = TitleLabel("Інформація про вас")
        title.setStyleSheet(OnboardingScreenStyles.step_title())
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)

        # Підзаголовок
        subtitle = QLabel("Розкажіть нам про себе")
        subtitle.setStyleSheet(OnboardingScreenStyles.user_info_subtitle())
        subtitle.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        content_layout.addWidget(subtitle)

        content_layout.addItem(QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Група 1: Особисті дані
        personal_group = self._create_form_group("👤 Особисті дані", [
            ("Ваше ім'я:", self.user_name_input),
            ("Дата народження:", self.birth_date_input)
        ])
        content_layout.addLayout(personal_group)

        content_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Група 2: Параметри тіла
        body_group = self._create_form_group("📏 Параметри тіла", [
            ("Вага до вагітності:", self.weight_spin),
            ("Зріст:", self.height_spin)
        ])
        content_layout.addLayout(body_group)

        content_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Група 3: Менструальний цикл
        cycle_group = self._create_form_group("🗓️ Менструальний цикл", [
            ("Середня тривалість циклу:", self.cycle_spin)
        ])
        content_layout.addLayout(cycle_group)

        # Розтягуючий spacer
        content_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Кнопка "Завершити" (фіксована внизу, поза scroll area)
        button_container = QFrame()
        button_container.setStyleSheet("QFrame { background: transparent; border: none; }")
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(40, 20, 40, 40)
        
        finish_btn = StyledButton("Далі")
        finish_btn.setStyleSheet(OnboardingScreenStyles.onboarding_button())
        finish_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        finish_btn.clicked.connect(self._on_finish_clicked)
        button_layout.addWidget(finish_btn)
        
        main_layout.addWidget(button_container)

    def _create_form_group(self, title, fields):
        """Створює групу полів з заголовком (без фонового контейнера)"""
        group_layout = QVBoxLayout()
        group_layout.setContentsMargins(0, 0, 0, 0)
        group_layout.setSpacing(12)

        # Заголовок групи (без фону)
        group_title = QLabel(title)
        group_title.setStyleSheet(OnboardingScreenStyles.user_info_group_label())
        group_title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        group_layout.addWidget(group_title)

        # Форма з полями
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setVerticalSpacing(12)
        form_layout.setHorizontalSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet(OnboardingScreenStyles.user_info_field_label())
            label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            label.setMinimumHeight(24)  # Зменшена висота для кращого вирівнювання
            label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            widget.setMinimumHeight(24)  # Така ж висота як у лейбла
            widget.setMaximumHeight(40)  # Обмежуємо максимальну висоту
            
            form_layout.addRow(label, widget)

        group_layout.addLayout(form_layout)
        return group_layout

    def _load_user_data(self):
        if not self.init_data_controller():
            logger.info("Не вдалося ініціалізувати DataController, залишаємо дефолтні значення")
            return

        try:
            profile = self.data_controller.user_profile

            if not profile:
                logger.info("Профіль не знайдено, залишаємо дефолтні значення")
                return

            self.user_name_input.setText(profile.name or "")

            if profile.birth_date:
                qdate = QDate(profile.birth_date.year, profile.birth_date.month, profile.birth_date.day)
                self.birth_date_input.setDate(qdate)

            self.weight_spin.setValue(profile.weight_before_pregnancy or 60.0)
            self.height_spin.setValue(profile.height or 165)
            self.cycle_spin.setValue(profile.cycle_length or 28)

            logger.info(f"Дані користувача {profile.name} завантажено")
        except Exception as e:
            logger.error(f"Помилка при завантаженні даних користувача: {e}")

    def _on_finish_clicked(self):
        logger.info("Натиснуто кнопку 'Завершити'")

        user_id = self.get_current_user_id()
        if not user_id:
            show_error(self, "Помилка", "Користувач не авторизований")
            return

        # Отримання дати з QDateEdit
        birth_qdate = self.birth_date_input.date()
        birth_date_obj = datetime(birth_qdate.year(), birth_qdate.month(), birth_qdate.day()).date()

        user_data = {
            "name": self.user_name_input.text().strip(),
            "birth_date": birth_date_obj.isoformat(),
            "weight_before_pregnancy": self.weight_spin.value(),
            "height": self.height_spin.value(),
            "cycle_length": self.cycle_spin.value()
        }

        try:
            if not self.data_controller:
                self.init_data_controller()

            profile = self.data_controller.user_profile
            if not profile:
                show_error(self, "Помилка", "Не вдалося знайти профіль користувача")
                return

            profile.name = user_data["name"]
            profile.birth_date = birth_date_obj
            profile.weight_before_pregnancy = user_data["weight_before_pregnancy"]
            profile.height = user_data["height"]
            profile.cycle_length = user_data["cycle_length"]

            self.data_controller.save_user_profile()

            logger.info("Профіль користувача збережено")
            self.proceed_signal.emit(user_data)
        except Exception as e:
            show_error(self, "Помилка", f"Помилка при збереженні даних: {str(e)}")
            logger.error(f"Помилка при збереженні даних користувача: {e}")

    def showEvent(self, event):
        super().showEvent(event)
        self._load_user_data()