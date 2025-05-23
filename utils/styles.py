class Styles:
    COLORS = {
        'primary': '#FF8C00', 'primary_hover': '#FFA500', 'primary_pressed': '#E07800',
        'background': '#121212', 'surface': '#222222', 'surface_variant': '#333333', 'surface_hover': '#2A2A2A',
        'text_primary': '#FFFFFF', 'text_secondary': '#AAAAAA', 'text_accent': '#FF8C00',
        'success': '#4CAF50', 'success_hover': '#388E3C', 'error': '#F44336', 'error_hover': '#D32F2F',
        'warning': '#FF9800', 'info': '#2196F3', 'border': '#444444', 'border_hover': '#555555'
    }

    @staticmethod
    def _lighten_color(hex_color, factor=0.2):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"#{min(int(r + (255 - r) * factor), 255):02x}{min(int(g + (255 - g) * factor), 255):02x}{min(int(b + (255 - b) * factor), 255):02x}"

    @staticmethod
    def _darken_color(hex_color, factor=0.2):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"#{max(int(r * (1 - factor)), 0):02x}{max(int(g * (1 - factor)), 0):02x}{max(int(b * (1 - factor)), 0):02x}"

    @staticmethod
    def button(style_type='primary', color=None, hover_color=None, size='normal'):
        if color:
            bg_color = color
            hover_bg = hover_color or Styles._darken_color(color)
        else:
            colors = {
                'primary': (Styles.COLORS['primary'], Styles.COLORS['primary_hover']),
                'secondary': (Styles.COLORS['surface_variant'], Styles.COLORS['border_hover']),
                'success': (Styles.COLORS['success'], Styles.COLORS['success_hover']),
                'error': (Styles.COLORS['error'], Styles.COLORS['error_hover'])
            }
            bg_color, hover_bg = colors.get(style_type, colors['primary'])

        padding = "10px 20px" if size == 'large' else "8px"
        radius = "25px" if size == 'large' else ("15px" if style_type == 'primary' else "8px")
        height = "35px" if size != 'large' else "auto"

        return f"""
            QPushButton {{
                background-color: {bg_color}; color: white; border: none; border-radius: {radius};
                padding: {padding}; font-weight: bold; min-height: {height};
            }}
            QPushButton:hover {{ background-color: {hover_bg}; }}
            QPushButton:pressed {{ background-color: {Styles._darken_color(hover_bg)}; }}
            QPushButton:disabled {{ background-color: #777777; color: #AAAAAA; }}
        """

    @staticmethod
    def button_primary():
        return Styles.button('primary')

    @staticmethod
    def button_secondary():
        return Styles.button('secondary')

    @staticmethod
    def button_success():
        return Styles.button('success')

    @staticmethod
    def button_error():
        return Styles.button('error')

    @staticmethod
    def button_colored(color, hover_color=None):
        return Styles.button(color=color, hover_color=hover_color)

    @staticmethod
    def button_colored_large(color, hover_color=None):
        return Styles.button(color=color, hover_color=hover_color, size='large')

    @staticmethod
    def button_circular(color, size=60):
        return f"""
            QPushButton {{
                background-color: {color}; border-radius: {size // 2}px; font-weight: bold;
                font-size: 18px; color: white; text-align: center;
            }}
            QPushButton:checked {{ background-color: {Styles.COLORS['primary']}; color: white; }}
            QPushButton:hover:!checked {{ background-color: {Styles._lighten_color(color)}; }}
        """

    @staticmethod
    def button_nav_arrow():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['surface_variant']}; border-radius: 22px;
                font-weight: bold; color: #DDDDDD; font-size: 18px;
            }}
            QPushButton:disabled {{ background-color: {Styles.COLORS['surface']}; color: {Styles.COLORS['border']}; }}
            QPushButton:hover:enabled {{ background-color: {Styles.COLORS['border']}; }}
        """

    @staticmethod
    def input_field():
        return f"""
            background-color: {Styles.COLORS['surface_variant']}; border: none; border-radius: 8px;
            padding: 8px; color: {Styles.COLORS['text_primary']}; min-height: 30px;
        """

    @staticmethod
    def form_control():
        return f"""
            QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
                background-color: {Styles.COLORS['surface_variant']}; border: none; border-radius: 8px;
                padding: 8px; color: {Styles.COLORS['text_primary']}; min-height: 30px;
            }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox QAbstractItemView {{
                background-color: {Styles.COLORS['surface_variant']}; border: 1px solid {Styles.COLORS['border']};
                color: {Styles.COLORS['text_primary']}; selection-background-color: {Styles.COLORS['primary']};
            }}
        """

    @staticmethod
    def date_time_edit():
        return Styles.form_control()

    @staticmethod
    def spinbox():
        return Styles.form_control()

    @staticmethod
    def combobox():
        return Styles.form_control()

    @staticmethod
    def checkbox(border_color=None, checked_color=None):
        border = border_color or Styles.COLORS['border']
        checked = checked_color or Styles.COLORS['success']
        return f"""
            QCheckBox {{ color: {Styles.COLORS['text_primary']}; font-size: 14px; spacing: 5px; }}
            QCheckBox::indicator {{ width: 20px; height: 20px; border-radius: 4px; border: 2px solid {border}; }}
            QCheckBox::indicator:checked {{ background-color: {checked}; border: 2px solid {checked}; }}
        """

    @staticmethod
    def checkbox_custom(border_color, checked_color):
        return Styles.checkbox(border_color, checked_color)

    @staticmethod
    def radio_button():
        return f"""
            QRadioButton {{ color: {Styles.COLORS['text_primary']}; font-size: 14px; }}
            QRadioButton::indicator {{ width: 20px; height: 20px; border-radius: 10px; border: 2px solid {Styles.COLORS['border']}; }}
            QRadioButton::indicator:checked {{ background-color: {Styles.COLORS['primary']}; border: 2px solid {Styles.COLORS['primary']}; }}
        """

    @staticmethod
    def text_style(color=None):
        text_color = color or Styles.COLORS['text_primary']
        return f"color: {text_color};"

    @staticmethod
    def text_primary():
        return Styles.text_style()

    @staticmethod
    def text_secondary():
        return Styles.text_style(Styles.COLORS['text_secondary'])

    @staticmethod
    def text_accent():
        return Styles.text_style(Styles.COLORS['text_accent'])

    @staticmethod
    def title_colored(color, size=22):
        return f"color: {color}; font-size: {size}px; font-weight: bold;"

    @staticmethod
    def container(rounded=True, padding="15px"):
        radius = "15px" if rounded else "0px"
        return f"background-color: {Styles.COLORS['surface']}; border-radius: {radius}; padding: {padding};"

    @staticmethod
    def card_frame():
        return Styles.container()

    @staticmethod
    def frame():
        return Styles.container(padding="10px")

    @staticmethod
    def form_container():
        return Styles.container(padding="10px")

    @staticmethod
    def card_colored(color):
        return f"{Styles.container()} QLabel {{ color: {color}; }}"

    @staticmethod
    def list_widget():
        return f"""
            QListWidget {{
                background-color: {Styles.COLORS['surface_variant']}; border: none; border-radius: 5px;
                color: {Styles.COLORS['text_primary']}; padding: 5px;
            }}
            QListWidget::item {{ padding: 8px; border-bottom: 1px solid {Styles.COLORS['border']}; }}
            QListWidget::item:selected {{ background-color: {Styles.COLORS['primary']}; }}
        """

    @staticmethod
    def tab_button():
        return f"""
            QPushButton {{
                background-color: {Styles.COLORS['background']}; color: {Styles.COLORS['text_secondary']};
                border: none; font-size: 14px; padding: 10px; text-align: center;
            }}
            QPushButton:checked {{
                background-color: {Styles.COLORS['surface']}; color: {Styles.COLORS['primary']}; font-weight: bold;
            }}
            QPushButton:hover:!checked {{ background-color: #1A1A1A; }}
        """

    @staticmethod
    def settings_tab_button():
        return Styles.tab_button()

    @staticmethod
    def progress_bar():
        return f"background-color: {Styles.COLORS['surface_variant']}; border-radius: 10px; padding: 0px; text-align: left;"

    @staticmethod
    def progress_bar_dynamic(progress_percent):
        return f"""
            background-color: {Styles.COLORS['surface_variant']}; border-radius: 10px; padding: 0px; text-align: left;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {Styles.COLORS['primary']}, stop:{progress_percent / 100} {Styles.COLORS['primary']},
                stop:{progress_percent / 100} {Styles.COLORS['surface_variant']}, stop:1 {Styles.COLORS['surface_variant']});
        """

    @staticmethod
    def header():
        return f"background-color: {Styles.COLORS['background']}; min-height: 60px;"

    @staticmethod
    def scroll_area():
        return "border: none;"

    @staticmethod
    def nav_bottom():
        return f"background-color: {Styles.COLORS['background']};"

    @staticmethod
    def nav_button():
        return f"""
            QPushButton {{
                background-color: transparent; border: none; color: #888888;
                padding-top: 5px; font-size: 10px;
            }}
            QPushButton:checked {{ color: {Styles.COLORS['primary']}; }}
            QPushButton:hover {{ color: #AAAAAA; }}
        """

    @staticmethod
    def slider():
        return f"""
            QSlider::groove:horizontal {{ height: 8px; background: {Styles.COLORS['border']}; border-radius: 4px; }}
            QSlider::handle:horizontal {{
                background: {Styles.COLORS['primary']}; border: 1px solid {Styles.COLORS['primary']};
                width: 18px; height: 18px; margin: -5px 0; border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{ background: {Styles.COLORS['primary']}; border-radius: 4px; }}
        """

    @staticmethod
    def calendar():
        return f"""
            QCalendarWidget {{ background-color: {Styles.COLORS['background']}; }}
            QCalendarWidget QToolButton {{
                color: {Styles.COLORS['text_primary']}; background-color: {Styles.COLORS['surface_variant']}; border-radius: 5px;
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                color: {Styles.COLORS['text_primary']}; background-color: {Styles.COLORS['background']};
                selection-background-color: {Styles.COLORS['primary']}; selection-color: white;
            }}
        """

    @staticmethod
    def dialog_base():
        return f"QDialog {{ background-color: {Styles.COLORS['background']}; color: {Styles.COLORS['text_primary']}; }}"

    @staticmethod
    def section_title():
        return "font-family: Arial; font-size: 16px; font-weight: bold;"

    @staticmethod
    def tab_widget_contraction():
        return f"""
            QTabWidget::pane {{ border: 1px solid {Styles.COLORS['surface_variant']}; background-color: {Styles.COLORS['surface']}; border-radius: 8px; }}
            QTabBar::tab {{ background-color: {Styles.COLORS['surface_variant']}; color: {Styles.COLORS['text_primary']}; padding: 8px 15px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }}
            QTabBar::tab:selected {{ background-color: #2196F3; color: white; }}
        """

    @staticmethod
    def progress_bar_contraction():
        return f"""
            QProgressBar {{ background-color: {Styles.COLORS['border']}; border-radius: 5px; height: 15px; }}
            QProgressBar::chunk {{ background-color: #2196F3; border-radius: 5px; }}
        """

    @staticmethod
    def info_text_box():
        return f"color: white; background-color: {Styles.COLORS['surface_variant']}; padding: 10px; border-radius: 5px;"

    @staticmethod
    def timer_display():
        return "color: #2196F3; font-family: Arial; font-size: 40px; font-weight: bold;"

    @staticmethod
    def tool_card_base():
        return f"QFrame {{ background-color: {Styles.COLORS['surface']}; border-radius: 15px; min-height: 150px; }}"

    @staticmethod
    def tool_card_title(accent_color):
        return f"color: {accent_color}; font-weight: bold;"

    @staticmethod
    def tool_card_description():
        return f"color: {Styles.COLORS['text_secondary']};"

    @staticmethod
    def tool_icon_fallback(accent_color):
        return f"font-size: 24px; color: {accent_color};"

    @staticmethod
    def info_card_base():
        return f"QFrame {{ background-color: {Styles.COLORS['surface']}; border-radius: 15px; padding: 10px; }} QLabel {{ color: {Styles.COLORS['text_primary']}; }}"

    @staticmethod
    def info_card_hover():
        return f"QFrame {{ background-color: {Styles.COLORS['surface_hover']}; border-radius: 15px; padding: 10px; border: 1px solid {Styles.COLORS['primary']}; }} QLabel {{ color: {Styles.COLORS['text_primary']}; }}"

    @staticmethod
    def info_card_pressed():
        return f"QFrame {{ background-color: {Styles.COLORS['surface_variant']}; border-radius: 15px; padding: 10px; border: 1px solid {Styles.COLORS['primary']}; }} QLabel {{ color: {Styles.COLORS['text_primary']}; }}"

    @staticmethod
    def tool_card_accent(color):
        return f"QFrame {{ background-color: {Styles.COLORS['surface']}; border-radius: 15px; min-height: 150px; }} QLabel#titleLabel {{ color: {color}; font-weight: bold; }}"