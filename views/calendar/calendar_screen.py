from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCalendarWidget, QDialog)
from PyQt6.QtGui import QFont
from utils.base_widgets import (HeaderWidget, StyledButton, StyledInput, StyledComboBox, StyledTimeEdit, StyledCard)
from utils.styles import Styles


class EventDialog(QDialog):
    def __init__(self, parent=None, date=None):
        super().__init__(parent)
        self.date = date
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Додати подію")
        self.setFixedSize(350, 280)
        self.setStyleSheet(Styles.dialog_base())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title_label = QLabel(f"Нова подія на {self.date.toString('dd.MM.yyyy')}")
        title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title_label.setStyleSheet(Styles.text_primary())
        layout.addWidget(title_label)

        name_label = QLabel("Назва події:")
        name_label.setStyleSheet(Styles.text_primary())
        layout.addWidget(name_label)

        self.name_edit = StyledInput("Наприклад: Візит до гінеколога")
        layout.addWidget(self.name_edit)

        type_label = QLabel("Тип події:")
        type_label.setStyleSheet(Styles.text_primary())
        layout.addWidget(type_label)

        self.type_combo = StyledComboBox(["Візит до лікаря", "УЗД", "Аналізи", "Особисте"])
        layout.addWidget(self.type_combo)

        time_label = QLabel("Час:")
        time_label.setStyleSheet(Styles.text_primary())
        layout.addWidget(time_label)

        self.time_edit = StyledTimeEdit()
        layout.addWidget(self.time_edit)

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
        self.parent = parent
        self.events = {}
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = HeaderWidget("Календар")
        main_layout.addWidget(header)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet(Styles.calendar())
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.date_clicked)

        content_layout.addWidget(self.calendar)

        add_event_btn = StyledButton("Додати подію")
        add_event_btn.clicked.connect(self.add_event)
        content_layout.addWidget(add_event_btn)

        events_frame = StyledCard("Події на вибраний день:")

        self.events_list = QLabel("Виберіть день, щоб побачити заплановані події")
        self.events_list.setWordWrap(True)
        self.events_list.setStyleSheet(Styles.text_primary())
        events_frame.layout.addWidget(self.events_list)

        content_layout.addWidget(events_frame)
        main_layout.addWidget(content)

    def date_clicked(self, date):
        date_str = date.toString("yyyy-MM-dd")
        if date_str in self.events:
            events_text = ""
            for event in self.events[date_str]:
                events_text += f"• {event['time']} - {event['name']} ({event['type']})\n"
            self.events_list.setText(events_text)
        else:
            self.events_list.setText("На цей день немає запланованих подій")

    def add_event(self):
        selected_date = self.calendar.selectedDate()
        dialog = EventDialog(self, selected_date)

        if dialog.exec():
            date_str = selected_date.toString("yyyy-MM-dd")
            event = {
                "name": dialog.name_edit.text(),
                "type": dialog.type_combo.currentText(),
                "time": dialog.time_edit.time().toString("HH:mm")
            }

            if date_str not in self.events:
                self.events[date_str] = []

            self.events[date_str].append(event)
            self.date_clicked(selected_date)