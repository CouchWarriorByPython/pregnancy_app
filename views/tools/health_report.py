import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
                             QDateEdit, QLineEdit, QHBoxLayout, QListWidget,
                             QListWidgetItem, QMessageBox, QSplitter, QFrame)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from utils.logger import get_logger

logger = get_logger('health_report')


class HealthReportScreen(QWidget):
    """Екран для запису нотаток про здоров'я та генерації звіту"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_notes()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Звіт про здоров'я")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF5252;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Додаємо спліттер для розділення форми додавання і списку нотаток
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # === Ліва частина - форма для додавання нотаток ===
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #222222; border-radius: 10px; padding: 10px;")
        form_layout = QVBoxLayout(form_frame)

        form_title = QLabel("Додати нову нотатку")
        form_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        form_title.setStyleSheet("color: #FF5252;")
        form_layout.addWidget(form_title)

        # Дата
        date_layout = QHBoxLayout()
        date_label = QLabel("Дата:")
        date_label.setStyleSheet("color: white;")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        form_layout.addLayout(date_layout)

        # Заголовок нотатки
        title_label = QLabel("Заголовок:")
        title_label.setStyleSheet("color: white;")
        self.title_edit = QLineEdit()
        self.title_edit.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        form_layout.addWidget(title_label)
        form_layout.addWidget(self.title_edit)

        # Текст нотатки
        content_label = QLabel("Текст нотатки:")
        content_label.setStyleSheet("color: white;")
        self.content_edit = QTextEdit()
        self.content_edit.setStyleSheet("""
            QTextEdit {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        form_layout.addWidget(content_label)
        form_layout.addWidget(self.content_edit)

        # Кнопка збереження
        save_btn = QPushButton("Зберегти нотатку")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5252;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF1744;
            }
        """)
        save_btn.clicked.connect(self.save_note)
        form_layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        # === Права частина - список нотаток ===
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = QFrame()
        list_frame.setStyleSheet("background-color: #222222; border-radius: 10px; padding: 10px;")
        list_layout = QVBoxLayout(list_frame)

        list_title = QLabel("Ваші нотатки")
        list_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        list_title.setStyleSheet("color: #FF5252;")
        list_layout.addWidget(list_title)

        # Список нотаток
        self.notes_list = QListWidget()
        self.notes_list.setStyleSheet("""
            QListWidget {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #444444;
            }
            QListWidget::item:selected {
                background-color: #FF5252;
            }
        """)
        list_layout.addWidget(self.notes_list)

        # Кнопки для експорту PDF та оновлення списку
        buttons_layout = QHBoxLayout()

        refresh_btn = QPushButton("Оновити список")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        refresh_btn.clicked.connect(self.load_notes)

        export_btn = QPushButton("Експортувати в PDF")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5252;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF1744;
            }
        """)
        export_btn.clicked.connect(self.export_to_pdf)

        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(export_btn)
        list_layout.addLayout(buttons_layout)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_notes(self):
        """Завантажує всі нотатки про здоров'я з бази даних"""
        try:
            notes = self.data_controller.db.get_health_notes()

            self.notes_list.clear()

            for note in notes:
                item_text = f"{note['date']} - {note['title']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, note)
                self.notes_list.addItem(item)

            logger.info(f"Завантажено {len(notes)} нотаток про здоров'я")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити нотатки: {str(e)}")
            logger.error(f"Помилка при завантаженні нотаток: {str(e)}")

    def save_note(self):
        """Зберігає нову нотатку про здоров'я"""
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            title = self.title_edit.text().strip()
            content = self.content_edit.toPlainText().strip()

            if not content:
                QMessageBox.warning(self, "Попередження", "Введіть текст нотатки")
                return

            # Зберігаємо нотатку в базу
            self.data_controller.db.add_health_note(date_str, content, title)

            # Очищаємо поля введення
            self.title_edit.clear()
            self.content_edit.clear()

            # Оновлюємо список нотаток
            self.load_notes()

            QMessageBox.information(self, "Успіх", "Нотатку успішно збережено")
            logger.info(f"Збережено нову нотатку про здоров'я: {date_str}, {title}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти нотатку: {str(e)}")
            logger.error(f"Помилка при збереженні нотатки: {str(e)}")

    def export_to_pdf(self):
        """Експортує всі нотатки у PDF-файл"""
        try:
            # Отримуємо всі нотатки
            notes = self.data_controller.db.get_health_notes()

            if not notes:
                QMessageBox.information(self, "Інформація", "Немає нотаток для експорту")
                return

            # Створюємо PDF-звіт
            today = datetime.date.today().strftime("%Y-%m-%d")
            file_name = f"health_report_{today}.pdf"

            # Отримуємо інформацію про вагітність
            pregnancy_data = self.data_controller.pregnancy_data
            current_week = self.data_controller.get_current_week() or "невідомо"

            # Отримуємо інформацію про користувача
            user_profile = self.data_controller.user_profile

            # Створюємо PDF-документ
            document = SimpleDocTemplate(
                file_name,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Створюємо контент
            styles = getSampleStyleSheet()

            # Визначаємо стиль для заголовків і тексту
            title_style = styles["Heading1"]
            subtitle_style = styles["Heading2"]
            normal_style = styles["Normal"]

            # Підготовка вмісту PDF
            content = []

            # Додавання заголовка
            content.append(Paragraph("Звіт про здоров'я", title_style))
            content.append(Spacer(1, 12))

            # Інформація про користувача
            content.append(Paragraph("Інформація про користувача", subtitle_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"Ім'я: {user_profile.name}", normal_style))
            content.append(Paragraph(f"Поточний тиждень: {current_week}", normal_style))
            if pregnancy_data.due_date:
                content.append(
                    Paragraph(f"Очікувана дата пологів: {pregnancy_data.due_date.strftime('%d.%m.%Y')}", normal_style))
            content.append(Spacer(1, 12))

            # Додаємо всі нотатки
            content.append(Paragraph("Нотатки про здоров'я", subtitle_style))
            content.append(Spacer(1, 6))

            for note in notes:
                note_date = note['date']
                note_title = note['title'] or "Без заголовку"
                note_content = note['content']

                content.append(Paragraph(f"<b>{note_date} - {note_title}</b>", normal_style))
                content.append(Paragraph(note_content, normal_style))
                content.append(Spacer(1, 12))

            # Будуємо PDF-файл
            document.build(content)

            QMessageBox.information(self, "Успіх", f"Звіт успішно експортовано у файл {file_name}")
            logger.info(f"Експортовано PDF-звіт: {file_name}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося експортувати звіт: {str(e)}")
            logger.error(f"Помилка при експорті PDF: {str(e)}")