"""
Стилі для екранів онбордингу
"""

from ..base import Colors


class OnboardingScreenStyles:
    @staticmethod
    def main_container():
        """Основний контейнер онбордингу"""
        return f"""
            QWidget {{
                background: {Colors.BACKGROUND_GRADIENT};
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def step_title():
        """Заголовок кроку онбордингу"""
        return f"""
            QLabel {{
                color: white;
                font-size: 26px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 20px;
            }}
        """

    @staticmethod
    def form_section():
        """Секція форми онбордингу"""
        return f"""
            QWidget {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 24px;
                margin: 12px;
            }}
        """

    @staticmethod
    def field_label():
        """Підпис поля в онбордингу"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 8px;
            }}
        """

    @staticmethod
    def onboarding_input():
        """Поля введення в онбордингу"""
        return f"""
            QLineEdit {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 16px 20px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 500;
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.PRIMARY};
                background: rgba(255, 255, 255, 0.12);
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_SECONDARY};
                font-weight: 400;
            }}
        """

    @staticmethod
    def onboarding_button():
        """Кнопки онбордингу"""
        return f"""
            QPushButton {{
                background: {Colors.PRIMARY_GRADIENT};
                color: white;
                border: none;
                border-radius: 20px;
                padding: 18px 32px;
                font-weight: 700;
                font-size: 16px;
                min-height: 20px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #DB2777);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6D28D9, stop:1 #BE185D);
            }}
        """

    @staticmethod
    def gender_section():
        """Секція вибору статі дитини"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(236, 72, 153, 0.1), stop:1 rgba(219, 39, 119, 0.05));
                border: 1px solid rgba(236, 72, 153, 0.3);
                border-radius: 20px;
                padding: 24px;
                margin: 12px 0;
            }}
        """

    @staticmethod
    def gender_radio():
        """Радіо кнопки для статі"""
        return f"""
            QRadioButton {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                padding: 16px;
                spacing: 16px;
                border-radius: 12px;
                margin: 4px 0;
            }}
            QRadioButton:hover {{
                background: rgba(255, 255, 255, 0.05);
            }}
            QRadioButton::indicator {{
                width: 28px;
                height: 28px;
                border-radius: 14px;
                border: 2px solid {Colors.GLASS_BORDER};
                background: {Colors.GLASS_SURFACE};
            }}
            QRadioButton::indicator:checked {{
                background: {Colors.PRIMARY_GRADIENT};
                border: 3px solid white;
            }}
        """

    @staticmethod
    def first_labour_checkbox():
        """Чекбокс для перших пологів"""
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                padding: 20px;
                spacing: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(16, 185, 129, 0.1), stop:1 rgba(5, 150, 105, 0.05));
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 16px;
                margin: 12px 0;
            }}
            QCheckBox:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(16, 185, 129, 0.15), stop:1 rgba(5, 150, 105, 0.1));
            }}
            QCheckBox::indicator {{
                width: 28px;
                height: 28px;
                border-radius: 8px;
                border: 2px solid {Colors.GLASS_BORDER};
                background: {Colors.GLASS_SURFACE};
            }}
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10B981, stop:1 #059669);
                border: 3px solid white;
            }}
        """

    @staticmethod
    def pregnancy_info_date_edit():
        """Поля дати в екрані інформації про вагітність"""
        return f"""
            QDateEdit {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 16px 20px;
                color: white;
                font-size: 14px;
                min-height: 20px;
            }}
            QDateEdit:focus {{
                border: 2px solid #8B5CF6;
                background: rgba(255, 255, 255, 0.12);
            }}
            QDateEdit::drop-down {{
                border: none;
                width: 30px;
                background: transparent;
            }}
            QDateEdit::down-arrow {{
                image: none;
                border: 5px solid transparent;
                border-top: 8px solid white;
                margin-right: 10px;
            }}
            QCalendarWidget {{
                background-color: #1E1B4B;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
            }}
            QCalendarWidget QToolButton {{
                color: white;
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 4px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QCalendarWidget QMenu {{
                background-color: #1E1B4B;
                color: white;
            }}
            QCalendarWidget QSpinBox {{
                background-color: transparent;
                color: white;
                border: none;
            }}
            QCalendarWidget QAbstractItemView {{
                background-color: #1E1B4B;
                color: white;
                selection-background-color: #8B5CF6;
                selection-color: white;
            }}
        """

    @staticmethod
    def pregnancy_info_date_edit():
        """Поля дати в екрані інформації про вагітність"""
        return f"""
            QDateEdit {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 16px 20px;
                color: white;
                font-size: 14px;
                min-height: 20px;
            }}
            QDateEdit:focus {{
                border: 2px solid #8B5CF6;
                background: rgba(255, 255, 255, 0.12);
            }}
            QDateEdit::drop-down {{
                border: none;
                width: 30px;
                background: transparent;
            }}
            QDateEdit::down-arrow {{
                image: none;
                border: 5px solid transparent;
                border-top: 8px solid white;
                margin-right: 10px;
            }}
            QCalendarWidget {{
                background-color: #1E1B4B;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
            }}
            QCalendarWidget QToolButton {{
                color: white;
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 4px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QCalendarWidget QMenu {{
                background-color: #1E1B4B;
                color: white;
            }}
            QCalendarWidget QSpinBox {{
                background-color: transparent;
                color: white;
                border: none;
            }}
            QCalendarWidget QAbstractItemView {{
                background-color: #1E1B4B;
                color: white;
                selection-background-color: #8B5CF6;
                selection-color: white;
            }}
        """

    @staticmethod
    def welcome_login_button():
        """Кнопка входу на екрані привітання"""
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid #FF8C00;
                color: #FF8C00;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 140, 0, 0.2);
            }}
        """