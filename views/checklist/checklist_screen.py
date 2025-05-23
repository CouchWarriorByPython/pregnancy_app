from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
                             QScrollArea, QFrame, QCheckBox, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from utils.styles import Styles
from models.data import CHECKLIST_DATA


class CheckItem(QWidget):
    def __init__(self, text, description=None, parent=None):
        super().__init__(parent)
        self._setup_ui(text, description)

    def _setup_ui(self, text, description):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        self.checkbox = QCheckBox()
        self.checkbox.setMinimumSize(30, 30)
        self.checkbox.setStyleSheet(Styles.checkbox_custom(Styles.COLORS['border'], Styles.COLORS['success']))
        self.checkbox.toggled.connect(self._on_checkbox_toggled)
        layout.addWidget(self.checkbox)

        text_layout = QVBoxLayout()
        title = QLabel(text)
        title.setFont(QFont('Arial', 14))
        text_layout.addWidget(title)

        if description:
            desc = QLabel(description)
            desc.setFont(QFont('Arial', 10))
            desc.setStyleSheet(Styles.text_secondary())
            text_layout.addWidget(desc)

        layout.addLayout(text_layout)
        layout.setStretch(1, 1)

    def _on_checkbox_toggled(self, checked):
        parent = self.parent()
        while parent and not isinstance(parent, ChecklistScreen):
            parent = parent.parent()
        if parent:
            parent.update_progress(parent.current_trimester_index)


class ChecklistScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_trimester_index = 0
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._create_header())
        main_layout.addWidget(self._create_trimester_selector())

        self.trimester_stack = QStackedWidget()
        for i in range(1, 4):
            tab = self._create_trimester_tab(i)
            self.trimester_stack.addWidget(tab)

        main_layout.addWidget(self.trimester_stack)
        self.set_trimester(0)

    def _create_header(self):
        header = QWidget()
        header.setMinimumHeight(60)
        header.setStyleSheet(Styles.header())

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)

        checklist_label = QLabel("Чекліст")
        checklist_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        checklist_label.setStyleSheet(Styles.text_accent())
        header_layout.addWidget(checklist_label)

        return header

    def _create_trimester_selector(self):
        trimester_selector = QWidget()
        trimester_selector.setFixedHeight(50)
        trimester_selector.setStyleSheet("background-color: #181818;")

        trimester_layout = QHBoxLayout(trimester_selector)
        trimester_layout.setContentsMargins(0, 0, 0, 0)
        trimester_layout.setSpacing(0)

        self.trimester_buttons = []
        for i in range(1, 4):
            trimester_data = CHECKLIST_DATA[i]
            btn = QPushButton(trimester_data["title"])
            btn.setCheckable(True)
            btn.setFixedHeight(50)
            btn.setStyleSheet(Styles.tab_button())
            btn.clicked.connect(lambda checked, idx=i - 1: self.set_trimester(idx))
            trimester_layout.addWidget(btn)
            self.trimester_buttons.append(btn)

        return trimester_selector

    def _create_trimester_tab(self, trimester_number):
        trimester_data = CHECKLIST_DATA[trimester_number]
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(Styles.scroll_area())

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)

        title_label = QLabel(trimester_data["title"])
        title_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        content_layout.addWidget(title_label)

        content_layout.addWidget(self._create_progress_frame())
        content_layout.addWidget(self._create_checklist_section(trimester_data))

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        return tab

    def _create_progress_frame(self):
        progress_frame = QFrame()
        progress_frame.setStyleSheet(Styles.frame())
        progress_layout = QVBoxLayout(progress_frame)

        progress_title = QLabel("Прогрес:")
        progress_title.setFont(QFont('Arial', 16))
        progress_layout.addWidget(progress_title)

        progress_bar = QLabel()
        progress_bar.setObjectName("progress_bar")
        progress_bar.setMinimumHeight(20)
        progress_bar.setStyleSheet(Styles.progress_bar())
        progress_layout.addWidget(progress_bar)

        progress_text = QLabel("0% виконано")
        progress_text.setObjectName("progress_text")
        progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(progress_text)

        return progress_frame

    def _create_checklist_section(self, trimester_data):
        checklist_section = QFrame()
        checklist_section.setObjectName("checklist_section")
        checklist_section.setStyleSheet(Styles.frame())
        checklist_section.setMaximumWidth(600)

        checklist_layout = QVBoxLayout(checklist_section)

        for section in trimester_data["sections"]:
            section_label = QLabel(section["name"])
            section_label.setStyleSheet(Styles.section_title())
            checklist_layout.addWidget(section_label)

            for text, desc in section["items"]:
                item = CheckItem(text, desc)
                checklist_layout.addWidget(item)

        return checklist_section

    def set_trimester(self, index):
        self.current_trimester_index = index
        for i, btn in enumerate(self.trimester_buttons):
            btn.setChecked(i == index)
        self.trimester_stack.setCurrentIndex(index)
        self.update_progress(index)

    def update_progress(self, tab_index):
        tab = self.trimester_stack.widget(tab_index)
        if not tab:
            return

        checklist_section = tab.findChild(QFrame, "checklist_section")
        if not checklist_section:
            return

        checkboxes = [item.checkbox for item in checklist_section.findChildren(CheckItem)]
        if not checkboxes:
            return

        progress_percent = int((sum(cb.isChecked() for cb in checkboxes) / len(checkboxes)) * 100)

        progress_bar = tab.findChild(QLabel, "progress_bar")
        progress_text = tab.findChild(QLabel, "progress_text")

        if progress_bar and progress_text:
            progress_bar.setStyleSheet(Styles.progress_bar_dynamic(progress_percent))
            progress_text.setText(f"{progress_percent}% виконано")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_progress(self.current_trimester_index)