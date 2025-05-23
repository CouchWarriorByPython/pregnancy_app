"""
Стилі для екрану інструментів та окремих інструментів
"""

from .base import BaseStyles, Colors


class ToolsStyles:
    @staticmethod
    def tool_card_base():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                min-height: 150px;
            }}
        """

    @staticmethod
    def tool_card_title(accent_color):
        return f"color: {accent_color}; font-weight: bold;"

    @staticmethod
    def tool_card_description():
        return f"color: {Colors.TEXT_SECONDARY};"

    @staticmethod
    def tool_icon_fallback(accent_color):
        return f"font-size: 24px; color: {accent_color};"

    @staticmethod
    def colored_button(color, hover_color=None):
        hover = hover_color or BaseStyles.darken_color(color)
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {BaseStyles.darken_color(hover)};
            }}
        """

    @staticmethod
    def colored_card(color):
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 15px;
            }}
            QLabel {{
                color: {color};
            }}
        """


class HealthReportStyles:
    @staticmethod
    def export_button():
        return ToolsStyles.colored_button("#FF5252", "#E53935")

    @staticmethod
    def report_card():
        return ToolsStyles.colored_card("#FF5252")


class WeightMonitorStyles:
    @staticmethod
    def monitor_button():
        return ToolsStyles.colored_button("#757575", "#616161")

    @staticmethod
    def monitor_card():
        return ToolsStyles.colored_card("#757575")


class KickCounterStyles:
    @staticmethod
    def counter_button():
        return ToolsStyles.colored_button("#4CAF50", "#388E3C")

    @staticmethod
    def counter_card():
        return ToolsStyles.colored_card("#4CAF50")

    @staticmethod
    def info_text():
        return f"""
            QLabel {{
                color: white;
                background-color: {Colors.SURFACE_VARIANT};
                padding: 10px;
                border-radius: 5px;
            }}
        """


class ContractionCounterStyles:
    @staticmethod
    def timer_display():
        return "color: #2196F3; font-family: Arial; font-size: 40px; font-weight: bold;"

    @staticmethod
    def progress_bar():
        return f"""
            QProgressBar {{
                background-color: {Colors.BORDER};
                border-radius: 5px;
                height: 15px;
            }}
            QProgressBar::chunk {{
                background-color: #2196F3;
                border-radius: 5px;
            }}
        """

    @staticmethod
    def tab_widget():
        return f"""
            QTabWidget::pane {{
                border: 1px solid {Colors.SURFACE_VARIANT};
                background-color: {Colors.SURFACE};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {Colors.SURFACE_VARIANT};
                color: {Colors.TEXT_PRIMARY};
                padding: 8px 15px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: #2196F3;
                color: white;
            }}
        """

    @staticmethod
    def contraction_button():
        return ToolsStyles.colored_button("#2196F3", "#1976D2")


class BloodPressureStyles:
    @staticmethod
    def pressure_button():
        return ToolsStyles.colored_button("#E91E63", "#C2185B")

    @staticmethod
    def pressure_card():
        return ToolsStyles.colored_card("#E91E63")


class BellyTrackerStyles:
    @staticmethod
    def tracker_button():
        return ToolsStyles.colored_button("#FF9800", "#F57C00")

    @staticmethod
    def tracker_card():
        return ToolsStyles.colored_card("#FF9800")


class WishlistStyles:
    @staticmethod
    def wishlist_button():
        return ToolsStyles.colored_button("#673AB7", "#5E35B1")

    @staticmethod
    def wishlist_card():
        return ToolsStyles.colored_card("#673AB7")

    @staticmethod
    def priority_colors():
        return {
            'low': '#AAAAAA',
            'high': '#FF9800',
            'purchased': '#777777'
        }


class KegelExercisesStyles:
    @staticmethod
    def exercise_button():
        return ToolsStyles.colored_button("#9C27B0", "#7B1FA2")

    @staticmethod
    def exercise_card():
        return ToolsStyles.colored_card("#9C27B0")

    @staticmethod
    def info_box():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                background-color: {Colors.SURFACE};
                padding: 15px;
                border-radius: 10px;
            }}
        """


class SliderStyles:
    @staticmethod
    def horizontal_slider():
        return f"""
            QSlider::groove:horizontal {{
                height: 8px;
                background: {Colors.BORDER};
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {Colors.PRIMARY};
                border: 1px solid {Colors.PRIMARY};
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{
                background: {Colors.PRIMARY};
                border-radius: 4px;
            }}
        """