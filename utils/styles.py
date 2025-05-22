class Styles:
    COLORS = {
        'primary': '#FF8C00',
        'background': '#121212',
        'surface': '#222222',
        'surface_variant': '#333333',
        'text_primary': '#FFFFFF',
        'text_secondary': '#AAAAAA',
        'success': '#4CAF50',
        'error': '#F44336',
        'warning': '#FF9800',
        'info': '#2196F3'
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
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: #FFA500;
            }}
        """

    @staticmethod
    def button_secondary():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['surface_variant']};
                color: white;
                border-radius: 8px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: #444444;
            }}
        """

    @staticmethod
    def card():
        return f"""
            background-color: {Styles.COLORS['surface']};
            border-radius: 15px;
            padding: 15px;
        """

    @staticmethod
    def list_widget():
        return f"""
            QListWidget {{
                background-color: {Styles.COLORS['surface_variant']};
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #444444;
            }}
            QListWidget::item:selected {{
                background-color: {Styles.COLORS['primary']};
            }}
        """