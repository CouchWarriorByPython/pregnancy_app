from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout,QMessageBox, QSplitter
from PyQt6.QtCore import Qt, QDate, QTime
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledDateEdit, StyledTimeEdit, StyledSpinBox,
                               StyledButton, StyledListWidget, TitleLabel)
from utils.styles import Styles

logger = get_logger('kick_counter')


class KickCounterScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_kicks()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = TitleLabel("Лічильник поштовхів", 22)
        title.setStyleSheet(Styles.title_colored("#4CAF50"))
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = StyledCard("Записати поштовхи")
        form_frame.setStyleSheet(Styles.card_colored("#4CAF50"))

        info_text = """
        <p>Підрахунок поштовхів дитини допомагає відстежувати її активність і здоров'я.</p>
        <p>Рекомендується рахувати поштовхи щодня в один і той самий час, наприклад, після їжі, 
        коли дитина найбільш активна.</p>
        <p>Занепокоєння може викликати значне зменшення кількості поштовхів.</p>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet(Styles.text_secondary())
        form_frame.layout.addWidget(info_label)

        date_layout = QHBoxLayout()
        date_label = QLabel("Дата:")
        date_label.setStyleSheet(Styles.text_primary())
        self.date_edit = StyledDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        form_frame.layout.addLayout(date_layout)

        time_layout = QHBoxLayout()
        time_label = QLabel("Час:")
        time_label.setStyleSheet(Styles.text_primary())
        self.time_edit = StyledTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_edit)
        form_frame.layout.addLayout(time_layout)

        kicks_layout = QHBoxLayout()
        kicks_label = QLabel("Кількість поштовхів:")
        kicks_label.setStyleSheet(Styles.text_primary())
        self.kicks_spin = StyledSpinBox(1, 100)
        self.kicks_spin.setValue(10)
        kicks_layout.addWidget(kicks_label)
        kicks_layout.addWidget(self.kicks_spin)
        form_frame.layout.addLayout(kicks_layout)

        save_btn = StyledButton("Зберегти запис")
        save_btn.setStyleSheet(Styles.button_colored("#4CAF50", "#388E3C"))
        save_btn.clicked.connect(self.save_kicks)
        form_frame.layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = StyledCard("Історія поштовхів")
        list_frame.setStyleSheet(Styles.card_colored("#4CAF50"))

        self.kicks_list = StyledListWidget()
        list_frame.layout.addWidget(self.kicks_list)

        refresh_btn = StyledButton("Оновити історію", "secondary")
        refresh_btn.clicked.connect(self.load_kicks)
        list_frame.layout.addWidget(refresh_btn)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_kicks(self):
        try:
            kicks = self.data_controller.db.get_baby_kicks()
            self.kicks_list.clear()

            for kick in kicks:
                item_text = f"{kick['date']} {kick['time']}: {kick['count']} поштовхів"
                self.kicks_list.addItem(item_text)

            logger.info(f"Завантажено {len(kicks)} записів поштовхів")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити історію поштовхів: {str(e)}")
            logger.error(f"Помилка при завантаженні поштовхів: {str(e)}")

    def save_kicks(self):
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            time_str = self.time_edit.time().toString("HH:mm")
            count = self.kicks_spin.value()

            self.data_controller.db.add_baby_kick(date_str, time_str, count)
            self.load_kicks()

            QMessageBox.information(self, "Успіх", "Запис поштовхів успішно збережено")
            logger.info(f"Збережено новий запис поштовхів: {date_str} {time_str}, кількість: {count}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису поштовхів: {str(e)}")