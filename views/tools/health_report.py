import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QSplitter, QLabel, QMessageBox
from PyQt6.QtCore import QDate
from utils.logger import get_logger
from utils.base_widgets import StyledCard, StyledInput, StyledDateEdit, StyledButton, StyledListWidget, TitleLabel
from styles import HealthReportStyles, BaseStyles
from utils.user_mixin import UserMixin

logger = get_logger('health_report')


class HealthReportScreen(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = TitleLabel("Звіт про здоров'я", 22)
        title.setStyleSheet("color: #FF5252; font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        splitter = QSplitter()
        splitter.setChildrenCollapsible(False)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = StyledCard("Додати нову нотатку")
        form_frame.setStyleSheet(HealthReportStyles.report_card())

        date_layout = QHBoxLayout()
        date_label = QLabel("Дата:")
        date_label.setStyleSheet(BaseStyles.text_primary())
        self.date_edit = StyledDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        form_frame.layout.addLayout(date_layout)

        title_label = QLabel("Заголовок:")
        title_label.setStyleSheet(BaseStyles.text_primary())
        self.title_edit = StyledInput()
        form_frame.layout.addWidget(title_label)
        form_frame.layout.addWidget(self.title_edit)

        content_label = QLabel("Текст нотатки:")
        content_label.setStyleSheet(BaseStyles.text_primary())
        self.content_edit = QTextEdit()
        self.content_edit.setStyleSheet(BaseStyles.input_field())
        form_frame.layout.addWidget(content_label)
        form_frame.layout.addWidget(self.content_edit)

        save_btn = StyledButton("Зберегти нотатку")
        save_btn.setStyleSheet(HealthReportStyles.export_button())
        save_btn.clicked.connect(self.save_note)
        form_frame.layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = StyledCard("Ваші нотатки")
        list_frame.setStyleSheet(HealthReportStyles.report_card())

        self.notes_list = StyledListWidget()
        list_frame.layout.addWidget(self.notes_list)

        buttons_layout = QHBoxLayout()

        refresh_btn = StyledButton("Оновити список", "secondary")
        refresh_btn.clicked.connect(self.load_notes)

        export_btn = StyledButton("Експортувати в PDF")
        export_btn.setStyleSheet(HealthReportStyles.export_button())
        export_btn.clicked.connect(self.export_to_pdf)

        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(export_btn)
        list_frame.layout.addLayout(buttons_layout)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def showEvent(self, event):
        super().showEvent(event)
        if self.init_data_controller():
            self.load_notes()

    def load_notes(self):
        if not self.init_data_controller():
            QMessageBox.warning(self, "Помилка", "Необхідно увійти в систему для перегляду нотаток")
            return

        try:
            user_id = self.get_current_user_id()
            notes = self.data_controller.db.get_health_notes(user_id)
            self.notes_list.clear()

            for note in notes:
                item_text = f"{note['date']} - {note['title']}"
                self.notes_list.addItem(item_text)

            logger.info(f"Завантажено {len(notes)} нотаток про здоров'я для користувача {user_id}")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити нотатки: {str(e)}")
            logger.error(f"Помилка при завантаженні нотаток для користувача {user_id}: {str(e)}")

    def save_note(self):
        if not self.init_data_controller():
            QMessageBox.warning(self, "Помилка", "Необхідно увійти в систему для збереження нотаток")
            return

        try:
            user_id = self.get_current_user_id()
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            title = self.title_edit.text().strip()
            content = self.content_edit.toPlainText().strip()

            if not content:
                QMessageBox.warning(self, "Помилка", "Введіть текст нотатки")
                return

            self.data_controller.db.add_health_note(date_str, content, title, user_id)

            self.title_edit.clear()
            self.content_edit.clear()
            self.load_notes()

            QMessageBox.information(self, "Успіх", "Нотатку збережено")
            logger.info(f"Збережено нову нотатку про здоров'я для користувача {user_id}: {date_str}, {title}")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти нотатку: {str(e)}")
            logger.error(f"Помилка при збереженні нотатки для користувача {user_id}: {str(e)}")

    def export_to_pdf(self):
        if not self.init_data_controller():
            QMessageBox.warning(self, "Помилка", "Необхідно увійти в систему для експорту")
            return

        try:
            user_id = self.get_current_user_id()
            notes = self.data_controller.db.get_health_notes(user_id)
            if not notes:
                QMessageBox.information(self, "Інформація", "Немає нотаток для експорту")
                return

            today = datetime.date.today().strftime("%Y-%m-%d")
            file_name = f"health_report_{today}.pdf"

            current_week = self.data_controller.get_current_week() or "невідомо"
            user_profile = self.data_controller.user_profile
            pregnancy_data = self.data_controller.pregnancy_data

            document = SimpleDocTemplate(file_name, pageSize=A4, rightMargin=72, leftMargin=72, topMargin=72,
                                         bottomMargin=72)

            styles = getSampleStyleSheet()
            title_style = styles["Heading1"]
            subtitle_style = styles["Heading2"]
            normal_style = styles["Normal"]

            content = []
            content.append(Paragraph("Звіт про здоров'я", title_style))
            content.append(Spacer(1, 12))

            content.append(Paragraph("Інформація про користувача", subtitle_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"Ім'я: {user_profile.name if user_profile else 'Не вказано'}", normal_style))
            content.append(Paragraph(f"Поточний тиждень: {current_week}", normal_style))
            if pregnancy_data and pregnancy_data.due_date:
                content.append(
                    Paragraph(f"Очікувана дата пологів: {pregnancy_data.due_date.strftime('%d.%m.%Y')}", normal_style))
            content.append(Spacer(1, 12))

            content.append(Paragraph("Нотатки про здоров'я", subtitle_style))
            content.append(Spacer(1, 6))

            for note in notes:
                note_date = note['date']
                note_title = note['title'] or "Без заголовку"
                note_content = note['content']

                content.append(Paragraph(f"<b>{note_date} - {note_title}</b>", normal_style))
                content.append(Paragraph(note_content, normal_style))
                content.append(Spacer(1, 12))

            document.build(content)

            QMessageBox.information(self, "Успіх", f"PDF-звіт збережено як {file_name}")
            logger.info(f"Експортовано PDF-звіт для користувача {user_id}: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося експортувати PDF: {str(e)}")
            logger.error(f"Помилка при експорті PDF для користувача {user_id}: {str(e)}")