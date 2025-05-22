from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QHBoxLayout, QScrollArea, QFrame, QCheckBox, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from utils.styles import Styles


class CheckItem(QWidget):
    def __init__(self, text, description=None, parent=None):
        super().__init__(parent)
        self.setup_ui(text, description)

    def setup_ui(self, text, description):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        self.checkbox = QCheckBox()
        self.checkbox.setMinimumSize(30, 30)
        self.checkbox.setStyleSheet(f"""
            QCheckBox {{
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 25px;
                height: 25px;
                border-radius: 5px;
                border: 2px solid {Styles.COLORS['border']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Styles.COLORS['success']};
                border: 2px solid {Styles.COLORS['success']};
            }}
        """)
        self.checkbox.toggled.connect(self.on_checkbox_toggled)
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

    def on_checkbox_toggled(self, checked):
        parent = self.parent()
        while parent and not isinstance(parent, ChecklistScreen):
            parent = parent.parent()

        if parent and isinstance(parent, ChecklistScreen):
            parent.update_progress(parent.current_trimester_index)


class ChecklistScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_trimester_index = 0
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QWidget()
        header.setMinimumHeight(60)
        header.setStyleSheet(Styles.header())

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)

        checklist_label = QLabel("Чекліст")
        checklist_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        checklist_label.setStyleSheet(Styles.text_accent())

        header_layout.addWidget(checklist_label)
        main_layout.addWidget(header)

        trimester_selector = QWidget()
        trimester_selector.setFixedHeight(50)
        trimester_selector.setStyleSheet("background-color: #181818;")

        trimester_layout = QHBoxLayout(trimester_selector)
        trimester_layout.setContentsMargins(0, 0, 0, 0)
        trimester_layout.setSpacing(0)

        self.trimester_buttons = []
        for i, name in enumerate(["I Триместр", "II Триместр", "III Триместр"]):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setFixedHeight(50)
            btn.setStyleSheet(Styles.tab_button())
            btn.clicked.connect(lambda checked, idx=i: self.set_trimester(idx))
            trimester_layout.addWidget(btn)
            self.trimester_buttons.append(btn)

        main_layout.addWidget(trimester_selector)

        self.trimester_stack = QStackedWidget()

        first_tab = self.create_trimester_tab("I Триместр")
        first_tab.setObjectName("trimester_tab_1")
        second_tab = self.create_trimester_tab("II Триместр")
        second_tab.setObjectName("trimester_tab_2")
        third_tab = self.create_trimester_tab("III Триместр")
        third_tab.setObjectName("trimester_tab_3")

        self.add_first_trimester_items(first_tab)
        self.add_second_trimester_items(second_tab)
        self.add_third_trimester_items(third_tab)

        self.trimester_stack.addWidget(first_tab)
        self.trimester_stack.addWidget(second_tab)
        self.trimester_stack.addWidget(third_tab)

        main_layout.addWidget(self.trimester_stack)
        self.set_trimester(0)

    def set_trimester(self, index):
        self.current_trimester_index = index

        for i, btn in enumerate(self.trimester_buttons):
            btn.setChecked(i == index)

        self.trimester_stack.setCurrentIndex(index)
        self.update_progress(index)

    def create_trimester_tab(self, title):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(Styles.scroll_area())

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(15)

        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        self.content_layout.addWidget(title_label)

        progress_frame = QFrame()
        progress_frame.setStyleSheet(Styles.frame())
        progress_layout = QVBoxLayout(progress_frame)

        progress_title = QLabel("Прогрес:")
        progress_title.setFont(QFont('Arial', 16))

        self.progress_bar = QLabel()
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setStyleSheet(Styles.progress_bar())

        self.progress_text = QLabel("0% виконано")
        self.progress_text.setObjectName("progress_text")
        self.progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        progress_layout.addWidget(progress_title)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_text)

        self.content_layout.addWidget(progress_frame)

        self.checklist_section = QFrame()
        self.checklist_section.setObjectName("checklist_section")
        self.checklist_section.setStyleSheet(Styles.frame())
        self.checklist_section.setMaximumWidth(600)

        self.checklist_layout = QVBoxLayout(self.checklist_section)

        self.content_layout.addWidget(self.checklist_section)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        return tab

    def add_first_trimester_items(self, tab):
        checklist_layout = tab.findChild(QFrame, "checklist_section").layout()

        analyses_label = QLabel("Аналізи")
        analyses_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(analyses_label)

        items = [
            ("Загальний аналіз крові", "До 12 тижнів"),
            ("Аналіз крові на групу та резус-фактор", "До 12 тижнів"),
            ("Аналіз крові на ВІЛ", "До 12 тижнів"),
            ("Аналіз крові на сифіліс", "До 12 тижнів"),
            ("Загальний аналіз сечі", "До 12 тижнів"),
            ("Аналіз на TORCH-інфекції", "До 12 тижнів"),
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

        ultrasound_label = QLabel("УЗД")
        ultrasound_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(ultrasound_label)

        items = [
            ("Перше скринінгове УЗД", "11-13 тижнів")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

        consult_label = QLabel("Консультації")
        consult_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(consult_label)

        items = [
            ("Гінеколог", "Перший візит до 12 тижнів"),
            ("Терапевт", "До 12 тижнів"),
            ("Стоматолог", "До 12 тижнів")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

    def add_second_trimester_items(self, tab):
        checklist_layout = tab.findChild(QFrame, "checklist_section").layout()
        tab.findChild(QFrame, "checklist_section").setMaximumWidth(600)

        analyses_label = QLabel("Аналізи")
        analyses_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(analyses_label)

        items = [
            ("Загальний аналіз крові", "16-20 тижнів"),
            ("Загальний аналіз сечі", "16-20 тижнів"),
            ("Глюкозотолерантний тест", "24-28 тижнів"),
            ("Аналіз крові на RW", "20-22 тижні"),
            ("Аналіз на групу крові", "16-18 тижнів"),
            ("Аналіз на резус-фактор", "16-18 тижнів"),
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

        ultrasound_label = QLabel("УЗД")
        ultrasound_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(ultrasound_label)

        items = [
            ("Друге скринінгове УЗД", "18-22 тижнів"),
            ("Доплер-УЗД", "20-24 тижні")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

        consult_label = QLabel("Консультації")
        consult_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(consult_label)

        items = [
            ("Гінеколог", "Кожні 4 тижні"),
            ("Окуліст", "До 20 тижнів"),
            ("Ендокринолог", "18-22 тижні"),
            ("Терапевт", "20-24 тижні")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

        other_label = QLabel("Інше")
        other_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(other_label)

        items = [
            ("Придбати одяг для вагітних", "16-20 тижнів"),
            ("Вибрати пологовий будинок", "18-24 тижні"),
            ("Записатись на курси для вагітних", "20-24 тижні")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

    def add_third_trimester_items(self, tab):
        checklist_layout = tab.findChild(QFrame, "checklist_section").layout()

        analyses_label = QLabel("Аналізи")
        analyses_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(analyses_label)

        items = [
            ("Загальний аналіз крові", "30 тижнів"),
            ("Загальний аналіз сечі", "30-32 тижнів"),
            ("Аналіз крові на ВІЛ", "30 тижнів"),
            ("Аналіз крові на сифіліс", "30 тижнів"),
            ("Мазок на флору", "30 тижнів")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

        ultrasound_label = QLabel("УЗД")
        ultrasound_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(ultrasound_label)

        items = [
            ("Третє скринінгове УЗД", "32-34 тижнів"),
            ("Доплерометрія", "34-36 тижнів")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

        consult_label = QLabel("Консультації")
        consult_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(consult_label)

        items = [
            ("Гінеколог", "Кожні 2 тижні до 36 тижня, потім щотижня"),
            ("Консультація анестезіолога", "За 2-3 тижні до пологів")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

    def update_progress(self, tab_index):
        tab = self.trimester_stack.widget(tab_index)
        if not tab:
            return

        checklist_section = tab.findChild(QFrame, "checklist_section")
        if not checklist_section:
            return

        checkboxes = []
        for item in checklist_section.findChildren(CheckItem):
            checkboxes.append(item.checkbox)

        total = len(checkboxes)
        if total == 0:
            return

        checked = sum(1 for cb in checkboxes if cb.isChecked())
        progress_percent = int((checked / total) * 100)

        progress_bar = tab.findChild(QLabel, "progress_bar")
        progress_text = tab.findChild(QLabel, "progress_text")

        if progress_bar and progress_text:
            progress_bar.setStyleSheet(f"""
                background-color: {Styles.COLORS['surface_variant']};
                border-radius: 10px;
                padding: 0px;
                text-align: left;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 {Styles.COLORS['primary']}, stop:{progress_percent / 100} {Styles.COLORS['primary']},
                                          stop:{progress_percent / 100} {Styles.COLORS['surface_variant']}, stop:1 {Styles.COLORS['surface_variant']});
            """)

            progress_text.setText(f"{progress_percent}% виконано")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_progress(self.current_trimester_index)