import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QTimeEdit, QSpinBox, QHBoxLayout, QListWidget,
                             QMessageBox, QFrame, QSlider, QTabWidget, QGridLayout, QProgressBar, QFormLayout, QAbstractSpinBox, QScrollArea)
from PyQt6.QtCore import Qt, QDate, QTime, QTimer
from PyQt6.QtGui import QFont
from utils.logger import get_logger
from utils.message_utils import show_info, show_warning, show_error
from styles import ContractionCounterStyles, SliderStyles, OnboardingScreenStyles
from styles.base import BaseStyles
from utils.user_mixin import UserMixin
from utils.base_widgets import TitleLabel, StyledButton, StyledDateEdit, StyledInput, StyledSpinBox

logger = get_logger('contraction_counter')


class ContractionCounterScreen(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.start_time = None
        self.current_seconds = 0
        self.is_timing = False

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 8, 15, 8)
        main_layout.setSpacing(8)

        # Компактний заголовок
        title = TitleLabel("Лічильник переймів", 16)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Відстежуйте тривалість та інтенсивність переймів")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Основний горизонтальний контейнер з двома колонками
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(20)
        
        # Ліва колонка - Фіксація переймів
        left_column = QVBoxLayout()
        left_column.setSpacing(8)
        
        # Інформація (коротша)
        info_title = QLabel("⏱️ Як користуватися")
        info_title.setStyleSheet("color: white; font-weight: 700; font-size: 14px; background: transparent; border: none;")
        left_column.addWidget(info_title)

        info_text = """• "Почати" → початок перейми  • "Стоп" → кінець
• Оцініть інтенсивність 1-10  • Збережіть результат"""

        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 12px; background: transparent; border: none;")
        info_label.setWordWrap(True)
        left_column.addWidget(info_label)

        # Таймер
        timer_title = QLabel("⏰ Поточна перейма")
        timer_title.setStyleSheet("color: white; font-weight: 700; font-size: 14px; background: transparent; border: none; margin-top: 6px;")
        left_column.addWidget(timer_title)

        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet("color: white; font-size: 36px; font-weight: 700; background: transparent; border: none; text-align: center;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_column.addWidget(self.timer_label)

        # Прогрес бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 180)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximumHeight(6)
        self.progress_bar.setStyleSheet(ContractionCounterStyles.progress_bar())
        left_column.addWidget(self.progress_bar)

        # Кнопки управління (компактні)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.start_btn = StyledButton("▶️ Почати")
        self.start_btn.setMinimumHeight(36)
        self.start_btn.clicked.connect(self.start_contraction)

        self.stop_btn = StyledButton("⏹️ Стоп")
        self.stop_btn.setMinimumHeight(36)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_contraction)

        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.stop_btn)
        left_column.addLayout(buttons_layout)

        # Інтенсивність (компактна)
        intensity_layout = QHBoxLayout()
        intensity_layout.setSpacing(8)
        intensity_label = QLabel("💪")
        intensity_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")

        self.intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.intensity_slider.setRange(1, 10)
        self.intensity_slider.setValue(5)
        self.intensity_slider.setMaximumHeight(20)
        self.intensity_slider.setStyleSheet(SliderStyles.horizontal_slider())

        self.intensity_value = QLabel("5")
        self.intensity_value.setStyleSheet("color: white; font-weight: 600; font-size: 14px; background: transparent; border: none;")
        self.intensity_slider.valueChanged.connect(lambda v: self.intensity_value.setText(str(v)))

        intensity_layout.addWidget(intensity_label)
        intensity_layout.addWidget(self.intensity_slider)
        intensity_layout.addWidget(self.intensity_value)
        left_column.addLayout(intensity_layout)

        # Кнопка збереження
        save_btn = StyledButton("💾 Зберегти")
        save_btn.setMinimumHeight(36)
        save_btn.setStyleSheet(ContractionCounterStyles.contraction_button())
        save_btn.clicked.connect(self.save_timed_contraction)
        left_column.addWidget(save_btn)

        # Ручний запис (компактний)
        manual_title = QLabel("✏️ Ручний запис")
        manual_title.setStyleSheet("color: white; font-weight: 700; font-size: 14px; background: transparent; border: none; margin-top: 8px;")
        left_column.addWidget(manual_title)

        # Компактна форма
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(6)
        form_layout.setHorizontalSpacing(10)

        # Дата
        date_manual_label = QLabel("📅")
        date_manual_label.setStyleSheet("color: white; font-size: 12px; font-weight: 600; background: transparent; border: none;")

        self.manual_date_edit = StyledDateEdit()
        self.manual_date_edit.setDate(QDate.currentDate())
        self.manual_date_edit.setMaximumHeight(32)
        form_layout.addRow(date_manual_label, self.manual_date_edit)

        # Час початку
        time_manual_label = QLabel("🕐")
        time_manual_label.setStyleSheet("color: white; font-size: 12px; font-weight: 600; background: transparent; border: none;")

        self.manual_time_edit = StyledInput("гг:хх")
        self.manual_time_edit.setText(QTime.currentTime().toString("HH:mm"))
        self.manual_time_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.manual_time_edit.setMaximumHeight(32)
        form_layout.addRow(time_manual_label, self.manual_time_edit)

        # Тривалість
        duration_manual_label = QLabel("⏱️")
        duration_manual_label.setStyleSheet("color: white; font-size: 12px; font-weight: 600; background: transparent; border: none;")

        self.manual_duration_spin = StyledSpinBox(10, 300)
        self.manual_duration_spin.setValue(60)
        self.manual_duration_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.manual_duration_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.manual_duration_spin.setMaximumHeight(32)
        form_layout.addRow(duration_manual_label, self.manual_duration_spin)

        # Інтенсивність
        intensity_manual_label = QLabel("🔥")
        intensity_manual_label.setStyleSheet("color: white; font-size: 12px; font-weight: 600; background: transparent; border: none;")

        self.manual_intensity_spin = StyledSpinBox(1, 10)
        self.manual_intensity_spin.setValue(5)
        self.manual_intensity_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.manual_intensity_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.manual_intensity_spin.setMaximumHeight(32)
        form_layout.addRow(intensity_manual_label, self.manual_intensity_spin)

        left_column.addLayout(form_layout)

        # Кнопка збереження ручного запису
        save_manual_btn = StyledButton("💾 Зберегти запис")
        save_manual_btn.setMinimumHeight(36)
        save_manual_btn.clicked.connect(self.save_manual_contraction)
        left_column.addWidget(save_manual_btn)

        # Права колонка - Історія та статистика
        right_column = QVBoxLayout()
        right_column.setSpacing(8)

        # Історія переймів зі скролом
        history_title = QLabel("📊 Історія переймів")
        history_title.setStyleSheet("color: white; font-weight: 700; font-size: 14px; background: transparent; border: none;")
        right_column.addWidget(history_title)

        # Scroll area для історії
        history_scroll = QScrollArea()
        history_scroll.setWidgetResizable(True)
        history_scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.5);
            }
        """)

        self.contractions_list = QListWidget()
        self.contractions_list.setStyleSheet("""
            QListWidget {
                background: transparent; 
                border: none; 
                color: white; 
                font-size: 12px;
            }
            QListWidget::item {
                padding: 4px 2px;
                border: none;
                background: transparent;
                color: white;
            }
            QListWidget::item:selected {
                background: rgba(255, 255, 255, 0.1);
                color: white;
            }
        """)
        self.contractions_list.setWordWrap(True)
        
        history_scroll.setWidget(self.contractions_list)
        history_scroll.setMaximumHeight(200)  # Обмежуємо висоту
        right_column.addWidget(history_scroll)

        # Статистика (компактна)
        stats_title = QLabel("📈 Статистика")
        stats_title.setStyleSheet("color: white; font-weight: 700; font-size: 14px; background: transparent; border: none; margin-top: 8px;")
        right_column.addWidget(stats_title)

        self.stats_label = QLabel("Завантаження...")
        self.stats_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 12px; background: transparent; border: none;")
        self.stats_label.setWordWrap(True)
        right_column.addWidget(self.stats_label)

        # Додаємо розтягуючий spacer для правої колонки
        right_column.addStretch()

        # Додаємо колонки до основного layout
        columns_layout.addLayout(left_column, 1)  # Ліва колонка займає 1 частину
        columns_layout.addLayout(right_column, 1)  # Права колонка займає 1 частину
        
        main_layout.addLayout(columns_layout)

    def showEvent(self, event):
        super().showEvent(event)
        if self.init_data_controller():
            self.load_contractions()

    def update_timer(self):
        if self.is_timing:
            self.current_seconds += 1
            minutes = self.current_seconds // 60
            seconds = self.current_seconds % 60
            self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
            self.progress_bar.setValue(min(self.current_seconds, 180))

    def start_contraction(self):
        self.start_time = datetime.datetime.now()
        self.current_seconds = 0
        self.is_timing = True
        self.timer.start(1000)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        self.timer_label.setText("00:00")
        logger.info("Почато відлік перейми")

    def stop_contraction(self):
        self.is_timing = False
        self.timer.stop()

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        logger.info(f"Зупинено відлік перейми. Тривалість: {self.current_seconds} секунд")

    def save_timed_contraction(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для збереження записів")
            return

        try:
            if self.is_timing:
                self.stop_contraction()

            user_id = self.get_current_user_id()
            date_str = QDate.currentDate().toString("yyyy-MM-dd")

            if self.start_time:
                start_time_str = self.start_time.strftime("%H:%M:%S")
                end_time = self.start_time + datetime.timedelta(seconds=self.current_seconds)
                end_time_str = end_time.strftime("%H:%M:%S")

                duration = self.current_seconds
                intensity = self.intensity_slider.value()

                self.data_controller.db.add_contraction(date_str, start_time_str, end_time_str, duration, intensity,
                                                        user_id)

                self.current_seconds = 0
                self.timer_label.setText("00:00")
                self.progress_bar.setValue(0)

                self.load_contractions()

                show_info(self, "Успіх", "Перейма збережена")
                logger.info(f"Збережено нову перейму для користувача {user_id}: {start_time_str} - {end_time_str}, тривалість: {duration}с, інтенсивність: {intensity}")
            else:
                show_warning(self, "Попередження", "Спочатку скористайтеся таймером для вимірювання перейми")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні перейми з таймера для користувача {user_id}: {str(e)}")

    def save_manual_contraction(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для збереження записів")
            return

        try:
            user_id = self.get_current_user_id()
            date_str = self.manual_date_edit.date().toString("yyyy-MM-dd")
            start_time_text = self.manual_time_edit.text().strip()
            
            # Валідація часу
            try:
                time_parts = start_time_text.split(':')
                if len(time_parts) != 2:
                    show_warning(self, "Помилка", "Невірний формат часу. Використовуйте формат гг:хх")
                    return
                    
                hour, minute = map(int, time_parts)
                if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                    show_warning(self, "Помилка", "Невірний час. Години: 0-23, хвилини: 0-59")
                    return
                start_time_str = f"{hour:02d}:{minute:02d}:00"
            except ValueError:
                show_warning(self, "Помилка", "Невірний формат часу. Використовуйте формат гг:хх")
                return
            
            # Обчислюємо час закінчення
            try:
                start_time = QTime(hour, minute)
                end_time = start_time.addSecs(self.manual_duration_spin.value())
                end_time_str = end_time.toString("HH:mm:ss")
            except:
                end_time_str = start_time_str
            
            duration = self.manual_duration_spin.value()
            intensity = self.manual_intensity_spin.value()

            self.data_controller.db.add_contraction(date_str, start_time_str, end_time_str, duration, intensity,
                                                    user_id)

            show_info(self, "Успіх", "Ручний запис збережено")
            logger.info(f"Збережено ручний запис перейми для користувача {user_id}: {date_str} {start_time_str}, тривалість: {duration}с, інтенсивність: {intensity}")

            # Оновлюємо список та статистику
            self.load_contractions()

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні перейми вручну для користувача {user_id}: {str(e)}")

    def load_contractions(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для перегляду записів")
            return

        try:
            user_id = self.get_current_user_id()
            contractions = self.data_controller.db.get_contractions(user_id)
            self.contractions_list.clear()

            for contraction in contractions:
                if contraction.get('start_time') and contraction.get('end_time'):
                    # Автоматичний запис
                    duration_text = f"{contraction['duration']}с"
                    item_text = f"🕐 {contraction['start_time']} - {contraction['end_time']} | ⏱️ {duration_text} | 💪 {contraction['intensity']}/10"
                else:
                    # Ручний запис
                    duration_text = f"{contraction['duration']}с"
                    item_text = f"✏️ {contraction['date']} {contraction['start_time']} | ⏱️ {duration_text} | 💪 {contraction['intensity']}/10"
                
                self.contractions_list.addItem(item_text)

            logger.info(f"Завантажено {len(contractions)} записів переймів для користувача {user_id}")
            
            # Оновлюємо статистику
            self.update_statistics(contractions)

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося завантажити історію переймів: {str(e)}")
            logger.error(f"Помилка при завантаженні переймів для користувача {user_id}: {str(e)}")

    def update_statistics(self, contractions):
        """Оновлює статистичну інформацію"""
        if not contractions:
            self.stats_label.setText("📊 Немає даних для статистики")
            return
            
        total_contractions = len(contractions)
        
        # Обчислюємо середню тривалість
        durations = [c['duration'] for c in contractions if c.get('duration')]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Обчислюємо середню інтенсивність
        intensities = [c['intensity'] for c in contractions if c.get('intensity')]
        avg_intensity = sum(intensities) / len(intensities) if intensities else 0
        
        # Знаходимо найдовшу та найкоротшу перейму
        max_duration = max(durations) if durations else 0
        min_duration = min(durations) if durations else 0
        
        # Формуємо текст статистики
        stats_text = f"""📊 Загальна кількість: {total_contractions}
⏱️ Середня тривалість: {avg_duration:.0f}с
💪 Середня інтенсивність: {avg_intensity:.1f}/10
📈 Найдовша: {max_duration}с
📉 Найкоротша: {min_duration}с"""

        self.stats_label.setText(stats_text)