from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCalendarWidget, QDialog, QCheckBox, QMessageBox, \
    QFrame
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.base_widgets import StyledButton, StyledInput, StyledComboBox, StyledTimeEdit, StyledCard
from styles import CalendarScreenStyles, BaseStyles, Colors, OnboardingScreenStyles
from utils.logger import get_logger
from utils.user_mixin import UserMixin

logger = get_logger('calendar_screen')


class EventDialog(QDialog):
    def __init__(self, parent=None, date=None):
        super().__init__(parent)
        self.date = date
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Додати подію")
        self.setFixedSize(500, 600)
        self.setStyleSheet(CalendarScreenStyles.event_dialog())

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)

        title_label = QLabel(f"Нова подія на {self.date.toString('dd.MM.yyyy')}")
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title_label.setStyleSheet(CalendarScreenStyles.event_dialog_title())
        layout.addWidget(title_label)

        self._add_form_fields(layout)
        self._add_reminder_section(layout)
        self._add_buttons(layout)

    def _add_form_fields(self, layout):
        # Назва події
        name_label = QLabel("Назва події:")
        name_label.setStyleSheet(OnboardingScreenStyles.user_info_field_label())
        layout.addWidget(name_label)
        
        self.input_edit = StyledInput("Наприклад: Візит до гінеколога")
        self.input_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        layout.addWidget(self.input_edit)

        # Тип події
        type_label = QLabel("Тип події:")
        type_label.setStyleSheet(OnboardingScreenStyles.user_info_field_label())
        layout.addWidget(type_label)
        
        self.combobox_edit = StyledComboBox(["Візит до лікаря", "УЗД", "Аналізи", "Особисте"])
        self.combobox_edit.setStyleSheet(OnboardingScreenStyles.elegant_input() + f"""
            QComboBox QAbstractItemView {{
                background: {Colors.SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 12px;
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.PRIMARY};
                padding: 8px;
            }}
        """)
        layout.addWidget(self.combobox_edit)

        # Час
        time_label = QLabel("Час:")
        time_label.setStyleSheet(OnboardingScreenStyles.user_info_field_label())
        layout.addWidget(time_label)
        
        self.timeedit_edit = StyledInput("00:00")
        self.timeedit_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.timeedit_edit.setPlaceholderText("Формат: ГГ:ХХ (наприклад, 14:30)")
        layout.addWidget(self.timeedit_edit)

    def _add_reminder_section(self, layout):
        reminder_container = QWidget()
        reminder_container.setStyleSheet("background: transparent;")
        container_layout = QVBoxLayout(reminder_container)
        container_layout.setContentsMargins(0, 15, 0, 0)
        container_layout.setSpacing(0)

        reminder_frame = QFrame()
        reminder_frame.setStyleSheet(CalendarScreenStyles.event_dialog_reminder_frame())

        frame_layout = QVBoxLayout(reminder_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(15)

        self.reminder_checkbox = QCheckBox("Додати нагадування")
        self.reminder_checkbox.setStyleSheet(CalendarScreenStyles.event_dialog_reminder_checkbox())
        self.reminder_checkbox.toggled.connect(self._toggle_reminder_options)
        frame_layout.addWidget(self.reminder_checkbox)

        self.reminder_options = QWidget()
        self.reminder_options.setVisible(False)
        self.reminder_options.setStyleSheet("background: transparent;")
        options_layout = QVBoxLayout(self.reminder_options)
        options_layout.setContentsMargins(0, 10, 0, 0)
        options_layout.setSpacing(10)

        reminder_label = QLabel("Нагадати за:")
        reminder_label.setStyleSheet(OnboardingScreenStyles.user_info_field_label())
        options_layout.addWidget(reminder_label)

        self.reminder_time_combo = StyledComboBox([
            "5 хвилин (для тесту)",
            "15 хвилин",
            "30 хвилин",
            "1 годину",
            "2 години"
        ])
        self.reminder_time_combo.setStyleSheet(OnboardingScreenStyles.elegant_input() + f"""
            QComboBox QAbstractItemView {{
                background: {Colors.SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 12px;
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.PRIMARY};
                padding: 8px;
            }}
        """)
        options_layout.addWidget(self.reminder_time_combo)

        hint_label = QLabel("💡 Нагадування прийде як системне сповіщення")
        hint_label.setStyleSheet(CalendarScreenStyles.event_dialog_hint_label())
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
        buttons_layout.setSpacing(15)

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
        # Парсимо час з текстового поля
        time_text = self.timeedit_edit.text().strip()
        if not time_text or time_text == "00:00":
            from PyQt6.QtCore import QTime
            time_obj = QTime(0, 0)
        else:
            try:
                from PyQt6.QtCore import QTime
                parts = time_text.split(':')
                if len(parts) == 2:
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    if 0 <= hours <= 23 and 0 <= minutes <= 59:
                        time_obj = QTime(hours, minutes)
                    else:
                        time_obj = QTime(0, 0)
                else:
                    time_obj = QTime(0, 0)
            except (ValueError, IndexError):
                time_obj = QTime(0, 0)
        
        return {
            'name': self.input_edit.text(),
            'type': self.combobox_edit.currentText(),
            'time': time_obj,
            'date': self.date,
            'reminder_enabled': self.reminder_checkbox.isChecked(),
            'reminder_time': self.reminder_time_combo.currentText() if self.reminder_checkbox.isChecked() else None
        }


class CalendarScreen(QWidget, UserMixin):
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
        self.calendar.setStyleSheet(CalendarScreenStyles.calendar_widget())
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.date_clicked)
        content_layout.addWidget(self.calendar)

        add_event_btn = StyledButton("Додати подію")
        add_event_btn.clicked.connect(self.add_event)
        content_layout.addWidget(add_event_btn)

        events_frame = StyledCard("Події на вибраний день:")
        events_frame.setStyleSheet(CalendarScreenStyles.events_card())
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
        """Ініціалізує сервіси при показі екрану"""
        if self.init_data_controller():
            logger.info(f"CalendarScreen ініціалізований з user_id: {self.get_current_user_id()}")

            # Отримуємо reminder_service з MainWindow
            main_window = self._find_main_window()
            if main_window and hasattr(main_window, 'reminder_service'):
                self.reminder_service = main_window.reminder_service
        else:
            logger.warning("CalendarScreen: не вдалося ініціалізувати DataController")

    def date_clicked(self, date):
        self._show_events_for_date(date)

    def _show_events_for_date(self, date):
        """Показує події для вибраної дати"""
        if not self.is_user_authenticated():
            self.events_list.setText("Необхідно увійти в систему для перегляду подій")
            return

        user_id = self.get_current_user_id()

        try:
            date_str = date.toString("yyyy-MM-dd")
            events = self.data_controller.db.get_events_for_date(date_str, user_id)

            if events:
                events_text = ""
                for event in events:
                    time_str = event.get('time', 'Весь день')

                    if time_str != 'Весь день' and 'end_time' in event:
                        time_str = f"{time_str} - {event['end_time']}"

                    events_text += f"• {time_str} - {event['title']} ({event['event_type']})\n"

                    if event.get('description') and 'Нагадування' in event['description']:
                        events_text += "  🔔 З нагадуванням\n"

                self.events_list.setText(events_text.strip())
            else:
                self.events_list.setText("На цей день немає запланованих подій")

        except Exception as e:
            logger.error(f"Помилка при завантаженні подій: {str(e)}")
            self.events_list.setText("Помилка при завантаженні подій")

    def _load_events(self):
        if self.data_controller:
            today = self.calendar.selectedDate()
            self._show_events_for_date(today)

    def add_event(self):
        if not self.is_user_authenticated():
            show_warning(self, "Помилка", "Необхідно увійти в систему для додавання подій")
            return

        selected_date = self.calendar.selectedDate()
        dialog = EventDialog(self, selected_date)

        if dialog.exec():
            event_data = dialog.get_event_data()
            self._save_event(event_data)

    def _save_event(self, event_data):
        user_id = self.get_current_user_id()
        if not user_id:
            show_warning(self, "Помилка", "Помилка авторизації")
            return

        try:
            date_str = event_data['date'].toString("yyyy-MM-dd")
            time_str = event_data['time'].toString("HH:mm")

            # Зберігаємо подію
            event_id = self.data_controller.db.add_calendar_event(
                title=event_data['name'],
                description=f"Тип: {event_data['type']}",
                start_date=date_str,
                start_time=time_str,
                event_type=event_data['type'],
                user_id=user_id
            )

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
            show_info(self, "Успіх", "Подію успішно додано")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося зберегти подію: {str(e)}")
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

        if reminder_datetime <= datetime.now():
            reminder_datetime = datetime.now() + timedelta(minutes=1)
            logger.info(f"Час нагадування був у минулому, встановлено на {reminder_datetime}")

        return {
            'date': reminder_datetime.strftime('%Y-%m-%d'),
            'time': reminder_datetime.strftime('%H:%M')
        }