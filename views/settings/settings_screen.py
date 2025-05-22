from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont

from controllers.data_controller import DataController
from .profile_editor import ProfileEditor
from .pregnancy_editor import PregnancyEditor
from .child_info_editor import ChildInfoEditor


class SettingsScreen(QWidget):
    """Екран налаштувань додатку"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Верхній заголовок
        header = QWidget()
        header.setMinimumHeight(60)
        header.setStyleSheet("background-color: #121212;")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)

        settings_label = QLabel("Налаштування")
        settings_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        settings_label.setStyleSheet("color: #FF8C00;")

        header_layout.addWidget(settings_label)
        main_layout.addWidget(header)

        # Панель з кнопками вибору категорії налаштувань
        tab_selector = QWidget()
        tab_selector.setFixedHeight(50)
        tab_selector.setStyleSheet("background-color: #181818;")

        tab_layout = QHBoxLayout(tab_selector)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)

        # Створення кнопок для категорій
        self.tab_buttons = []
        tab_names = ["Профіль", "Вагітність", "Дитина"]

        for i, name in enumerate(tab_names):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #121212;
                    color: #AAAAAA;
                    border: none;
                    font-size: 14px;
                    padding: 10px;
                    text-align: center;
                }
                QPushButton:checked {
                    background-color: #222222;
                    color: #FF8C00;
                    font-weight: bold;
                }
                QPushButton:hover:!checked {
                    background-color: #1A1A1A;
                }
            """)
            btn.clicked.connect(lambda checked, idx=i: self.set_tab(idx))
            tab_layout.addWidget(btn)
            self.tab_buttons.append(btn)

        main_layout.addWidget(tab_selector)

        # Контейнер для вмісту вкладок
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Створюємо редактори для кожної вкладки
        self.profile_editor = ProfileEditor()
        self.pregnancy_editor = PregnancyEditor()
        self.child_editor = ChildInfoEditor()

        # Додаємо редактори у layout і одразу приховуємо їх
        self.content_layout.addWidget(self.profile_editor)
        self.content_layout.addWidget(self.pregnancy_editor)
        self.content_layout.addWidget(self.child_editor)

        self.profile_editor.hide()
        self.pregnancy_editor.hide()
        self.child_editor.hide()

        main_layout.addWidget(self.content_container)

        # Встановлюємо початкову вкладку
        self.set_tab(0)

    def set_tab(self, index):
        """Встановлює активну вкладку налаштувань"""
        # Оновлюємо стан кнопок
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)

        # Показуємо відповідний редактор і приховуємо інші
        self.profile_editor.setVisible(index == 0)
        self.pregnancy_editor.setVisible(index == 1)
        self.child_editor.setVisible(index == 2)