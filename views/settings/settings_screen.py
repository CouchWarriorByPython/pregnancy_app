from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.logger import get_logger
from utils.user_mixin import UserMixin
from styles import SettingsScreenStyles
from .profile_editor import ProfileEditor
from .pregnancy_editor import PregnancyEditor
from .child_info_editor import ChildInfoEditor
from .password_editor import PasswordEditor

logger = get_logger('settings_screen')


class SettingsScreen(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._init_editors()
        self._setup_ui()

    def _init_editors(self):
        """Ініціалізує всі редактори"""
        self.editors = [
            ("Профіль", ProfileEditor(self)),
            ("Вагітність", PregnancyEditor(self)),
            ("Дитина", ChildInfoEditor(self)),
            ("Пароль", PasswordEditor(self))
        ]
        for _, editor in self.editors:
            editor.hide()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._create_header())
        main_layout.addWidget(self._create_tab_selector())
        main_layout.addWidget(self._create_content_container())
        main_layout.addWidget(self._create_logout_section())

        self.set_tab(0)

    def _create_header(self):
        header = QWidget()
        header.setMinimumHeight(50)
        header.setStyleSheet("background: transparent; border: none;")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 8, 20, 8)

        title_label = QLabel("⚙️ Налаштування")
        title_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        return header

    def _create_tab_selector(self):
        tab_selector = QWidget()
        tab_selector.setFixedHeight(60)
        tab_selector.setStyleSheet("background: transparent; border: none;")

        layout = QHBoxLayout(tab_selector)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(4)

        self.tab_buttons = []
        tab_icons = ["👤", "🤰", "👶", "🔐"]

        for i, (name, _) in enumerate(self.editors):
            btn = QPushButton(f"{tab_icons[i]} {name}")
            btn.setCheckable(True)
            btn.setFixedHeight(48)
            btn.setStyleSheet(SettingsScreenStyles.tab_button())
            btn.clicked.connect(lambda checked, idx=i: self.set_tab(idx))
            layout.addWidget(btn)
            self.tab_buttons.append(btn)

        return tab_selector

    def _create_content_container(self):
        self.content_container = QWidget()
        self.content_container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self.content_container)
        layout.setContentsMargins(0, 0, 0, 0)

        for _, editor in self.editors:
            layout.addWidget(editor)

        return self.content_container

    def _create_logout_section(self):
        logout_section = QWidget()
        logout_section.setMinimumHeight(70)
        logout_section.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(logout_section)
        layout.setContentsMargins(24, 12, 24, 12)

        logout_btn = QPushButton("🚪 Вийти")
        logout_btn.setMinimumHeight(46)
        logout_btn.setStyleSheet(SettingsScreenStyles.logout_button())
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        return logout_section

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Підтвердження виходу",
            "Ви впевнені, що хочете вийти з акаунту?\n\nВсі незбережені зміни будуть втрачені.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            main_window = self._find_main_window()
            if main_window and hasattr(main_window, 'logout'):
                main_window.logout()
            else:
                QMessageBox.warning(self, "Помилка", "Не вдалося вийти з системи")

    def set_tab(self, index):
        """Перемикає між табами редакторів"""
        current_size = self.window().size() if self.window() else None

        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)

        for i, (_, editor) in enumerate(self.editors):
            editor.setVisible(i == index)

        if self.window() and current_size and self.window().size() != current_size:
            self.window().resize(current_size)

    def showEvent(self, event):
        """Викликається при показі екрану"""
        super().showEvent(event)
        if self.init_data_controller():
            logger.info(f"SettingsScreen ініціалізований з user_id: {self.get_current_user_id()}")
            for i, (_, editor) in enumerate(self.editors):
                if editor.isVisible() and hasattr(editor, 'load_data'):
                    try:
                        editor.load_data()
                    except Exception as e:
                        logger.error(f"Помилка завантаження даних для {editor.__class__.__name__}: {str(e)}")
        else:
            logger.warning("SettingsScreen: не вдалося ініціалізувати DataController")