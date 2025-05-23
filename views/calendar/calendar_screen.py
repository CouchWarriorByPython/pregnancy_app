from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCalendarWidget, QDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.base_widgets import HeaderWidget, StyledButton, StyledInput, StyledComboBox, StyledTimeEdit, StyledCard
from styles.calendar import CalendarStyles
from styles.base import BaseStyles


class EventDialog(QDialog):
    def __init__(self, parent=None, date=None):
        super().__init__(parent)
        self.date = date
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Додати подію")
        # Збільшуємо розмір діалогового вікна
        self.setFixedSize(450, 380)
        self.setStyleSheet(CalendarStyles.event_dialog())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title_label = QLabel(f"Нова подія на {self.date.toString('dd.MM.yyyy')}")
        title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title_label.setStyleSheet(BaseStyles.text_primary())
        layout.addWidget(title_label)

        self._add_form_fields(layout)
        self._add_buttons(layout)

    def _add_form_fields(self, layout):
        fields = [
            ("Назва події:", StyledInput("Наприклад: Візит до гінеколога")),
            ("Тип події:", StyledComboBox(["Візит до лікаря", "УЗД", "Аналізи", "Особисте"])),
            ("Час:", StyledTimeEdit())
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet(BaseStyles.text_primary())
            layout.addWidget(label)
            layout.addWidget(widget)
            setattr(self, f"{widget.__class__.__name__.lower().replace('styled', '')}_edit", widget)

    def _add_buttons(self, layout):
        buttons_layout = QHBoxLayout()

        self.cancel_btn = StyledButton("Скасувати", "secondary")
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = StyledButton("Зберегти")
        self.save_btn.clicked.connect(self.accept)

        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)
        layout.addLayout(buttons_layout)


class CalendarScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.events = {}
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Змінюємо заголовок на власний з центруванням
        header = QWidget()
        header.setMinimumHeight(60)
        header.setStyleSheet(BaseStyles.header())

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)

        title_label = QLabel("Календар")
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title_label.setStyleSheet(BaseStyles.text_accent())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(title_label)
        main_layout.addWidget(header)

        main_layout.addWidget(self._create_content())

    def _create_content(self):
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet(CalendarStyles.calendar_widget())
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.date_clicked)
        content_layout.addWidget(self.calendar)

        add_event_btn = StyledButton("Додати подію")
        add_event_btn.clicked.connect(self.add_event)
        content_layout.addWidget(add_event_btn)

        events_frame = StyledCard("Події на вибраний день:")
        events_frame.setStyleSheet(CalendarStyles.events_card())
        self.events_list = QLabel("Виберіть день, щоб побачити заплановані події")
        self.events_list.setWordWrap(True)
        self.events_list.setStyleSheet(BaseStyles.text_primary())
        events_frame.layout.addWidget(self.events_list)
        content_layout.addWidget(events_frame)

        return content

    def date_clicked(self, date):
        date_str = date.toString("yyyy-MM-dd")
        if date_str in self.events:
            events_text = "".join(f"• {event['time']} - {event['name']} ({event['type']})\n"
                                  for event in self.events[date_str])
            self.events_list.setText(events_text)
        else:
            self.events_list.setText("На цей день немає запланованих подій")

    def add_event(self):
        selected_date = self.calendar.selectedDate()
        dialog = EventDialog(self, selected_date)

        if dialog.exec():
            date_str = selected_date.toString("yyyy-MM-dd")
            event = {
                "name": dialog.input_edit.text(),
                "type": dialog.combobox_edit.currentText(),
                "time": dialog.timeedit_edit.time().toString("HH:mm")
            }

            if date_str not in self.events:
                self.events[date_str] = []

            self.events[date_str].append(event)
            self.date_clicked(selected_date)