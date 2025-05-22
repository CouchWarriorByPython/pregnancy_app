import os
import subprocess
import platform
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from utils.logger import get_logger
from utils.base_widgets import TitleLabel, StyledButton
from utils.styles import Styles

logger = get_logger('kegel_exercises')


class KegelExercisesScreen(QWidget):
    """Екран для роботи з вправами Кегеля"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = TitleLabel("Вправи Кегеля", 22)
        title.setStyleSheet("color: #9C27B0;")
        main_layout.addWidget(title)

        info_text = """
        <p>Вправи Кегеля - це спеціальні вправи для зміцнення м'язів тазового дна.</p>
        <p>Регулярне виконання вправ Кегеля під час вагітності може:</p>
        <ul>
            <li>Зміцнити м'язи, які підтримують матку, сечовий міхур та кишечник</li>
            <li>Покращити контроль над сечовим міхуром</li>
            <li>Підготувати до пологів</li>
            <li>Прискорити відновлення після пологів</li>
        </ul>
        <p>Натисніть кнопку нижче, щоб відкрити детальну інструкцію у PDF-форматі.</p>
        """

        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet(f"""
            color: {Styles.COLORS['text_primary']};
            background-color: {Styles.COLORS['surface']};
            padding: 15px;
            border-radius: 10px;
        """)
        main_layout.addWidget(info_label)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        open_pdf_btn = StyledButton("Відкрити інструкцію з вправами")
        open_pdf_btn.setMinimumHeight(50)
        open_pdf_btn.setMinimumWidth(250)
        open_pdf_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #9C27B0;
                color: white;
                border-radius: 25px;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: #7B1FA2;
            }}
            QPushButton:pressed {{
                background-color: #6A1B9A;
            }}
        """)
        open_pdf_btn.clicked.connect(self.open_pdf)

        button_layout.addWidget(open_pdf_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def open_pdf(self):
        """Відкриває PDF-файл з вправами Кегеля"""
        try:
            pdf_path = os.path.join("resources", "Вправи Кегеля.pdf")

            if not os.path.exists(pdf_path):
                QMessageBox.warning(self, "Файл не знайдено",
                                    f"Файл {pdf_path} не знайдено.\nБудь ласка, перевірте наявність файлу в папці ресурсів.")
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
            QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити файл: {str(e)}")
            logger.error(f"Помилка при відкритті PDF: {str(e)}")