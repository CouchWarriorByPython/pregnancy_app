"""
Базові стилі та кольори для всього додатку
"""


class Colors:
    # Градієнтні кольори
    PRIMARY_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #EC4899)"
    SECONDARY_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #EC4899, stop:1 #F97316)"
    ACCENT_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366F1, stop:1 #8B5CF6)"
    BACKGROUND_GRADIENT = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1E1B4B, stop:1 #312E81)"

    # Основні кольори
    PRIMARY = '#8B5CF6'
    PRIMARY_HOVER = '#7C3AED'
    PRIMARY_PRESSED = '#6D28D9'

    SECONDARY = '#EC4899'
    SECONDARY_HOVER = '#DB2777'
    SECONDARY_PRESSED = '#BE185D'

    # Фон та поверхні
    BACKGROUND = '#0F0F23'
    SURFACE = 'rgba(255, 255, 255, 0.1)'
    SURFACE_VARIANT = 'rgba(255, 255, 255, 0.15)'
    SURFACE_HOVER = 'rgba(255, 255, 255, 0.2)'
    GLASS_SURFACE = 'rgba(255, 255, 255, 0.08)'
    GLASS_BORDER = 'rgba(255, 255, 255, 0.2)'

    # Текст
    TEXT_PRIMARY = '#FFFFFF'
    TEXT_SECONDARY = 'rgba(255, 255, 255, 0.7)'
    TEXT_ACCENT = '#8B5CF6'

    # Стани
    SUCCESS = '#10B981'
    SUCCESS_HOVER = '#059669'
    ERROR = '#EF4444'
    ERROR_HOVER = '#DC2626'
    WARNING = '#F59E0B'
    INFO = '#3B82F6'

    # Обводки
    BORDER = 'rgba(255, 255, 255, 0.1)'
    BORDER_HOVER = 'rgba(255, 255, 255, 0.3)'


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
                background: {Colors.PRIMARY_GRADIENT};
                color: white;
                border: none;
                border-radius: 20px;
                padding: 15px 25px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #DB2777);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6D28D9, stop:1 #BE185D);
            }}
            QPushButton:disabled {{
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.4);
            }}
        """

    @staticmethod
    def button_secondary():
        return f"""
            QPushButton {{
                background: {Colors.SURFACE};
                color: white;
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 500;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: {Colors.SURFACE_HOVER};
                border: 1px solid rgba(255, 255, 255, 0.4);
            }}
            QPushButton:pressed {{
                background: rgba(255, 255, 255, 0.25);
            }}
        """

    @staticmethod
    def button_success():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10B981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 15px 25px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #059669, stop:1 #047857);
            }}
        """

    @staticmethod
    def button_error():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #EF4444, stop:1 #DC2626);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 15px 25px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #DC2626, stop:1 #B91C1C);
            }}
        """

    @staticmethod
    def input_field():
        return f"""
            QLineEdit, QTextEdit {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 16px 20px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                min-height: 20px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 2px solid {Colors.PRIMARY};
                background: rgba(255, 255, 255, 0.12);
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_SECONDARY};
            }}
        """

    @staticmethod
    def form_controls():
        return f"""
            QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 16px 20px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                min-height: 20px;
            }}
            QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
                border: 2px solid {Colors.PRIMARY};
                background: rgba(255, 255, 255, 0.12);
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
                background: transparent;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: 5px solid transparent;
                border-top: 8px solid {Colors.TEXT_PRIMARY};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background: {Colors.SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 12px;
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.PRIMARY};
                padding: 8px;
            }}
            QSpinBox::up-button, QSpinBox::down-button,
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
                background: transparent;
                border: none;
                width: 20px;
            }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                image: none;
                border: 4px solid transparent;
                border-bottom: 6px solid {Colors.TEXT_PRIMARY};
            }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                image: none;
                border: 4px solid transparent;
                border-top: 6px solid {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def checkbox():
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 500;
                spacing: 12px;
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 8px;
                border: 2px solid {Colors.GLASS_BORDER};
                background: {Colors.GLASS_SURFACE};
            }}
            QCheckBox::indicator:checked {{
                background: {Colors.PRIMARY_GRADIENT};
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def radio_button():
        return f"""
            QRadioButton {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 500;
                spacing: 12px;
            }}
            QRadioButton::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 12px;
                border: 2px solid {Colors.GLASS_BORDER};
                background: {Colors.GLASS_SURFACE};
            }}
            QRadioButton::indicator:checked {{
                background: {Colors.PRIMARY_GRADIENT};
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def card_frame():
        return f"""
            QFrame {{
                background: {Colors.SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 24px;
            }}
        """

    @staticmethod
    def glass_card():
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 20px;
            }}
        """

    @staticmethod
    def list_widget():
        return f"""
            QListWidget {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                color: {Colors.TEXT_PRIMARY};
                padding: 8px;
            }}
            QListWidget::item {{
                padding: 16px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin: 4px;
            }}
            QListWidget::item:selected {{
                background: {Colors.PRIMARY_GRADIENT};
                border: none;
            }}
            QListWidget::item:hover {{
                background: rgba(255, 255, 255, 0.1);
            }}
        """

    @staticmethod
    def scroll_area():
        return f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {Colors.PRIMARY};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {Colors.PRIMARY_HOVER};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """

    @staticmethod
    def header():
        return f"""
            QWidget {{
                background: {Colors.BACKGROUND_GRADIENT};
                border-bottom: 1px solid {Colors.GLASS_BORDER};
                min-height: 80px;
            }}
        """

    @staticmethod
    def text_primary():
        return f"color: {Colors.TEXT_PRIMARY}; font-weight: 500;"

    @staticmethod
    def text_secondary():
        return f"color: {Colors.TEXT_SECONDARY}; font-weight: 400;"

    @staticmethod
    def text_accent():
        return f"color: {Colors.TEXT_ACCENT}; font-weight: 600;"

    @staticmethod
    def dialog_base():
        return f"""
            QDialog {{
                background: {Colors.BACKGROUND_GRADIENT};
                color: {Colors.TEXT_PRIMARY};
                border-radius: 20px;
            }}
        """

    @staticmethod
    def progress_bar():
        return f"""
            QProgressBar {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                height: 24px;
                text-align: center;
                color: white;
                font-weight: 600;
            }}
            QProgressBar::chunk {{
                background: {Colors.PRIMARY_GRADIENT};
                border-radius: 12px;
            }}
        """

    @staticmethod
    def tab_widget():
        return f"""
            QTabWidget::pane {{
                border: 1px solid {Colors.GLASS_BORDER};
                background: {Colors.GLASS_SURFACE};
                border-radius: 16px;
            }}
            QTabBar::tab {{
                background: rgba(255, 255, 255, 0.05);
                color: {Colors.TEXT_SECONDARY};
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background: {Colors.PRIMARY_GRADIENT};
                color: white;
                font-weight: 600;
            }}
            QTabBar::tab:hover:!selected {{
                background: rgba(255, 255, 255, 0.1);
            }}
        """