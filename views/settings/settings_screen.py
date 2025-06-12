from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from controllers.data_controller import DataController
from styles import SettingsScreenStyles
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
        user_id = self._get_current_user_id()
        if user_id:
            self.data_controller = DataController(user_id)
        else:
            self.data_controller = DataController()

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id') and self.parent.current_user_id:
            return self.parent.current_user_id

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
        header.setMinimumHeight(70)
        header.setStyleSheet(SettingsScreenStyles.main_header())

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)

        title_label = QLabel("⚙️ Налаштування")
        title_label.setFont(QFont('Segoe UI', 20, QFont.Weight.Bold))
        title_label.setStyleSheet(SettingsScreenStyles.header_title())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        return header

    def _create_tab_selector(self):
        tab_selector = QWidget()
        tab_selector.setFixedHeight(80)
        tab_selector.setStyleSheet(SettingsScreenStyles.tab_selector())

        layout = QHBoxLayout(tab_selector)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        self.tab_buttons = []
        tab_icons = ["👤", "🤰", "👶", "🔐"]

        for i, (name, _) in enumerate(self.editors):
            btn = QPushButton(f"{tab_icons[i]} {name}")
            btn.setCheckable(True)
            btn.setFixedHeight(64)
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
        logout_section.setMinimumHeight(90)
        logout_section.setStyleSheet(SettingsScreenStyles.logout_section())

        layout = QVBoxLayout(logout_section)
        layout.setContentsMargins(24, 16, 24, 16)

        logout_btn = QPushButton("🚪 Вийти з акаунту")
        logout_btn.setMinimumHeight(58)
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