"""
Стилі для екранів налаштувань
"""

from ..base import BaseStyles, Colors


class SettingsScreenStyles:
    @staticmethod
    def main_header():
        """Головний заголовок екрану налаштувань"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(139, 92, 246, 0.15), 
                    stop:1 rgba(236, 72, 153, 0.1));
                border-bottom: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 12px;
                margin: 8px;
            }}
        """

    @staticmethod
    def header_title():
        """Стиль заголовка"""
        return f"""
            QLabel {{
                color: white;
                font-weight: 700;
                text-align: center;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def tab_selector():
        """Контейнер для табів"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(30, 27, 75, 0.9), 
                    stop:1 rgba(49, 46, 129, 0.8));
                border-radius: 16px;
                margin: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
        """

    @staticmethod
    def tab_button():
        """Кнопки табів налаштувань з покращеним дизайном"""
        return f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.1);
                font-size: 15px;
                font-weight: 600;
                padding: 12px 20px;
                text-align: center;
                border-radius: 12px;
                margin: 2px;
            }}
            QPushButton:checked {{
                background: {Colors.PRIMARY_GRADIENT};
                color: white;
                font-weight: 700;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
            QPushButton:hover:!checked {{
                background: rgba(255, 255, 255, 0.12);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            QPushButton:pressed {{
                background: rgba(255, 255, 255, 0.25);
            }}
        """

    @staticmethod
    def editor_form():
        """Форми редакторів"""
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 24px;
                margin: 12px;
            }}
        """

    @staticmethod
    def field_label():
        """Підписи полів"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """

    @staticmethod
    def field_hint():
        """Підказки для полів"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
                font-weight: 400;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """

    @staticmethod
    def info_frame():
        """Інформаційні фрейми"""
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(59, 130, 246, 0.1), stop:1 rgba(29, 78, 216, 0.05));
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 20px;
                padding: 20px;
                margin: 12px;
            }}
        """

    @staticmethod
    def logout_section():
        """Секція виходу з покращеним дизайном"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(239, 68, 68, 0.15), 
                    stop:1 rgba(220, 38, 38, 0.1));
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 16px;
                margin: 12px;
            }}
        """

    @staticmethod
    def save_button():
        """Кнопка збереження"""
        return BaseStyles.button_primary()

    @staticmethod
    def logout_button():
        """Кнопка виходу з анімаціями"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #EF4444, stop:1 #DC2626);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 16px 32px;
                font-weight: 700;
                font-size: 16px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #DC2626, stop:1 #B91C1C);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #B91C1C, stop:1 #991B1B);
            }}
        """


class ProfileEditorStyles:
    @staticmethod
    def title_container():
        """Контейнер заголовка профілю"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(139, 92, 246, 0.15), 
                    stop:1 rgba(236, 72, 153, 0.1));
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 16px;
                padding: 16px;
            }}
        """

    @staticmethod
    def section_title():
        """Заголовок секції"""
        return "color: white; font-weight: 700;"

    @staticmethod
    def section_subtitle():
        """Підзаголовок секції"""
        return "color: rgba(255, 255, 255, 0.8); font-size: 14px; margin-top: 4px;"

    @staticmethod
    def form_label():
        """Підписи полів форми"""
        return f"""
            QLabel {{
                color: white;
                font-size: 15px;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 8px 0px;
            }}
        """

    @staticmethod
    def disabled_email_field():
        """Неактивне поле email"""
        return f"""
            QLineEdit {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 14px 18px;
                color: rgba(255, 255, 255, 0.6);
                font-size: 14px;
                font-style: italic;
            }}
        """

    @staticmethod
    def save_button():
        """Кнопка збереження профілю"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #10B981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 16px 32px;
                font-weight: 700;
                font-size: 16px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #059669, stop:1 #047857);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #047857, stop:1 #065F46);
            }}
        """


class PregnancyEditorStyles:
    @staticmethod
    def title_container():
        """Контейнер заголовка вагітності"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(236, 72, 153, 0.15), 
                    stop:1 rgba(219, 39, 119, 0.1));
                border: 1px solid rgba(236, 72, 153, 0.3);
                border-radius: 16px;
                padding: 16px;
            }}
        """

    @staticmethod
    def section_title():
        """Заголовок секції"""
        return "color: white; font-weight: 700;"

    @staticmethod
    def section_subtitle():
        """Підзаголовок секції"""
        return "color: rgba(255, 255, 255, 0.8); font-size: 14px; margin-top: 4px;"

    @staticmethod
    def form_frame():
        """Фрейм форми вагітності"""
        return f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 24px;
            }}
        """

    @staticmethod
    def field_label():
        """Підписи полів вагітності"""
        return f"""
            color: white;
            font-size: 16px;
            font-weight: 600;
            background: transparent;
            border: none;
            padding: 8px 0px;
        """

    @staticmethod
    def date_edit():
        """Поля дати в редакторі вагітності"""
        return f"""
            QDateEdit {{
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 14px 18px;
                color: white;
                font-size: 15px;
                font-weight: 500;
                min-height: 24px;
            }}
            QDateEdit:focus {{
                border: 2px solid #EC4899;
                background: rgba(255, 255, 255, 0.18);
            }}
            QDateEdit::drop-down {{
                border: none;
                width: 32px;
                background: transparent;
            }}
            QDateEdit::down-arrow {{
                image: none;
                border: 6px solid transparent;
                border-top: 10px solid white;
                margin-right: 8px;
            }}
            QCalendarWidget {{
                background: #1E1B4B;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }}
            QCalendarWidget QToolButton {{
                color: white;
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 6px;
                padding: 6px;
                margin: 2px;
            }}
            QCalendarWidget QToolButton:hover {{
                background: rgba(255, 255, 255, 0.2);
            }}
            QCalendarWidget QAbstractItemView {{
                background: #1E1B4B;
                color: white;
                selection-background-color: #EC4899;
                selection-color: white;
            }}
        """

    @staticmethod
    def due_date_label():
        """Неактивне поле для дати пологів"""
        return f"""
            QLabel {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(16, 185, 129, 0.2), 
                    stop:1 rgba(5, 150, 105, 0.1));
                border: 1px solid rgba(16, 185, 129, 0.4);
                border-radius: 12px;
                padding: 14px 18px;
                color: white;
                font-size: 15px;
                font-weight: 600;
            }}
        """

    @staticmethod
    def info_frame():
        """Інформаційний фрейм з термінами"""
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(59, 130, 246, 0.15), 
                    stop:1 rgba(29, 78, 216, 0.1));
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 20px;
                padding: 24px;
            }}
        """

    @staticmethod
    def info_title():
        """Заголовок інформації"""
        return "color: white; font-weight: 700; margin-bottom: 8px;"

    @staticmethod
    def info_label():
        """Інформаційні підписи"""
        return "color: white; background: transparent; border: none; font-weight: 500; padding: 4px 0px;"

    @staticmethod
    def save_button():
        """Кнопка збереження вагітності"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #EC4899, stop:1 #DB2777);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 16px 32px;
                font-weight: 700;
                font-size: 16px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #DB2777, stop:1 #BE185D);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #BE185D, stop:1 #9D174D);
            }}
        """


class ChildInfoEditorStyles:
    @staticmethod
    def title_container():
        """Контейнер заголовка дитини"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(255, 152, 0, 0.15), 
                    stop:1 rgba(245, 124, 0, 0.1));
                border: 1px solid rgba(255, 152, 0, 0.3);
                border-radius: 16px;
                padding: 16px;
            }}
        """

    @staticmethod
    def section_title():
        """Заголовок секції"""
        return "color: white; font-weight: 700;"

    @staticmethod
    def section_subtitle():
        """Підзаголовок секції"""
        return "color: rgba(255, 255, 255, 0.8); font-size: 14px; margin-top: 4px;"

    @staticmethod
    def form_frame():
        """Фрейм форми дитини"""
        return f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 24px;
            }}
        """

    @staticmethod
    def field_label():
        """Підписи полів дитини"""
        return f"""
            QLabel {{
                color: white;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 8px 0px;
            }}
        """

    @staticmethod
    def gender_combo():
        """Комбобокс для вибору статі"""
        return f"""
            QComboBox {{
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                color: white;
                font-size: 15px;
                font-weight: 500;
            }}
            QComboBox:focus {{
                border: 2px solid #FF9800;
                background: rgba(255, 255, 255, 0.18);
            }}
            QComboBox::drop-down {{
                border: none;
                width: 32px;
                background: transparent;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: 6px solid transparent;
                border-top: 10px solid white;
                margin-right: 8px;
            }}
            QComboBox QAbstractItemView {{
                background: rgba(30, 27, 75, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                selection-background-color: #FF9800;
                padding: 8px;
            }}
        """

    @staticmethod
    def save_button():
        """Кнопка збереження дитини"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #FF9800, stop:1 #F57C00);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 16px 32px;
                font-weight: 700;
                font-size: 16px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #F57C00, stop:1 #E65100);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #E65100, stop:1 #D84315);
            }}
        """


class PasswordEditorStyles:
    @staticmethod
    def title_container():
        """Контейнер заголовка паролю"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(239, 68, 68, 0.15), 
                    stop:1 rgba(220, 38, 38, 0.1));
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 16px;
                padding: 16px;
            }}
        """

    @staticmethod
    def security_info():
        """Інформаційний блок про безпеку"""
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(59, 130, 246, 0.15), 
                    stop:1 rgba(29, 78, 216, 0.1));
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 16px;
                padding: 18px;
            }}
        """

    @staticmethod
    def security_title():
        """Заголовок безпеки"""
        return "color: white; font-weight: 700; font-size: 16px; margin-bottom: 8px;"

    @staticmethod
    def security_tips():
        """Поради безпеки"""
        return "color: rgba(255, 255, 255, 0.9); font-size: 14px; line-height: 1.4;"

    @staticmethod
    def form_frame():
        """Фрейм форми паролю"""
        return f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 24px;
            }}
        """

    @staticmethod
    def field_label():
        """Підписи полів паролю"""
        return f"""
            QLabel {{
                color: white;
                font-size: 16px;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 8px 0px;
            }}
        """

    @staticmethod
    def password_input():
        """Поля введення паролю"""
        return f"""
            QLineEdit {{
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                color: white;
                font-size: 15px;
                font-weight: 500;
            }}
            QLineEdit:focus {{
                border: 2px solid #EF4444;
                background: rgba(255, 255, 255, 0.18);
            }}
            QLineEdit::placeholder {{
                color: rgba(255, 255, 255, 0.5);
            }}
        """

    @staticmethod
    def change_button():
        """Кнопка зміни паролю"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #EF4444, stop:1 #DC2626);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 16px 32px;
                font-weight: 700;
                font-size: 16px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #DC2626, stop:1 #B91C1C);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #B91C1C, stop:1 #991B1B);
            }}
        """