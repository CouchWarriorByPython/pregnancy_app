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
    def button_circular(color, size=60):
        return f"""
            QPushButton {{
                background-color: {color};
                border-radius: {size//2}px;
                font-weight: bold;
                font-size: 18px;
                color: white;
                text-align: center;
            }}
            QPushButton:checked {{
                background-color: {Styles.COLORS['primary']};
                color: white;
            }}
            QPushButton:hover:!checked {{
                background-color: {Styles._lighten_color(color)};
            }}
        """

    @staticmethod
    def button_nav_arrow():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['surface_variant']};
                border-radius: 22px;
                font-weight: bold;
                color: #DDDDDD;
                font-size: 18px;
            }}
            QPushButton:disabled {{
                background-color: {Styles.COLORS['surface']};
                color: {Styles.COLORS['border']};
            }}
            QPushButton:hover:enabled {{
                background-color: {Styles.COLORS['border']};
            }}
            QPushButton:pressed {{
                background-color: {Styles.COLORS['border_hover']};
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
    def tool_card():
        return f"""
            QFrame {{
                background-color: {Styles.COLORS['surface']};
                border-radius: 15px;
                min-height: 150px;
            }}
            QLabel#titleLabel {{
                font-weight: bold;
            }}
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
    def progress_bar():
        return f"""
            background-color: {Styles.COLORS['surface_variant']};
            border-radius: 10px;
            padding: 0px;
            text-align: left;
        """

    @staticmethod
    def splitter():
        return f"""
            QSplitter::handle {{
                background-color: {Styles.COLORS['border']};
            }}
        """

    @staticmethod
    def scroll_area():
        return "border: none;"

    @staticmethod
    def nav_bottom():
        return f"""
            background-color: {Styles.COLORS['background']};
        """

    @staticmethod
    def nav_button():
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: #888888;
                padding-top: 5px;
                font-size: 10px;
            }}
            QPushButton:checked {{
                color: {Styles.COLORS['primary']};
            }}
            QPushButton:hover {{
                color: #AAAAAA;
            }}
        """

    @staticmethod
    def form_container():
        return f"""
            background-color: {Styles.COLORS['surface']};
            border-radius: 10px;
            padding: 10px;
        """

    @staticmethod
    def slider():
        return f"""
            QSlider::groove:horizontal {{
                height: 8px;
                background: {Styles.COLORS['border']};
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {Styles.COLORS['primary']};
                border: 1px solid {Styles.COLORS['primary']};
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{
                background: {Styles.COLORS['primary']};
                border-radius: 4px;
            }}
        """

    @staticmethod
    def calendar():
        return f"""
            QCalendarWidget {{
                background-color: {Styles.COLORS['background']};
            }}
            QCalendarWidget QToolButton {{
                color: {Styles.COLORS['text_primary']};
                background-color: {Styles.COLORS['surface_variant']};
                border-radius: 5px;
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                color: {Styles.COLORS['text_primary']};
                background-color: {Styles.COLORS['background']};
                selection-background-color: {Styles.COLORS['primary']};
                selection-color: white;
            }}
        """

    @staticmethod
    def radio_button():
        return f"""
            QRadioButton {{
                color: {Styles.COLORS['text_primary']};
                font-size: 14px;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid {Styles.COLORS['border']};
            }}
            QRadioButton::indicator:checked {{
                background-color: {Styles.COLORS['primary']};
                border: 2px solid {Styles.COLORS['primary']};
            }}
        """

    @staticmethod
    def text_primary():
        return f"color: {Styles.COLORS['text_primary']};"

    @staticmethod
    def text_secondary():
        return f"color: {Styles.COLORS['text_secondary']};"

    @staticmethod
    def text_accent():
        return f"color: {Styles.COLORS['text_accent']};"

    @staticmethod
    def _lighten_color(hex_color, factor=0.2):
        """Освітлює RGB колір на заданий фактор"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(int(r + (255 - r) * factor), 255)
        g = min(int(g + (255 - g) * factor), 255)
        b = min(int(b + (255 - b) * factor), 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def accent_title(color):
        return f"""
            color: {color};
            font-weight: bold;
        """

    @staticmethod
    def form_section():
        return f"""
            background-color: {Styles.COLORS['surface']};
            border-radius: 15px;
            padding: 15px;
        """