from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from utils.styles import Styles
from .profile_editor import ProfileEditor
from .pregnancy_editor import PregnancyEditor
from .child_info_editor import ChildInfoEditor


class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_controller = DataController()
        self._init_editors()
        self._setup_ui()

    def _init_editors(self):
        self.editors = [
            ("Профіль", ProfileEditor()),
            ("Вагітність", PregnancyEditor()),
            ("Дитина", ChildInfoEditor())
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

        self.set_tab(0)

    def _create_header(self):
        header = QWidget()
        header.setMinimumHeight(60)
        header.setStyleSheet(Styles.header())

        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 5, 15, 5)

        label = QLabel("Налаштування")
        label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        label.setStyleSheet(Styles.text_accent())
        layout.addWidget(label)

        return header

    def _create_tab_selector(self):
        tab_selector = QWidget()
        tab_selector.setFixedHeight(50)
        tab_selector.setStyleSheet("background-color: #181818;")

        layout = QHBoxLayout(tab_selector)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_buttons = []
        for i, (name, _) in enumerate(self.editors):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setFixedHeight(50)
            btn.setStyleSheet(Styles.settings_tab_button())
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

    def set_tab(self, index):
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)

        for i, (_, editor) in enumerate(self.editors):
            editor.setVisible(i == index)