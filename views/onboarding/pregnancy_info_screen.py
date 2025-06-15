from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QMessageBox
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtCore import Qt
from utils.logger import get_logger
from utils.base_widgets import StyledButton, TitleLabel, StyledDateEdit
from styles import OnboardingScreenStyles
from datetime import datetime
from utils.user_mixin import UserMixin

logger = get_logger('pregnancy_info_screen')


class PregnancyInfoScreen(QWidget, UserMixin):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(OnboardingScreenStyles.main_container())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)  # Контролюємо відступи вручну

        # Заголовок
        title = TitleLabel("Інформація про вагітність", 28)
        title.setStyleSheet(OnboardingScreenStyles.step_title())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Підзаголовок
        subtitle = QLabel("Вкажіть дати для розрахунку терміну вагітності")
        subtitle.setStyleSheet(OnboardingScreenStyles.subtitle())
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        main_layout.addWidget(subtitle)

        # Відступ після заголовків (24px)
        main_layout.addItem(QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Група 1: Дата останньої менструації
        last_period_label = QLabel("Дата останньої менструації:")
        last_period_label.setStyleSheet(OnboardingScreenStyles.field_label())
        main_layout.addWidget(last_period_label)

        self.last_period_edit = StyledDateEdit()
        self.last_period_edit.setDate(QDate.currentDate().addDays(-280))
        self.last_period_edit.setMinimumHeight(50)
        self.last_period_edit.dateChanged.connect(self.update_due_date)
        main_layout.addWidget(self.last_period_edit)

        last_period_hint = QLabel("Перший день останнього менструального циклу")
        last_period_hint.setStyleSheet(OnboardingScreenStyles.hint())
        main_layout.addWidget(last_period_hint)

        # Відступ між групами (32px)
        main_layout.addItem(QSpacerItem(20, 32, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Група 2: Очікувана дата пологів
        due_date_label = QLabel("Очікувана дата пологів (розраховується автоматично):")
        due_date_label.setStyleSheet(OnboardingScreenStyles.field_label())
        main_layout.addWidget(due_date_label)

        self.due_date_label_value = QLabel()
        self.due_date_label_value.setStyleSheet(OnboardingScreenStyles.hint())
        main_layout.addWidget(self.due_date_label_value)

        # Відступ між групами (32px)
        main_layout.addItem(QSpacerItem(20, 32, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Група 3: Дата зачаття
        conception_label = QLabel("Дата зачаття (якщо відома):")
        conception_label.setStyleSheet(OnboardingScreenStyles.field_label())
        main_layout.addWidget(conception_label)

        self.conception_edit = StyledDateEdit()
        self.conception_edit.setDate(QDate.currentDate().addDays(-266))
        self.conception_edit.setMinimumHeight(50)
        main_layout.addWidget(self.conception_edit)

        conception_hint = QLabel("Зазвичай відбувається через 14 днів після початку менструації")
        conception_hint.setStyleSheet(OnboardingScreenStyles.hint())
        main_layout.addWidget(conception_hint)

        # Розтягуючий spacer - кнопка завжди внизу
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Кнопка завершення
        next_btn = StyledButton("ЗАВЕРШИТИ")
        next_btn.setMinimumHeight(60)
        next_btn.setStyleSheet(OnboardingScreenStyles.onboarding_button())
        next_btn.clicked.connect(self.on_next_clicked)
        main_layout.addWidget(next_btn)

        # Відступ знизу для кнопки
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.update_due_date()

    def update_due_date(self):
        last_period_date = self.last_period_edit.date()
        due_date = last_period_date.addDays(280)
        self.due_date_label_value.setText(due_date.toString("dd.MM.yyyy"))

        conception_date = last_period_date.addDays(14)
        self.conception_edit.setDate(conception_date)

    def on_next_clicked(self):
        user_id = self.get_current_user_id()
        if not user_id:
            show_error(self, "Помилка", "Користувач не авторизований")
            return

        last_period_date = self.last_period_edit.date()
        conception_date = self.conception_edit.date()

        last_period_date_obj = datetime(last_period_date.year(), last_period_date.month(),
                                        last_period_date.day()).date()
        conception_date_obj = datetime(conception_date.year(), conception_date.month(), conception_date.day()).date()

        if last_period_date_obj > conception_date_obj:
            show_warning(self, "Помилка",
                                "Дата останньої менструації не може бути пізніше дати зачаття.\n"
                                "Зачаття зазвичай відбувається приблизно через 14 днів після початку останньої менструації.")
            return

        days_diff = (conception_date_obj - last_period_date_obj).days
        if days_diff > 28:
            show_warning(self, "Увага",
                                "Дата зачаття виглядає занадто пізньою.\n"
                                "Зазвичай зачаття відбувається протягом 2-3 тижнів після початку останньої менструації.")

        pregnancy_data = {
            "last_period_date": last_period_date.toString("yyyy-MM-dd"),
            "conception_date": conception_date.toString("yyyy-MM-dd")
        }

        logger.info(f"Дані про вагітність зібрані: {pregnancy_data}")
        self.proceed_signal.emit(pregnancy_data)