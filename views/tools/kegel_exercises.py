import os
import subprocess
import platform
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from utils.message_utils import show_info, show_warning, show_error
from utils.logger import get_logger
from utils.base_widgets import TitleLabel, StyledButton
from styles import KegelExercisesStyles
from utils.user_mixin import UserMixin

logger = get_logger('kegel_exercises')


class KegelExercisesScreen(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(12)

        # Простий заголовок
        title = TitleLabel("Вправи Кегеля", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Спеціальні вправи для зміцнення м'язів тазового дна")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Відступ
        main_layout.addSpacing(20)

        # Інформація без фону
        info_title = QLabel("💪 Переваги вправ Кегеля")
        info_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(info_title)

        benefits_text = """• Зміцнити м'язи, які підтримують матку, сечовий міхур та кишечник
• Покращити контроль над сечовим міхуром
• Підготувати до пологів
• Прискорити відновлення після пологів"""

        benefits_label = QLabel(benefits_text)
        benefits_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; background: transparent; border: none;")
        benefits_label.setWordWrap(True)
        main_layout.addWidget(benefits_label)

        # Відступ
        main_layout.addSpacing(20)

        instruction_label = QLabel("📖 Натисніть кнопку нижче, щоб відкрити детальну інструкцію у PDF-форматі")
        instruction_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; background: transparent; border: none;")
        instruction_label.setWordWrap(True)
        main_layout.addWidget(instruction_label)

        # Розтягуючий spacer
        main_layout.addStretch()

        # Компактна кнопка
        open_pdf_btn = StyledButton("📄 Відкрити інструкцію з вправами")
        open_pdf_btn.setMinimumHeight(44)
        open_pdf_btn.setStyleSheet(KegelExercisesStyles.exercise_button())
        open_pdf_btn.clicked.connect(self.open_pdf)
        main_layout.addWidget(open_pdf_btn)

    def open_pdf(self):
        try:
            pdf_path = os.path.join("resources", "Kegels_exercises.pdf")

            if not os.path.exists(pdf_path):
                show_warning(self, "Файл не знайдено",
                                    f"Файл {pdf_path} не знайдено.\nПеревірте наявність файлу в папці ресурсів.")
                logger.error(f"Файл не знайдено: {pdf_path}")
                return

            system = platform.system()

            if system == "Windows":
                os.startfile(pdf_path)
            elif system == "Darwin":
                subprocess.call(["open", pdf_path])
            else:
                subprocess.call(["xdg-open", pdf_path])

            logger.info(f"Відкрито PDF-файл: {pdf_path}")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося відкрити файл: {str(e)}")
            logger.error(f"Помилка при відкритті PDF: {str(e)}")