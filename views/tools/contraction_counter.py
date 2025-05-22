import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QDateEdit, QTimeEdit, QSpinBox, QHBoxLayout, QListWidget,
                             QMessageBox, QFrame, QSlider, QTabWidget, QGridLayout, QProgressBar)
from PyQt6.QtCore import Qt, QDate, QTime, QTimer
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.styles import Styles

logger = get_logger('contraction_counter')


class ContractionCounterScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.start_time = None
        self.current_seconds = 0
        self.is_timing = False

        self.setup_ui()
        self.load_contractions()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = QLabel("Лічильник переймів")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2196F3;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {Styles.COLORS['surface_variant']};
                background-color: {Styles.COLORS['surface']};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {Styles.COLORS['surface_variant']};
                color: {Styles.COLORS['text_primary']};
                padding: 8px 15px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: #2196F3;
                color: white;
            }}
        """)

        timer_tab = QWidget()
        self.setup_timer_tab(timer_tab)
        tab_widget.addTab(timer_tab, "Лічильник")

        manual_tab = QWidget()
        self.setup_manual_tab(manual_tab)
        tab_widget.addTab(manual_tab, "Ручний запис")

        history_tab = QWidget()
        self.setup_history_tab(history_tab)
        tab_widget.addTab(history_tab, "Історія")

        main_layout.addWidget(tab_widget)

    def setup_timer_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        info_text = """
        <p>Використовуйте цей таймер для вимірювання тривалості та інтервалів переймів.</p>
        <p>Натисніть <b>"Почати перейму"</b>, коли відчуваєте початок перейми, і <b>"Зупинити перейму"</b>, 
        коли вона закінчиться.</p>
        <p>Записуйте результати, щоб відстежувати прогрес.</p>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet(f"color: white; background-color: {Styles.COLORS['surface_variant']}; padding: 10px; border-radius: 5px;")
        layout.addWidget(info_label)

        timer_frame = QFrame()
        timer_frame.setStyleSheet(Styles.form_container())
        timer_layout = QVBoxLayout(timer_frame)

        self.timer_label = QLabel("00:00")
        self.timer_label.setFont(QFont('Arial', 40, QFont.Weight.Bold))
        self.timer_label.setStyleSheet("color: #2196F3;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.timer_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 180)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Styles.COLORS['border']};
                border-radius: 5px;
                height: 15px;
            }}
            QProgressBar::chunk {{
                background-color: #2196F3;
                border-radius: 5px;
            }}
        """)
        timer_layout.addWidget(self.progress_bar)

        buttons_layout = QHBoxLayout()

        self.start_btn = QPushButton("Почати перейму")
        self.start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Styles.COLORS['success']};
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Styles.COLORS['success_hover']};
            }}
        """)
        self.start_btn.clicked.connect(self.start_contraction)

        self.stop_btn = QPushButton("Зупинити перейму")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Styles.COLORS['error']};
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Styles.COLORS['error_hover']};
            }}
            QPushButton:disabled {{
                background-color: #777777;
                color: #AAAAAA;
            }}
        """)
        self.stop_btn.clicked.connect(self.stop_contraction)

        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.stop_btn)
        timer_layout.addLayout(buttons_layout)

        intensity_layout = QHBoxLayout()
        intensity_label = QLabel("Інтенсивність:")
        intensity_label.setStyleSheet(Styles.text_primary())

        self.intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.intensity_slider.setRange(1, 10)
        self.intensity_slider.setValue(5)
        self.intensity_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.intensity_slider.setTickInterval(1)
        self.intensity_slider.setStyleSheet(Styles.slider())

        self.intensity_value = QLabel("5")
        self.intensity_value.setStyleSheet(f"color: {Styles.COLORS['text_primary']}; font-weight: bold;")
        self.intensity_slider.valueChanged.connect(lambda v: self.intensity_value.setText(str(v)))

        intensity_layout.addWidget(intensity_label)
        intensity_layout.addWidget(self.intensity_slider)
        intensity_layout.addWidget(self.intensity_value)
        timer_layout.addLayout(intensity_layout)

        save_btn = QPushButton("Зберегти результат")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """)
        save_btn.clicked.connect(self.save_timed_contraction)
        timer_layout.addWidget(save_btn)

        layout.addWidget(timer_frame)
        layout.addStretch()

    def setup_manual_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        form_frame = QFrame()
        form_frame.setStyleSheet(Styles.form_container())
        form_layout = QGridLayout(form_frame)
        form_layout.setColumnStretch(1, 1)

        date_label = QLabel("Дата:")
        date_label.setStyleSheet(Styles.text_primary())
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet(Styles.date_time_edit())
        form_layout.addWidget(date_label, 0, 0)
        form_layout.addWidget(self.date_edit, 0, 1)

        start_time_label = QLabel("Час початку:")
        start_time_label.setStyleSheet(Styles.text_primary())
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime.currentTime())
        self.start_time_edit.setStyleSheet(Styles.date_time_edit())
        form_layout.addWidget(start_time_label, 1, 0)
        form_layout.addWidget(self.start_time_edit, 1, 1)

        end_time_label = QLabel("Час закінчення:")
        end_time_label.setStyleSheet(Styles.text_primary())
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime.currentTime().addSecs(60))
        self.end_time_edit.setStyleSheet(Styles.date_time_edit())
        form_layout.addWidget(end_time_label, 2, 0)
        form_layout.addWidget(self.end_time_edit, 2, 1)

        duration_label = QLabel("Тривалість (сек):")
        duration_label.setStyleSheet(Styles.text_primary())
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 600)
        self.duration_spin.setValue(60)
        self.duration_spin.setStyleSheet(Styles.spinbox())
        form_layout.addWidget(duration_label, 3, 0)
        form_layout.addWidget(self.duration_spin, 3, 1)

        intensity_label = QLabel("Інтенсивність (1-10):")
        intensity_label.setStyleSheet(Styles.text_primary())
        self.manual_intensity_spin = QSpinBox()
        self.manual_intensity_spin.setRange(1, 10)
        self.manual_intensity_spin.setValue(5)
        self.manual_intensity_spin.setStyleSheet(Styles.spinbox())
        form_layout.addWidget(intensity_label, 4, 0)
        form_layout.addWidget(self.manual_intensity_spin, 4, 1)

        save_btn = QPushButton("Зберегти запис")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """)
        save_btn.clicked.connect(self.save_manual_contraction)
        form_layout.addWidget(save_btn, 5, 0, 1, 2)

        layout.addWidget(form_frame)
        layout.addStretch()

    def setup_history_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        self.contractions_list = QListWidget()
        self.contractions_list.setStyleSheet(Styles.list_widget())
        layout.addWidget(self.contractions_list)

        buttons_layout = QHBoxLayout()

        refresh_btn = QPushButton("Оновити історію")
        refresh_btn.setStyleSheet(Styles.button_secondary())
        refresh_btn.clicked.connect(self.load_contractions)

        period_label = QLabel("Показати за:")
        period_label.setStyleSheet(Styles.text_primary())

        self.period_spin = QSpinBox()
        self.period_spin.setRange(1, 7)
        self.period_spin.setValue(1)
        self.period_spin.setSuffix(" день")
        self.period_spin.setStyleSheet(Styles.spinbox())
        self.period_spin.valueChanged.connect(self.load_contractions)

        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(period_label)
        buttons_layout.addWidget(self.period_spin)

        layout.addLayout(buttons_layout)

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
        try:
            if self.is_timing:
                self.stop_contraction()

            date_str = QDate.currentDate().toString("yyyy-MM-dd")

            if self.start_time:
                start_time_str = self.start_time.strftime("%H:%M:%S")
                end_time = self.start_time + datetime.timedelta(seconds=self.current_seconds)
                end_time_str = end_time.strftime("%H:%M:%S")

                duration = self.current_seconds
                intensity = self.intensity_slider.value()

                self.data_controller.db.add_contraction(date_str, start_time_str, end_time_str, duration, intensity)

                self.current_seconds = 0
                self.timer_label.setText("00:00")
                self.progress_bar.setValue(0)

                self.load_contractions()

                QMessageBox.information(self, "Успіх", "Запис про перейму успішно збережено")
                logger.info(f"Збережено перейму: {date_str}, {start_time_str}-{end_time_str}, {duration} сек, інтенсивність: {intensity}")
            else:
                QMessageBox.warning(self, "Попередження", "Спочатку скористайтеся таймером для вимірювання перейми")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні перейми з таймера: {str(e)}")

    def save_manual_contraction(self):
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            start_time_str = self.start_time_edit.time().toString("HH:mm:ss")
            end_time_str = self.end_time_edit.time().toString("HH:mm:ss")
            duration = self.duration_spin.value()
            intensity = self.manual_intensity_spin.value()

            self.data_controller.db.add_contraction(date_str, start_time_str, end_time_str, duration, intensity)
            self.load_contractions()

            QMessageBox.information(self, "Успіх", "Запис про перейму успішно збережено")
            logger.info(f"Збережено перейму (ручний запис): {date_str}, {start_time_str}-{end_time_str}, {duration} сек, інтенсивність: {intensity}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні перейми вручну: {str(e)}")

    def load_contractions(self):
        try:
            days = self.period_spin.value() if hasattr(self, 'period_spin') else 1
            contractions = self.data_controller.db.get_contractions(days)

            if hasattr(self, 'contractions_list'):
                self.contractions_list.clear()

                for contraction in contractions:
                    item_text = f"{contraction['date']} {contraction['start_time']}-{contraction['end_time']}: " \
                                f"{contraction['duration']} сек., інтенсивність: {contraction['intensity']}/10"
                    self.contractions_list.addItem(item_text)

                logger.info(f"Завантажено {len(contractions)} записів переймів за {days} день/днів")

        except Exception as e:
            if hasattr(self, 'contractions_list'):
                QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити історію переймів: {str(e)}")
            logger.error(f"Помилка при завантаженні переймів: {str(e)}")