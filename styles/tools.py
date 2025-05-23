"""
Стилі для екрану інструментів та окремих інструментів
"""

from .base import BaseStyles, Colors


class ToolsStyles:
    @staticmethod
    def tool_card_base():
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                min-height: 180px;
                padding: 20px;
                margin: 8px;
            }}
            QFrame:hover {{
                background: {Colors.SURFACE_HOVER};
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def tool_card_title(accent_color):
        return f"""
            color: {accent_color}; 
            font-weight: 700;
            font-size: 16px;
        """

    @staticmethod
    def tool_card_description():
        return f"""
            color: {Colors.TEXT_SECONDARY};
            font-size: 13px;
            font-weight: 500;
            line-height: 1.5;
            margin-top: 8px;
        """

    @staticmethod
    def tool_icon_fallback(accent_color):
        return f"""
            font-size: 28px; 
            color: {accent_color};
        """

    @staticmethod
    def colored_button(color, hover_color=None):
        hover = hover_color or BaseStyles.darken_color(color.replace('#', ''))
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {color}, stop:1 {hover});
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {hover}, stop:1 {BaseStyles.darken_color(hover.replace('#', ''))});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {BaseStyles.darken_color(hover.replace('#', ''))}, stop:1 {BaseStyles.darken_color(BaseStyles.darken_color(hover.replace('#', '')))});
            }}
        """

    @staticmethod
    def colored_card(color):
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0.1), stop:1 rgba(255, 255, 255, 0.05));
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
            }}
        """


class HealthReportStyles:
    @staticmethod
    def export_button():
        return ToolsStyles.colored_button("#EF4444", "#DC2626")

    @staticmethod
    def report_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(239, 68, 68, 0.1), stop:1 rgba(220, 38, 38, 0.1));
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
            }}
        """


class WeightMonitorStyles:
    @staticmethod
    def monitor_button():
        return ToolsStyles.colored_button("#64748B", "#475569")

    @staticmethod
    def monitor_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(100, 116, 139, 0.1), stop:1 rgba(71, 85, 105, 0.1));
                border: 1px solid rgba(100, 116, 139, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
            }}
        """


class KickCounterStyles:
    @staticmethod
    def counter_button():
        return ToolsStyles.colored_button("#10B981", "#059669")

    @staticmethod
    def counter_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(16, 185, 129, 0.1), stop:1 rgba(5, 150, 105, 0.1));
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
            }}
        """

    @staticmethod
    def info_text():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                background: rgba(16, 185, 129, 0.1);
                padding: 16px;
                border-radius: 12px;
                border: 1px solid rgba(16, 185, 129, 0.3);
                font-size: 13px;
                font-weight: 500;
                line-height: 1.5;
            }}
        """


class ContractionCounterStyles:
    @staticmethod
    def timer_display():
        return f"""
            color: #3B82F6; 
            font-family: 'Segoe UI', Arial; 
            font-size: 48px; 
            font-weight: 700;
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
                border: 1px solid {Colors.GLASS_BORDER};
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3B82F6, stop:1 #1D4ED8);
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3B82F6, stop:1 #1D4ED8);
                color: white;
                font-weight: 600;
            }}
            QTabBar::tab:hover:!selected {{
                background: rgba(59, 130, 246, 0.2);
            }}
        """

    @staticmethod
    def contraction_button():
        return ToolsStyles.colored_button("#3B82F6", "#1D4ED8")


class BloodPressureStyles:
    @staticmethod
    def pressure_button():
        return ToolsStyles.colored_button("#EC4899", "#DB2777")

    @staticmethod
    def pressure_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(236, 72, 153, 0.1), stop:1 rgba(219, 39, 119, 0.1));
                border: 1px solid rgba(236, 72, 153, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
            }}
        """


class BellyTrackerStyles:
    @staticmethod
    def tracker_button():
        return ToolsStyles.colored_button("#F97316", "#EA580C")

    @staticmethod
    def tracker_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(249, 115, 22, 0.1), stop:1 rgba(234, 88, 12, 0.1));
                border: 1px solid rgba(249, 115, 22, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
            }}
        """


class WishlistStyles:
    @staticmethod
    def wishlist_button():
        return ToolsStyles.colored_button("#8B5CF6", "#7C3AED")

    @staticmethod
    def wishlist_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(139, 92, 246, 0.1), stop:1 rgba(124, 58, 237, 0.1));
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
            }}
        """

    @staticmethod
    def priority_colors():
        return {
            'low': '#94A3B8',
            'high': '#F97316',
            'purchased': '#64748B'
        }


class KegelExercisesStyles:
    @staticmethod
    def exercise_button():
        return ToolsStyles.colored_button("#A855F7", "#9333EA")

    @staticmethod
    def exercise_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(168, 85, 247, 0.1), stop:1 rgba(147, 51, 234, 0.1));
                border: 1px solid rgba(168, 85, 247, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
            }}
        """

    @staticmethod
    def info_box():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                background: {Colors.GLASS_SURFACE};
                padding: 20px;
                border-radius: 16px;
                border: 1px solid {Colors.GLASS_BORDER};
                font-size: 14px;
                font-weight: 500;
                line-height: 1.6;
            }}
        """


class SliderStyles:
    @staticmethod
    def horizontal_slider():
        return f"""
            QSlider::groove:horizontal {{
                height: 12px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                border: 1px solid {Colors.GLASS_BORDER};
            }}
            QSlider::handle:horizontal {{
                background: {Colors.PRIMARY_GRADIENT};
                border: 2px solid white;
                width: 24px;
                height: 24px;
                margin: -8px 0;
                border-radius: 12px;
            }}
            QSlider::handle:horizontal:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #DB2777);
            }}
            QSlider::sub-page:horizontal {{
                background: {Colors.PRIMARY_GRADIENT};
                border-radius: 6px;
            }}
        """