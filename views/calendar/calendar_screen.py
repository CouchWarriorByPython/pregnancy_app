from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCalendarWidget, QDialog, QCheckBox, QMessageBox, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal
from utils.base_widgets import StyledButton, StyledInput, StyledComboBox, StyledTimeEdit, StyledCard
from styles.calendar import CalendarStyles
from styles.base import BaseStyles, Colors
from controllers.data_controller import DataController
from utils.reminder_service import ReminderService
from utils.logger import get_logger

logger = get_logger('calendar_screen')


class EventDialog(QDialog):
    def __init__(self, parent=None, date=None):
        super().__init__(parent)
        self.date = date
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Додати подію")
        self.setFixedSize(500, 600)
        self.setStyleSheet(CalendarStyles.event_dialog())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel(f"Нова подія на {self.date.toString('dd.MM.yyyy')}")
        title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; margin-bottom: 10px;")
        layout.addWidget(title_label)

        self._add_form_fields(layout)
        self._add_reminder_section(layout)
        self._add_buttons(layout)

    def _add_form_fields(self, layout):
        fields = [
            ("Назва події:", StyledInput("Наприклад: Візит до гінеколога")),
            ("Тип події:", StyledComboBox(["Візит до лікаря", "УЗД", "Аналізи", "Особисте"])),
            ("Час:", StyledTimeEdit())
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 500; margin-top: 10px;")
            layout.addWidget(label)
            layout.addWidget(widget)
            setattr(self, f"{widget.__class__.__name__.lower().replace('styled', '')}_edit", widget)

    def _add_reminder_section(self, layout):
        # Основний контейнер для секції нагадувань
        reminder_container = QWidget()
        reminder_container.setStyleSheet("background: transparent;")
        container_layout = QVBoxLayout(reminder_container)
        container_layout.setContentsMargins(0, 10, 0, 0)
        container_layout.setSpacing(0)

        # Фрейм для нагадувань
        reminder_frame = QFrame()
        reminder_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(139, 92, 246, 0.1), 
                    stop:1 rgba(236, 72, 153, 0.1));
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 16px;
            }}
        """)

        frame_layout = QVBoxLayout(reminder_frame)
        frame_layout.setContentsMargins(20, 15, 20, 15)
        frame_layout.setSpacing(12)

        # Чекбокс
        self.reminder_checkbox = QCheckBox("Додати нагадування")
        self.reminder_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 15px;
                font-weight: 600;
                spacing: 12px;
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 8px;
                border: 2px solid rgba(139, 92, 246, 0.5);
                background: rgba(255, 255, 255, 0.1);
            }}
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #8B5CF6, stop:1 #EC4899);
                border: 2px solid #8B5CF6;
            }}
        """)
        self.reminder_checkbox.toggled.connect(self._toggle_reminder_options)
        frame_layout.addWidget(self.reminder_checkbox)

        # Контейнер для опцій
        self.reminder_options = QWidget()
        self.reminder_options.setVisible(False)
        self.reminder_options.setStyleSheet("background: transparent;")
        options_layout = QVBoxLayout(self.reminder_options)
        options_layout.setContentsMargins(35, 0, 0, 0)
        options_layout.setSpacing(8)

        reminder_label = QLabel("Нагадати за:")
        reminder_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-size: 14px; font-weight: 500;")
        options_layout.addWidget(reminder_label)

        self.reminder_time_combo = StyledComboBox([
            "5 хвилин (для тесту)",
            "15 хвилин",
            "30 хвилин",
            "1 годину",
            "2 години"
        ])
        self.reminder_time_combo.setMinimumHeight(45)
        options_layout.addWidget(self.reminder_time_combo)

        hint_label = QLabel("💡 Нагадування прийде як системне сповіщення")
        hint_label.setStyleSheet(f"color: rgba(255, 255, 255, 0.6); font-size: 12px; margin-top: 5px;")
        hint_label.setWordWrap(True)
        options_layout.addWidget(hint_label)

        frame_layout.addWidget(self.reminder_options)

        container_layout.addWidget(reminder_frame)
        layout.addWidget(reminder_container)

    def _toggle_reminder_options(self, checked):
        self.reminder_options.setVisible(checked)
        if checked:
            self.setFixedSize(500, 650)
        else:
            self.setFixedSize(500, 600)

    def _add_buttons(self, layout):
        layout.addStretch()

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.cancel_btn = StyledButton("Скасувати", "secondary")
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = StyledButton("Зберегти")
        self.save_btn.setMinimumHeight(45)
        self.save_btn.clicked.connect(self.accept)

        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)
        layout.addLayout(buttons_layout)

    def get_event_data(self):
        return {
            'name': self.input_edit.text(),
            'type': self.combobox_edit.currentText(),
            'time': self.timeedit_edit.time(),
            'date': self.date,
            'reminder_enabled': self.reminder_checkbox.isChecked(),
            'reminder_time': self.reminder_time_combo.currentText() if self.reminder_checkbox.isChecked() else None
        }


class CalendarScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self.reminder_service = None
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

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

    def showEvent(self, event):
        super().showEvent(event)
        self._init_services()
        self._load_events()

    def _init_services(self):
        user_id = self._get_current_user_id()
        if user_id:
            self.data_controller = DataController(user_id)
            if hasattr(self.parent, 'reminder_service'):
                self.reminder_service = self.parent.reminder_service

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id'):
            return self.parent.current_user_id
        return None

    def date_clicked(self, date):
        self._show_events_for_date(date)

    def _show_events_for_date(self, date):
        if not self.data_controller:
            return

        date_str = date.toString("yyyy-MM-dd")
        events = self.data_controller.db.get_events_for_date(date_str)

        if events:
            events_text = ""
            for event in events:
                time_str = event.get('time', 'Весь день')

                # Форматуємо час більш зрозуміло
                if time_str != 'Весь день' and 'end_time' in event:
                    time_str = f"{time_str} - {event['end_time']}"

                events_text += f"• {time_str} - {event['title']} ({event['event_type']})\n"

                # Додаємо індикатор нагадування якщо є
                if event.get('description') and 'Нагадування' in event['description']:
                    events_text += "  🔔 З нагадуванням\n"

            self.events_list.setText(events_text.strip())
        else:
            self.events_list.setText("На цей день немає запланованих подій")

    def _load_events(self):
        if self.data_controller:
            today = self.calendar.selectedDate()
            self._show_events_for_date(today)

    def add_event(self):
        if not self.data_controller:
            QMessageBox.warning(self, "Помилка", "Необхідно увійти в систему для додавання подій")
            return

        selected_date = self.calendar.selectedDate()
        dialog = EventDialog(self, selected_date)

        if dialog.exec():
            event_data = dialog.get_event_data()
            self._save_event(event_data)

    def _save_event(self, event_data):
        try:
            date_str = event_data['date'].toString("yyyy-MM-dd")
            time_str = event_data['time'].toString("HH:mm")

            # Зберігаємо подію в календар з часом
            event_id = self.data_controller.db.add_calendar_event(
                title=event_data['name'],
                description=f"Тип: {event_data['type']}",
                start_date=date_str,
                start_time=time_str,  # Передаємо час
                event_type=event_data['type']
            )

            # Якщо ввімкнено нагадування, створюємо його
            if event_data['reminder_enabled'] and self.reminder_service:
                reminder_time = self._calculate_reminder_time(
                    event_data['date'],
                    event_data['time'],
                    event_data['reminder_time']
                )

                if reminder_time:
                    self.reminder_service.add_reminder(
                        title=f"Нагадування: {event_data['name']}",
                        description=f"{event_data['type']} о {time_str}",
                        reminder_date=reminder_time['date'],
                        reminder_time=reminder_time['time'],
                        reminder_type='calendar'
                    )

                    logger.info(
                        f"Створено нагадування для події '{event_data['name']}' на {reminder_time['date']} {reminder_time['time']}")

            self._show_events_for_date(event_data['date'])
            QMessageBox.information(self, "Успіх", "Подію успішно додано")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти подію: {str(e)}")
            logger.error(f"Помилка збереження події: {str(e)}")

    def _calculate_reminder_time(self, event_date, event_time, reminder_offset):
        from datetime import datetime, timedelta

        event_datetime = datetime(
            event_date.year(),
            event_date.month(),
            event_date.day(),
            event_time.hour(),
            event_time.minute()
        )

        offset_map = {
            "5 хвилин (для тесту)": timedelta(minutes=5),
            "15 хвилин": timedelta(minutes=15),
            "30 хвилин": timedelta(minutes=30),
            "1 годину": timedelta(hours=1),
            "2 години": timedelta(hours=2)
        }

        offset = offset_map.get(reminder_offset, timedelta(minutes=15))
        reminder_datetime = event_datetime - offset

        # Для тестування: якщо час нагадування в минулому, встановлюємо його через 1 хвилину
        if reminder_datetime <= datetime.now():
            reminder_datetime = datetime.now() + timedelta(minutes=1)
            logger.info(f"Час нагадування був у минулому, встановлено на {reminder_datetime}")

        return {
            'date': reminder_datetime.strftime('%Y-%m-%d'),
            'time': reminder_datetime.strftime('%H:%M')
        }