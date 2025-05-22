import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QSplitter, QLabel
from PyQt6.QtCore import QDate
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.base_widgets import StyledCard, StyledInput, StyledDateEdit, StyledButton, StyledListWidget, TitleLabel
from utils.styles import Styles

logger = get_logger('health_report')

class HealthReportScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_notes()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = TitleLabel("Звіт про здоров'я", 22)
        main_layout.addWidget(title)

        splitter = QSplitter()
        splitter.setChildrenCollapsible(False)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = StyledCard("Додати нову нотатку")

        date_layout = QHBoxLayout()
        date_label = QLabel("Дата:")
        date_label.setStyleSheet(Styles.text_primary())
        self.date_edit = StyledDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        form_frame.layout.addLayout(date_layout)

        title_label = QLabel("Заголовок:")
        title_label.setStyleSheet(Styles.text_primary())
        self.title_edit = StyledInput()
        form_frame.layout.addWidget(title_label)
        form_frame.layout.addWidget(self.title_edit)

        content_label = QLabel("Текст нотатки:")
        content_label.setStyleSheet(Styles.text_primary())
        self.content_edit = QTextEdit()
        self.content_edit.setStyleSheet(Styles.input_field())
        form_frame.layout.addWidget(content_label)
        form_frame.layout.addWidget(self.content_edit)

        save_btn = StyledButton("Зберегти нотатку")
        save_btn.clicked.connect(self.save_note)
        form_frame.layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = StyledCard("Ваші нотатки")

        self.notes_list = StyledListWidget()
        list_frame.layout.addWidget(self.notes_list)

        buttons_layout = QHBoxLayout()

        refresh_btn = StyledButton("Оновити список", "secondary")
        refresh_btn.clicked.connect(self.load_notes)

        export_btn = StyledButton("Експортувати в PDF")
        export_btn.clicked.connect(self.export_to_pdf)

        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(export_btn)
        list_frame.layout.addLayout(buttons_layout)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_notes(self):
        try:
            notes = self.data_controller.db.get_health_notes()
            self.notes_list.clear()

            for note in notes:
                item_text = f"{note['date']} - {note['title']}"
                self.notes_list.addItem(item_text)

            logger.info(f"Завантажено {len(notes)} нотаток про здоров'я")
        except Exception as e:
            logger.error(f"Помилка при завантаженні нотаток: {str(e)}")

    def save_note(self):
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            title = self.title_edit.text().strip()
            content = self.content_edit.toPlainText().strip()

            if not content:
                return

            self.data_controller.db.add_health_note(date_str, content, title)

            self.title_edit.clear()
            self.content_edit.clear()
            self.load_notes()

            logger.info(f"Збережено нову нотатку про здоров'я: {date_str}, {title}")
        except Exception as e:
            logger.error(f"Помилка при збереженні нотатки: {str(e)}")

    def export_to_pdf(self):
        try:
            notes = self.data_controller.db.get_health_notes()
            if not notes:
                return

            today = datetime.date.today().strftime("%Y-%m-%d")
            file_name = f"health_report_{today}.pdf"

            pregnancy_data = self.data_controller.pregnancy_data
            current_week = self.data_controller.get_current_week() or "невідомо"
            user_profile = self.data_controller.user_profile

            document = SimpleDocTemplate(file_name, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)

            styles = getSampleStyleSheet()
            title_style = styles["Heading1"]
            subtitle_style = styles["Heading2"]
            normal_style = styles["Normal"]

            content = []
            content.append(Paragraph("Звіт про здоров'я", title_style))
            content.append(Spacer(1, 12))

            content.append(Paragraph("Інформація про користувача", subtitle_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"Ім'я: {user_profile.name}", normal_style))
            content.append(Paragraph(f"Поточний тиждень: {current_week}", normal_style))
            if pregnancy_data.due_date:
                content.append(Paragraph(f"Очікувана дата пологів: {pregnancy_data.due_date.strftime('%d.%m.%Y')}", normal_style))
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
            logger.info(f"Експортовано PDF-звіт: {file_name}")
        except Exception as e:
            logger.error(f"Помилка при експорті PDF: {str(e)}")