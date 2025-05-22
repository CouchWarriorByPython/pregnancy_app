class Styles:
    COLORS = {
        'primary': '#FF8C00',
        'primary_hover': '#FFA500',
        'primary_pressed': '#E07800',
        'background': '#121212',
        'surface': '#222222',
        'surface_variant': '#333333',
        'surface_hover': '#2A2A2A',
        'text_primary': '#FFFFFF',
        'text_secondary': '#AAAAAA',
        'text_accent': '#FF8C00',
        'success': '#4CAF50',
        'success_hover': '#388E3C',
        'error': '#F44336',
        'error_hover': '#D32F2F',
        'warning': '#FF9800',
        'info': '#2196F3',
        'border': '#444444',
        'border_hover': '#555555'
    }

    @staticmethod
    def input_field():
        return f"""
            background-color: {Styles.COLORS['surface_variant']};
            border: none;
            border-radius: 8px;
            padding: 8px;
            color: {Styles.COLORS['text_primary']};
            min-height: 30px;
        """

    @staticmethod
    def button_primary():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['primary']};
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: {Styles.COLORS['primary_hover']};
            }}
            QPushButton:pressed {{
                background-color: {Styles.COLORS['primary_pressed']};
            }}
        """

    @staticmethod
    def button_secondary():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['surface_variant']};
                color: {Styles.COLORS['text_primary']};
                border: none;
                border-radius: 8px;
                padding: 8px;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: {Styles.COLORS['border_hover']};
            }}
        """

    @staticmethod
    def button_success():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['success']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
                min-height: 35px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Styles.COLORS['success_hover']};
            }}
        """

    @staticmethod
    def button_error():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['error']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
                min-height: 35px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Styles.COLORS['error_hover']};
            }}
        """

    @staticmethod
    def date_time_edit():
        return f"""
            QDateEdit, QTimeEdit {{
                background-color: {Styles.COLORS['surface_variant']};
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: {Styles.COLORS['text_primary']};
                min-height: 30px;
            }}
        """

    @staticmethod
    def spinbox():
        return f"""
            QSpinBox, QDoubleSpinBox {{
                background-color: {Styles.COLORS['surface_variant']};
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: {Styles.COLORS['text_primary']};
                min-height: 30px;
            }}
        """

    @staticmethod
    def checkbox():
        return f"""
            QCheckBox {{
                color: {Styles.COLORS['text_primary']};
                font-size: 14px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid {Styles.COLORS['border']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Styles.COLORS['success']};
                border: 2px solid {Styles.COLORS['success']};
            }}
        """

    @staticmethod
    def combobox():
        return f"""
            QComboBox {{
                background-color: {Styles.COLORS['surface_variant']};
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: {Styles.COLORS['text_primary']};
                min-height: 30px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Styles.COLORS['surface_variant']};
                border: 1px solid {Styles.COLORS['border']};
                color: {Styles.COLORS['text_primary']};
                selection-background-color: {Styles.COLORS['primary']};
            }}
        """

    @staticmethod
    def list_widget():
        return f"""
            QListWidget {{
                background-color: {Styles.COLORS['surface_variant']};
                border: none;
                border-radius: 5px;
                color: {Styles.COLORS['text_primary']};
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {Styles.COLORS['border']};
            }}
            QListWidget::item:selected {{
                background-color: {Styles.COLORS['primary']};
            }}
        """

    @staticmethod
    def frame():
        return f"""
            QFrame {{
                background-color: {Styles.COLORS['surface']};
                border-radius: 10px;
                padding: 10px;
            }}
        """

    @staticmethod
    def card_frame():
        return f"""
            background-color: {Styles.COLORS['surface']};
            border-radius: 15px;
            padding: 15px;
        """

    @staticmethod
    def header():
        return f"""
            background-color: {Styles.COLORS['background']};
            min-height: 60px;
        """

    @staticmethod
    def tab_button():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['background']};
                color: {Styles.COLORS['text_secondary']};
                border: none;
                font-size: 14px;
                padding: 10px;
                text-align: center;
            }}
            QPushButton:checked {{
                background-color: {Styles.COLORS['surface']};
                color: {Styles.COLORS['primary']};
                font-weight: bold;
            }}
            QPushButton:hover:!checked {{
                background-color: #1A1A1A;
            }}
        """

    @staticmethod
    def scroll_area():
        return "border: none;"

    @staticmethod
    def text_primary():
        return f"color: {Styles.COLORS['text_primary']};"

    @staticmethod
    def text_secondary():
        return f"color: {Styles.COLORS['text_secondary']};"

    @staticmethod
    def text_accent():
        return f"color: {Styles.COLORS['text_accent']};"