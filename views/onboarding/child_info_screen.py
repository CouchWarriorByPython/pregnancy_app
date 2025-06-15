from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QMessageBox, QSpacerItem, QSizePolicy
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledCheckBox, StyledButton, TitleLabel, StyledScrollArea
from styles import OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('child_info_screen')


class ChildInfoScreen(QWidget, UserMixin):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.name_input = StyledInput("")
        self.name_input.setStyleSheet(OnboardingScreenStyles.onboarding_input())

        self.first_labour_checkbox = StyledCheckBox("Це мої перші пологи")
        self.first_labour_checkbox.setStyleSheet(OnboardingScreenStyles.checkbox_style())

        self.gender_group = QButtonGroup(self)

    def _setup_ui(self):
        self.setStyleSheet(OnboardingScreenStyles.main_container())
        
        # Встановлюємо адаптивну політику розміру
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)  # Контролюємо відступи вручну

        # Заголовок (без фону)
        title = TitleLabel("Інформація про дитину")
        title.setStyleSheet(OnboardingScreenStyles.step_title())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(title)

        # Підзаголовок
        subtitle = QLabel("Розкажіть нам про вашу дитину")
        subtitle.setStyleSheet(OnboardingScreenStyles.subtitle())
        subtitle.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(subtitle)

        # Відступ після підзаголовка (24px)
        main_layout.addItem(QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Ім'я дитини - лейбл
        name_label = QLabel("🏷️ Ім'я дитини")
        name_label.setStyleSheet(OnboardingScreenStyles.field_label())
        name_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(name_label)

        # Поле введення (стиль як дата народження)
        self.name_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(self.name_input)

        # Тільки одна підказка під полем
        name_hint = QLabel("Залиште поле порожнім, якщо ви ще не обрали ім'я")
        name_hint.setStyleSheet(OnboardingScreenStyles.hint())
        name_hint.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(name_hint)

        # Відступ (32px)
        main_layout.addItem(QSpacerItem(20, 32, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Чекбокс (чистий стиль)
        self.first_labour_checkbox.setText("✅ Це мої перші пологи")
        self.first_labour_checkbox.setStyleSheet(OnboardingScreenStyles.checkbox_style())
        self.first_labour_checkbox.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(self.first_labour_checkbox)

        # Відступ (32px)
        main_layout.addItem(QSpacerItem(20, 32, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Стать дитини (без фонової лінії)
        gender_label = QLabel("🧬 Стать дитини:")
        gender_label.setStyleSheet(OnboardingScreenStyles.field_label())
        gender_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(gender_label)

        # Відступ перед радіокнопками (8px)
        main_layout.addItem(QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Радіокнопки (чистий стиль, без фонів)
        gender_options = [
            ("♂ Хлопчик", "Хлопчик"), 
            ("♀ Дівчинка", "Дівчинка"), 
            ("⚧ Ще не знаю", "Невідомо")
        ]

        for i, (text, value) in enumerate(gender_options):
            radio = QRadioButton(text)
            radio.setStyleSheet(OnboardingScreenStyles.gender_radio())
            radio.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            radio.gender_value = value
            self.gender_group.addButton(radio, i)
            main_layout.addWidget(radio)

            # За замовчуванням вибираємо "Ще не знаю"
            if i == 2:
                radio.setChecked(True)

        # Розтягуючий spacer - кнопка завжди внизу з відступом
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Кнопка з відступами зверху та знизу
        next_btn = StyledButton("Далі")
        next_btn.setStyleSheet(OnboardingScreenStyles.onboarding_button())
        next_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        next_btn.setMinimumHeight(50)
        next_btn.clicked.connect(self._on_next_clicked)
        main_layout.addWidget(next_btn)

        # Відступ знизу для кнопки
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

    def _on_next_clicked(self):
        user_id = self.get_current_user_id()
        if not user_id:
            show_error(self, "Помилка", "Користувач не авторизований")
            return

        child_data = {
            "name": self.name_input.text().strip(),
            "first_labour": self.first_labour_checkbox.isChecked(),
            "gender": self._get_selected_gender()
        }
        logger.info(f"Дані дитини зібрані: {child_data}")
        self.proceed_signal.emit(child_data)

    def _get_selected_gender(self):
        selected_button = self.gender_group.checkedButton()
        return selected_button.gender_value if selected_button else "Невідомо"