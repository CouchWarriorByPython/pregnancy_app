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
                background: transparent;
                color: white;
                font-size: 26px;
                font-weight: 700;
                margin-bottom: 20px;
                border: none;
                padding: 0px;
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
                background: transparent;
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 8px;
                border: none;
                padding: 0px;
            }}
        """

    @staticmethod
    def onboarding_input():
        """Поля введення в онбордингу"""
        return f"""
            QLineEdit {{
                background: transparent;
                border: none;
                border-bottom: 2px solid {Colors.PRIMARY};
                border-radius: 0px;
                padding: 8px 4px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                min-height: 20px;
                selection-background-color: {Colors.ACCENT};
            }}
            QLineEdit:focus {{
                border-bottom: 2.5px solid {Colors.ACCENT};
                background: transparent;
            }}
            QLineEdit:hover {{
                border-bottom-color: {Colors.ACCENT};
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_SECONDARY};
                font-style: italic;
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
                padding: 12px 0px;
                spacing: 16px;
                background: transparent;
                border: none;
                margin: 4px 0;
            }}
            QRadioButton:hover {{
                color: {Colors.ACCENT};
            }}
            QRadioButton::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 12px;
                border: 2px solid {Colors.BORDER};
                background: transparent;
            }}
            QRadioButton::indicator:checked {{
                background: {Colors.ACCENT};
                border: 3px solid white;
            }}
            QRadioButton::indicator:hover {{
                border-color: {Colors.ACCENT};
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
                padding: 12px 0px;
                spacing: 16px;
                background: transparent;
                border: none;
                margin: 4px 0;
            }}
            QCheckBox:hover {{
                color: {Colors.ACCENT};
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 6px;
                border: 2px solid {Colors.BORDER};
                background: transparent;
            }}
            QCheckBox::indicator:checked {{
                background: {Colors.ACCENT};
                border: 3px solid white;
            }}
            QCheckBox::indicator:hover {{
                border-color: {Colors.ACCENT};
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
    def date_field_clean():
        """Абсолютно чисті поля дати без жодних візуальних елементів"""
        return """
            QDateEdit {
                background: transparent;
                color: white;
                border: none;
                border-bottom: 2px solid rgba(139, 92, 246, 1);
                border-radius: 0px;
                padding: 4px 4px 4px 4px;
                font-size: 16px;
                min-height: 20px;
            }
            QDateEdit:focus {
                border-bottom: 2px solid rgba(236, 72, 153, 1);
                background: transparent;
            }
            
            /* ПОВНЕ приховування всіх можливих елементів */
            QDateEdit::drop-down {
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QDateEdit::down-arrow {
                image: none !important;
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
            }
            QDateEdit::up-button, QDateEdit::down-button {
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
            }
            QDateEdit QAbstractSpinBox::up-button, QDateEdit QAbstractSpinBox::down-button {
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
            }
            QDateEdit QAbstractSpinBox::up-arrow, QDateEdit QAbstractSpinBox::down-arrow {
                image: none !important;
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
            }
            QDateEdit::section {
                background: transparent;
                color: white;
                border: none;
                selection-background-color: transparent;
                selection-color: white;
            }
            QDateEdit::separator {
                color: white;
                background: transparent;
                border: none;
            }
        """

    @staticmethod
    def elegant_input():
        """Елегантні поля вводу з підкресленням"""
        return """
            QLineEdit, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background: transparent;
                color: white;
                border: none;
                border-bottom: 2px solid rgba(139, 92, 246, 1);
                border-radius: 0px;
                padding: 4px 4px 4px 4px;
                font-size: 16px;
                min-height: 20px;
            }
            QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border-bottom: 2px solid rgba(236, 72, 153, 1);
                background: transparent;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
            
            /* Повне приховування всіх кнопок та елементів QDateEdit */
            QDateEdit::drop-down, QTimeEdit::drop-down, QComboBox::drop-down {
                width: 0px;
                height: 0px;
                border: none;
                background: transparent;
                subcontrol-position: right;
                subcontrol-origin: margin;
                padding: 0px;
                margin: 0px;
            }
            QDateEdit::down-arrow, QTimeEdit::down-arrow, QComboBox::down-arrow {
                image: none;
                width: 0px;
                height: 0px;
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            
            /* Агресивне приховування всіх кнопок спінерів */
            QDateEdit QAbstractSpinBox::up-button, QDateEdit QAbstractSpinBox::down-button,
            QTimeEdit QAbstractSpinBox::up-button, QTimeEdit QAbstractSpinBox::down-button {
                width: 0px;
                height: 0px;
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            
            /* Приховування секцій та сепараторів */
            QDateEdit::section {
                background: transparent;
                color: white;
                border: none;
                padding: 0px;
                margin: 0px;
                spacing: 0px;
            }
            QDateEdit::section:selected {
                background: transparent;
                color: white;
            }
            QDateEdit::separator {
                width: 0px;
                height: 0px;
                background: transparent;
                color: transparent;
                image: none;
                border: none;
                margin: 0px;
                padding: 0px;
            }
            
            /* Приховування всіх можливих кнопок */
            QDateEdit::up-button, QDateEdit::down-button,
            QDateEdit QAbstractSpinBox::up-arrow, QDateEdit QAbstractSpinBox::down-arrow {
                width: 0px;
                height: 0px;
                border: none;
                background: transparent;
                image: none;
                padding: 0px;
                margin: 0px;
            }
            
            QSpinBox::up-button, QSpinBox::down-button,
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                width: 0px;
                background: transparent;
                border: none;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow,
            QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
                image: none;
                width: 0px;
                height: 0px;
            }
        """

    @staticmethod
    def user_info_field_label():
        """Лейбли полів для екрану "Інформація про вас" """
        return f"""
            QLabel {{
                background-color: transparent;
                color: {Colors.TEXT_PRIMARY};
                font-size: 15px;
                font-weight: 600;
                padding: 0px;
                margin: 0px;
                line-height: 1.2;
                min-height: 24px;
                max-height: 24px;
                border: none;
            }}
        """

    @staticmethod
    def user_info_group_label():
        """Заголовки груп для екрану "Інформація про вас" (без фону)"""
        return f"""
            QLabel {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 700;
                padding: 8px 0px;
                margin: 0px;
                line-height: 1.3;
                min-height: 20px;
                max-height: 32px;
            }}
        """

    @staticmethod
    def user_info_subtitle():
        """Підзаголовок для екрану "Інформація про вас" """
        return f"""
            QLabel {{
                background-color: transparent;
                color: {Colors.TEXT_SECONDARY};
                font-size: 16px;
                font-weight: 400;
                padding: 0px;
                margin: 0px;
                line-height: 1.3;
                min-height: 20px;
                max-height: 24px;
                border: none;
            }}
        """

    @staticmethod
    def subtitle():
        """Підзаголовок/пояснення (без фону)"""
        return f"""
            QLabel {{
                background: transparent;
                font-size: 16px;
                color: #B0B0B0;
                margin-bottom: 12px;
                border: none;
                padding: 0px;
            }}
        """

    @staticmethod
    def hint():
        """Підказка під полем (курсив, покращений контраст)"""
        return f"""
            QLabel {{
                background: transparent;
                font-size: 13px;
                color: #CCCCCC;
                margin-top: 4px;
                margin-bottom: 0px;
                font-style: italic;
                border: none;
                padding: 0px;
            }}
        """

    @staticmethod
    def checkbox_style():
        """Стиль для чекбокса (ідентичний до радіокнопок)"""
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                padding: 12px 0px;
                spacing: 16px;
                background: transparent;
                border: none;
                margin: 4px 0;
            }}
            QCheckBox:hover {{
                color: {Colors.ACCENT};
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 12px;
                border: 2px solid {Colors.BORDER};
                background: transparent;
            }}
            QCheckBox::indicator:checked {{
                background: {Colors.ACCENT};
                border: 3px solid white;
            }}
            QCheckBox::indicator:hover {{
                border-color: {Colors.ACCENT};
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