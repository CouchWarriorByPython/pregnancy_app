from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                            QHBoxLayout, QScrollArea, QFrame, QCheckBox, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class CheckItem(QWidget):
    """Елемент чекліста з прапорцем та текстом"""

    def __init__(self, text, description=None, parent=None):
        super().__init__(parent)
        self.setup_ui(text, description)

    def setup_ui(self, text, description):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        # Чекбокс
        self.checkbox = QCheckBox()
        self.checkbox.setMinimumSize(30, 30)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 25px;
                height: 25px;
                border-radius: 5px;
                border: 2px solid #555555;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
            }
        """)
        # Підключаємо сигнал toggled для оновлення прогресу при зміні стану чекбоксу
        self.checkbox.toggled.connect(self.on_checkbox_toggled)
        layout.addWidget(self.checkbox)

        # Текстова інформація
        text_layout = QVBoxLayout()

        # Основний текст
        title = QLabel(text)
        title.setFont(QFont('Arial', 14))
        text_layout.addWidget(title)

        # Опис (якщо заданий)
        if description:
            desc = QLabel(description)
            desc.setFont(QFont('Arial', 10))
            desc.setStyleSheet("color: #AAAAAA;")
            text_layout.addWidget(desc)

        layout.addLayout(text_layout)
        layout.setStretch(1, 1)  # Розтягуємо текст на всю доступну ширину

    def on_checkbox_toggled(self, checked):
        """Обробка зміни стану чекбоксу"""
        # Знаходимо батьківський екран чекліста
        parent = self.parent()
        while parent and not isinstance(parent, ChecklistScreen):
            parent = parent.parent()

        # Оновлюємо прогрес, якщо знайшли батьківський екран
        if parent and isinstance(parent, ChecklistScreen):
            parent.update_progress(parent.tab_widget.currentIndex())


class ChecklistScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
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

        checklist_label = QLabel("Чекліст")
        checklist_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        checklist_label.setStyleSheet("color: #FF8C00;")

        header_layout.addWidget(checklist_label)
        main_layout.addWidget(header)

        # Табвіджет для різних категорій чекліста
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar {
                background-color: #121212;
            }
            QTabBar::tab {
                background-color: #121212;
                color: #AAAAAA;
                padding: 12px 0px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                min-width: 0px;
                width: 33.3%;
                border: none;
                margin: 0px;
            }
            QTabBar::tab:selected {
                background-color: #222222;
                color: #FF8C00;
            }
            QTabBar::tab:hover:!selected {
                background-color: #1A1A1A;
            }
        """)

        # Створюємо вкладки для кожного триместру
        first_tab = self.create_trimester_tab("I Триместр")
        first_tab.setObjectName("trimester_tab_1")
        second_tab = self.create_trimester_tab("II Триместр")
        second_tab.setObjectName("trimester_tab_2")
        third_tab = self.create_trimester_tab("III Триместр")
        third_tab.setObjectName("trimester_tab_3")

        # Додаємо елементи чекліста для першого триместру
        self.add_first_trimester_items(first_tab)

        # Додаємо елементи чекліста для другого триместру
        self.add_second_trimester_items(second_tab)

        # Додаємо елементи чекліста для третього триместру
        self.add_third_trimester_items(third_tab)

        # Додаємо вкладки до табвіджету
        self.tab_widget.addTab(first_tab, "I Триместр")
        self.tab_widget.addTab(second_tab, "II Триместр")
        self.tab_widget.addTab(third_tab, "III Триместр")

        # Встановлюємо однакову ширину для всіх вкладок
        self.tab_widget.tabBar().setExpanding(True)

        # Підключаємо обробку чекбоксів
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        main_layout.addWidget(self.tab_widget)

        # Оновлюємо прогрес для першого триместру
        self.update_progress(0)

    def create_trimester_tab(self, title):
        """Створює вкладку для триместру з прокруткою та контентом"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(15)

        # Заголовок
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        self.content_layout.addWidget(title_label)

        # Прогрес
        progress_frame = QFrame()
        progress_frame.setStyleSheet("background-color: #121212; border-radius: 15px;")
        progress_layout = QVBoxLayout(progress_frame)

        progress_title = QLabel("Прогрес:")
        progress_title.setFont(QFont('Arial', 16))

        # ВАЖЛИВО: Додаємо objectName для progress_bar та progress_text
        self.progress_bar = QLabel()
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setStyleSheet("background-color: #333333; border-radius: 10px;")

        self.progress_text = QLabel("0% виконано")
        self.progress_text.setObjectName("progress_text")
        self.progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        progress_layout.addWidget(progress_title)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_text)

        self.content_layout.addWidget(progress_frame)

        # Секція з чекбоксами
        self.checklist_section = QFrame()
        self.checklist_section.setObjectName("checklist_section")
        self.checklist_section.setStyleSheet("background-color: #121212; border-radius: 15px;")

        # Встановлюємо фіксовану ширину секції для уніфікації вигляду між триместрами
        self.checklist_section.setMaximumWidth(600)

        self.checklist_layout = QVBoxLayout(self.checklist_section)

        self.content_layout.addWidget(self.checklist_section)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        return tab

    def add_first_trimester_items(self, tab):
        """Додає елементи чекліста для першого триместру"""
        checklist_layout = tab.findChild(QFrame, "checklist_section").layout()

        # Аналізи
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

        # УЗД
        ultrasound_label = QLabel("УЗД")
        ultrasound_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        checklist_layout.addWidget(ultrasound_label)

        items = [
            ("Перше скринінгове УЗД", "11-13 тижнів")
        ]

        for text, desc in items:
            item = CheckItem(text, desc)
            checklist_layout.addWidget(item)

        # Консультації
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
        """Додає елементи чекліста для другого триместру"""
        checklist_layout = tab.findChild(QFrame, "checklist_section").layout()

        # Змінюємо ширину блоку
        tab.findChild(QFrame, "checklist_section").setMaximumWidth(600)

        # Аналізи
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

        # УЗД
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

        # Консультації
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

        # Інше
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
        """Додає елементи чекліста для третього триместру"""
        checklist_layout = tab.findChild(QFrame, "checklist_section").layout()

        # Аналізи
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

        # УЗД
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

        # Консультації
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
        """Оновлює стан прогрес-бару на основі відмічених пунктів"""
        tab = self.tab_widget.widget(tab_index)
        if not tab:
            return

        checklist_section = tab.findChild(QFrame, "checklist_section")
        if not checklist_section:
            return

        # Знаходимо всі чекбокси у цьому розділі
        checkboxes = []
        for item in checklist_section.findChildren(CheckItem):
            checkboxes.append(item.checkbox)

        # Рахуємо прогрес
        total = len(checkboxes)
        if total == 0:
            return

        checked = sum(1 for cb in checkboxes if cb.isChecked())
        progress_percent = int((checked / total) * 100)

        # Знаходимо прогрес-бар
        # ВАЖЛИВО: Оновлюємо пошук прогрес-бару та тексту
        progress_bar = tab.findChild(QLabel, "progress_bar")
        progress_text = tab.findChild(QLabel, "progress_text")

        if progress_bar and progress_text:
            # Встановлюємо стиль для прогрес-бару з фіксованими розмірами
            progress_bar.setStyleSheet(f"""
                background-color: #333333;
                border-radius: 10px;
                padding: 0px;
                text-align: left;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #FF8C00, stop:{progress_percent / 100} #FF8C00,
                                          stop:{progress_percent / 100} #333333, stop:1 #333333);
            """)

            progress_text.setText(f"{progress_percent}% виконано")

    def on_tab_changed(self, index):
        """Оновлює прогрес при зміні вкладки"""
        self.update_progress(index)

    def resizeEvent(self, event):
        """Обробка зміни розміру вікна для коректного відображення прогрес-бару"""
        super().resizeEvent(event)
        current_index = self.tab_widget.currentIndex()
        self.update_progress(current_index)