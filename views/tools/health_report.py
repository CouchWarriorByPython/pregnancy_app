import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QSplitter, QLabel, QMessageBox, QFormLayout, QAbstractSpinBox
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtCore import QDate, Qt
from utils.logger import get_logger
from utils.base_widgets import StyledCard, StyledInput, StyledDateEdit, StyledButton, StyledListWidget, TitleLabel
from styles import HealthReportStyles, BaseStyles, OnboardingScreenStyles
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
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(12)

        # Простий заголовок
        title = TitleLabel("Звіт про здоров'я", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Ведіть щоденник здоров'я та самопочуття")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Відступ
        main_layout.addSpacing(20)

        # Форма з підкресленими полями
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)
        form_layout.setHorizontalSpacing(20)

        # Дата
        date_label = QLabel("📅 Дата:")
        date_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        date_label.setMinimumHeight(24)

        self.date_edit = StyledDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow(date_label, self.date_edit)

        # Заголовок
        title_label = QLabel("📝 Заголовок:")
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        title_label.setMinimumHeight(24)

        self.title_edit = StyledInput("Введіть заголовок запису")
        self.title_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.title_edit.setMinimumHeight(24)
        self.title_edit.setMaximumHeight(40)

        form_layout.addRow(title_label, self.title_edit)

        main_layout.addLayout(form_layout)

        # Текст нотатки
        content_label = QLabel("📝 Текст нотатки:")
        content_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(content_label)

        self.content_edit = QTextEdit()
        self.content_edit.setStyleSheet("background: transparent; border: none; border-bottom: 2px solid rgba(139, 92, 246, 1); color: white; font-size: 16px; padding: 4px 4px 4px 4px; min-height: 100px;")
        self.content_edit.setPlaceholderText("Опишіть ваше самопочуття, симптоми, настрій...")
        main_layout.addWidget(self.content_edit)

        # Відступ
        main_layout.addSpacing(20)

        # Кнопка збереження
        save_btn = StyledButton("💾 Зберегти нотатку")
        save_btn.setMinimumHeight(44)
        save_btn.setStyleSheet(HealthReportStyles.export_button())
        save_btn.clicked.connect(self.save_note)
        main_layout.addWidget(save_btn)

        # Відступ
        main_layout.addSpacing(20)

        # Історія без рамки
        history_title = QLabel("📊 Ваші нотатки")
        history_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(history_title)

        self.notes_list = StyledListWidget()
        self.notes_list.setStyleSheet("""
            QListWidget {
                background: transparent; 
                border: none; 
                border-bottom: 2px solid rgba(255, 255, 255, 0.3); 
                color: white; 
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px 4px;
                border: none;
                background: transparent;
                color: white;
                min-height: 20px;
            }
            QListWidget::item:selected {
                background: rgba(255, 255, 255, 0.1);
                color: white;
            }
        """)
        self.notes_list.setWordWrap(True)
        self.notes_list.setTextElideMode(Qt.TextElideMode.ElideNone)
        main_layout.addWidget(self.notes_list)

        # Кнопка експорту
        export_btn = StyledButton("📄 Експортувати в PDF")
        export_btn.setMinimumHeight(44)
        export_btn.setStyleSheet(HealthReportStyles.export_button())
        export_btn.clicked.connect(self.export_to_pdf)
        main_layout.addWidget(export_btn)

        # Розтягуючий spacer
        main_layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        if self.init_data_controller():
            self.load_notes()

    def load_notes(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для перегляду нотаток")
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
            show_error(self, "Помилка", f"Не вдалося завантажити нотатки: {str(e)}")
            logger.error(f"Помилка при завантаженні нотаток для користувача {user_id}: {str(e)}")

    def save_note(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для збереження нотаток")
            return

        try:
            user_id = self.get_current_user_id()
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            title = self.title_edit.text().strip()
            content = self.content_edit.toPlainText().strip()

            if not content:
                show_warning(self, "Помилка", "Введіть текст нотатки")
                return

            self.data_controller.db.add_health_note(date_str, content, title, user_id)

            self.title_edit.clear()
            self.content_edit.clear()
            self.load_notes()

            show_info(self, "Успіх", "Нотатку збережено")
            logger.info(f"Збережено нову нотатку про здоров'я для користувача {user_id}: {date_str}, {title}")
        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося зберегти нотатку: {str(e)}")
            logger.error(f"Помилка при збереженні нотатки для користувача {user_id}: {str(e)}")

    def export_to_pdf(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для експорту")
            return

        try:
            user_id = self.get_current_user_id()
            notes = self.data_controller.db.get_health_notes(user_id)
            if not notes:
                show_info(self, "Інформація", "Немає нотаток для експорту")
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

            show_info(self, "Успіх", f"PDF-звіт збережено як {file_name}")
            logger.info(f"Експортовано PDF-звіт для користувача {user_id}: {file_name}")
        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося експортувати PDF: {str(e)}")
            logger.error(f"Помилка при експорті PDF для користувача {user_id}: {str(e)}")