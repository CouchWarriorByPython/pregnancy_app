from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                          QPushButton, QHBoxLayout, QFrame, QCalendarWidget,
                          QComboBox, QDialog, QLineEdit, QTimeEdit)
from PyQt6.QtGui import QFont

class EventDialog(QDialog):
    def __init__(self, parent=None, date=None):
        super().__init__(parent)
        self.date = date
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Додати подію")
        self.setFixedSize(350, 280)
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QLineEdit, QComboBox, QTimeEdit {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px;
                min-height: 30px;
            }
            QPushButton {
                background-color: #FF8C00;
                color: white;
                border-radius: 10px;
                min-height: 35px;
                font-weight: bold;
            }
            QPushButton#cancelBtn {
                background-color: transparent;
                border: 1px solid #FF8C00;
                color: #FF8C00;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Заголовок діалогу
        title_label = QLabel(f"Нова подія на {self.date.toString('dd.MM.yyyy')}")
        title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # Назва події
        name_label = QLabel("Назва події:")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Наприклад: Візит до гінеколога")
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        
        # Тип події
        type_label = QLabel("Тип події:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Візит до лікаря", "УЗД", "Аналізи", "Особисте"])
        layout.addWidget(type_label)
        layout.addWidget(self.type_combo)
        
        # Час події
        time_label = QLabel("Час:")
        self.time_edit = QTimeEdit()
        layout.addWidget(time_label)
        layout.addWidget(self.time_edit)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Скасувати")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Зберегти")
        self.save_btn.clicked.connect(self.accept)
        
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)
        
        layout.addLayout(buttons_layout)

class CalendarScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.events = {}  # Словник для зберігання подій {дата_str: [список_подій]}
        
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
        
        calendar_label = QLabel("Календар")
        calendar_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        calendar_label.setStyleSheet("color: #FF8C00;")
        
        header_layout.addWidget(calendar_label)
        main_layout.addWidget(header)
        
        # Контент сторінки
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Календар
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #121212;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: #333333;
                border-radius: 5px;
            }
            QCalendarWidget QMenu {
                background-color: #333333;
                color: white;
            }
            QCalendarWidget QSpinBox {
                background-color: #333333;
                color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: white;
                background-color: #121212;
                selection-background-color: #FF8C00;
                selection-color: white;
            }
        """)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.date_clicked)
        
        content_layout.addWidget(self.calendar)
        
        # Кнопка для додавання події
        add_event_btn = QPushButton("Додати подію")
        add_event_btn.setMinimumHeight(50)
        add_event_btn.clicked.connect(self.add_event)
        content_layout.addWidget(add_event_btn)
        
        # Рамка для відображення подій на вибраний день
        events_frame = QFrame()
        events_frame.setStyleSheet("background-color: #121212; border-radius: 15px;")
        events_layout = QVBoxLayout(events_frame)
        
        events_title = QLabel("Події на вибраний день:")
        events_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        events_layout.addWidget(events_title)
        
        self.events_list = QLabel("Виберіть день, щоб побачити заплановані події")
        self.events_list.setWordWrap(True)
        events_layout.addWidget(self.events_list)
        
        content_layout.addWidget(events_frame)
        
        main_layout.addWidget(content)
    
    def date_clicked(self, date):
        """Обробка кліку на дату в календарі"""
        date_str = date.toString("yyyy-MM-dd")
        if date_str in self.events:
            events_text = ""
            for event in self.events[date_str]:
                events_text += f"• {event['time']} - {event['name']} ({event['type']})\n"
            self.events_list.setText(events_text)
        else:
            self.events_list.setText("На цей день немає запланованих подій")
    
    def add_event(self):
        """Додати нову подію"""
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
            self.date_clicked(selected_date)  # Оновити відображення подій
            print(f"Додано подію: {event['name']} на {date_str} о {event['time']}") 