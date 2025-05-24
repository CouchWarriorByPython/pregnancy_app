from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from controllers.data_controller import DataController
from styles.settings import SettingsStyles
from styles.base import BaseStyles
from .profile_editor import ProfileEditor
from .pregnancy_editor import PregnancyEditor
from .child_info_editor import ChildInfoEditor
from .password_editor import PasswordEditor


class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._init_data_controller()
        self._init_editors()
        self._setup_ui()

    def _init_data_controller(self):
        # Ініціалізуємо DataController з current_user_id
        user_id = self._get_current_user_id()
        if user_id:
            self.data_controller = DataController(user_id)
        else:
            self.data_controller = DataController()

    def _get_current_user_id(self):
        # Спочатку перевіряємо parent
        if hasattr(self.parent, 'current_user_id') and self.parent.current_user_id:
            return self.parent.current_user_id

        # Потім перевіряємо parent.parent (MainWindow)
        if (hasattr(self.parent, 'parent') and
                hasattr(self.parent.parent, 'current_user_id') and
                self.parent.parent.current_user_id):
            return self.parent.parent.current_user_id

        return None

    def _init_editors(self):
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
        header.setMinimumHeight(60)
        header.setStyleSheet(BaseStyles.header())

        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 5, 15, 5)

        label = QLabel("Налаштування")
        label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        label.setStyleSheet(BaseStyles.text_accent())
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        return header

    def _create_tab_selector(self):
        tab_selector = QWidget()
        tab_selector.setFixedHeight(70)
        tab_selector.setStyleSheet("background-color: #181818;")

        layout = QHBoxLayout(tab_selector)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_buttons = []
        for i, (name, _) in enumerate(self.editors):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setFixedHeight(70)
            btn.setStyleSheet(SettingsStyles.tab_button())
            btn.clicked.connect(lambda checked, idx=i: self.set_tab(idx))
            layout.addWidget(btn)
            self.tab_buttons.append(btn)

        return tab_selector

    def _create_content_container(self):
        self.content_container = QWidget()
        layout = QVBoxLayout(self.content_container)
        layout.setContentsMargins(0, 0, 0, 0)

        for _, editor in self.editors:
            layout.addWidget(editor)

        return self.content_container

    def _create_logout_section(self):
        logout_section = QWidget()
        logout_section.setMinimumHeight(80)
        logout_section.setStyleSheet(SettingsStyles.logout_section())

        layout = QVBoxLayout(logout_section)
        layout.setContentsMargins(20, 15, 20, 15)

        logout_btn = QPushButton("Вийти з акаунту")
        logout_btn.setMinimumHeight(50)
        logout_btn.setStyleSheet(SettingsStyles.logout_button())
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        return logout_section

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Підтвердження",
            "Ви впевнені, що хочете вийти з акаунту?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if hasattr(self.parent, 'logout'):
                self.parent.logout()

    def set_tab(self, index):
        current_size = self.window().size() if self.window() else None

        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)

        for i, (_, editor) in enumerate(self.editors):
            editor.setVisible(i == index)

        if self.window() and current_size and self.window().size() != current_size:
            self.window().resize(current_size)

    @property
    def current_user_id(self):
        return self._get_current_user_id()