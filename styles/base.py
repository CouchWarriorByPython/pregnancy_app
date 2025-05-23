"""
Базові стилі та кольори для всього додатку
"""


class Colors:
    # Основні кольори
    PRIMARY = '#FF8C00'
    PRIMARY_HOVER = '#FFA500'
    PRIMARY_PRESSED = '#E07800'

    # Фон та поверхні
    BACKGROUND = '#121212'
    SURFACE = '#222222'
    SURFACE_VARIANT = '#333333'
    SURFACE_HOVER = '#2A2A2A'

    # Текст
    TEXT_PRIMARY = '#FFFFFF'
    TEXT_SECONDARY = '#AAAAAA'
    TEXT_ACCENT = '#FF8C00'

    # Стани
    SUCCESS = '#4CAF50'
    SUCCESS_HOVER = '#388E3C'
    ERROR = '#F44336'
    ERROR_HOVER = '#D32F2F'
    WARNING = '#FF9800'
    INFO = '#2196F3'

    # Обводки
    BORDER = '#444444'
    BORDER_HOVER = '#555555'


class BaseStyles:
    @staticmethod
    def lighten_color(hex_color, factor=0.2):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"#{min(int(r + (255 - r) * factor), 255):02x}{min(int(g + (255 - g) * factor), 255):02x}{min(int(b + (255 - b) * factor), 255):02x}"

    @staticmethod
    def darken_color(hex_color, factor=0.2):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"#{max(int(r * (1 - factor)), 0):02x}{max(int(g * (1 - factor)), 0):02x}{max(int(b * (1 - factor)), 0):02x}"

    @staticmethod
    def button_primary():
        return f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.PRIMARY_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: #777777;
                color: #AAAAAA;
            }}
        """

    @staticmethod
    def button_secondary():
        return f"""
            QPushButton {{
                background-color: {Colors.SURFACE_VARIANT};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BORDER_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {BaseStyles.darken_color(Colors.BORDER_HOVER)};
            }}
        """

    @staticmethod
    def button_success():
        return f"""
            QPushButton {{
                background-color: {Colors.SUCCESS};
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: {Colors.SUCCESS_HOVER};
            }}
        """

    @staticmethod
    def button_error():
        return f"""
            QPushButton {{
                background-color: {Colors.ERROR};
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: {Colors.ERROR_HOVER};
            }}
        """

    @staticmethod
    def input_field():
        return f"""
            QLineEdit, QTextEdit {{
                background-color: {Colors.SURFACE_VARIANT};
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: {Colors.TEXT_PRIMARY};
                min-height: 30px;
            }}
        """

    @staticmethod
    def form_controls():
        return f"""
            QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
                background-color: {Colors.SURFACE_VARIANT};
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: {Colors.TEXT_PRIMARY};
                min-height: 30px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.SURFACE_VARIANT};
                border: 1px solid {Colors.BORDER};
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def checkbox():
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid {Colors.BORDER};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Colors.SUCCESS};
                border: 2px solid {Colors.SUCCESS};
            }}
        """

    @staticmethod
    def radio_button():
        return f"""
            QRadioButton {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid {Colors.BORDER};
            }}
            QRadioButton::indicator:checked {{
                background-color: {Colors.PRIMARY};
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def card_frame():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 15px;
            }}
        """

    @staticmethod
    def list_widget():
        return f"""
            QListWidget {{
                background-color: {Colors.SURFACE_VARIANT};
                border: none;
                border-radius: 5px;
                color: {Colors.TEXT_PRIMARY};
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {Colors.BORDER};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def scroll_area():
        return "border: none;"

    @staticmethod
    def header():
        return f"background-color: {Colors.BACKGROUND}; min-height: 60px;"

    @staticmethod
    def text_primary():
        return f"color: {Colors.TEXT_PRIMARY};"

    @staticmethod
    def text_secondary():
        return f"color: {Colors.TEXT_SECONDARY};"

    @staticmethod
    def text_accent():
        return f"color: {Colors.TEXT_ACCENT};"

    @staticmethod
    def dialog_base():
        return f"QDialog {{ background-color: {Colors.BACKGROUND}; color: {Colors.TEXT_PRIMARY}; }}"