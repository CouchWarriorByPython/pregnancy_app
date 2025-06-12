from ..base import BaseStyles, Colors


class ToolsScreenStyles:
    @staticmethod
    def tool_card():
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def tool_card_hover():
        return f"""
            QFrame {{
                background: {Colors.SURFACE_HOVER};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def tool_card_pressed():
        return f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.25);
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def tool_card_title(accent_color):
        return f"""
            color: {accent_color}; 
            font-weight: 700;
            font-size: 16px;
            background: transparent;
            border: none;
        """

    @staticmethod
    def tool_card_description():
        return f"""
            color: {Colors.TEXT_PRIMARY};
            font-size: 13px;
            font-weight: 500;
            line-height: 1.3;
            background: transparent;
            border: none;
        """


class HealthReportStyles:
    @staticmethod
    def report_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(239, 68, 68, 0.1), stop:1 rgba(220, 38, 38, 0.1));
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def export_button():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF5252, stop:1 #D32F2F);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #D32F2F, stop:1 #B71C1C);
            }}
        """


class KegelExercisesStyles:
    @staticmethod
    def info_box():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(156, 39, 176, 0.1), stop:1 rgba(142, 36, 170, 0.1));
                padding: 20px;
                border-radius: 16px;
                border: 1px solid rgba(156, 39, 176, 0.3);
                font-size: 14px;
                font-weight: 500;
                line-height: 1.6;
            }}
        """

    @staticmethod
    def exercise_button():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #9C27B0, stop:1 #7B1FA2);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 15px 25px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7B1FA2, stop:1 #4A148C);
            }}
        """


class WeightMonitorStyles:
    @staticmethod
    def monitor_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(117, 117, 117, 0.1), stop:1 rgba(97, 97, 97, 0.1));
                border: 1px solid rgba(117, 117, 117, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def monitor_button():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #757575, stop:1 #616161);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #616161, stop:1 #424242);
            }}
        """


class KickCounterStyles:
    @staticmethod
    def counter_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(76, 175, 80, 0.1), stop:1 rgba(56, 142, 60, 0.1));
                border: 1px solid rgba(76, 175, 80, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def counter_button():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4CAF50, stop:1 #388E3C);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #388E3C, stop:1 #2E7D32);
            }}
        """

    @staticmethod
    def info_text():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                background: rgba(76, 175, 80, 0.1);
                padding: 16px;
                border-radius: 12px;
                border: 1px solid rgba(76, 175, 80, 0.3);
                font-size: 13px;
                font-weight: 500;
                line-height: 1.5;
            }}
        """


class ContractionCounterStyles:
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

    @staticmethod
    def timer_display():
        return f"""
            color: #2196F3; 
            font-family: 'Segoe UI', Arial; 
            font-size: 48px; 
            font-weight: 700;
            background: transparent;
            border: none;
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2196F3, stop:1 #1976D2);
                border-radius: 12px;
            }}
        """

    @staticmethod
    def contraction_button():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1976D2, stop:1 #1565C0);
            }}
        """


class BellyTrackerStyles:
    @staticmethod
    def tracker_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(255, 152, 0, 0.1), stop:1 rgba(245, 124, 0, 0.1));
                border: 1px solid rgba(255, 152, 0, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def tracker_button():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF9800, stop:1 #F57C00);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F57C00, stop:1 #E65100);
            }}
        """


class BloodPressureStyles:
    @staticmethod
    def pressure_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(233, 30, 99, 0.1), stop:1 rgba(194, 24, 91, 0.1));
                border: 1px solid rgba(233, 30, 99, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def pressure_button():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E91E63, stop:1 #C2185B);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C2185B, stop:1 #AD1457);
            }}
        """


class WishlistStyles:
    @staticmethod
    def wishlist_card():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(103, 58, 183, 0.1), stop:1 rgba(81, 45, 168, 0.1));
                border: 1px solid rgba(103, 58, 183, 0.3);
                border-radius: 20px;
                padding: 20px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def wishlist_button():
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #673AB7, stop:1 #512DA8);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #512DA8, stop:1 #4527A0);
            }}
        """

    @staticmethod
    def priority_colors():
        return {
            'low': '#94A3B8',
            'medium': '#64748B',
            'high': '#F97316',
            'purchased': '#10B981'
        }


class SliderStyles:
    @staticmethod
    def horizontal_slider():
        return f"""
            QSlider::groove:horizontal {{
                border: 1px solid {Colors.GLASS_BORDER};
                height: 10px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }}
            QSlider::handle:horizontal {{
                background: {Colors.PRIMARY_GRADIENT};
                border: 2px solid white;
                width: 20px;
                height: 20px;
                border-radius: 12px;
                margin: -7px 0;
            }}
            QSlider::handle:horizontal:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #DB2777);
            }}
            QSlider::sub-page:horizontal {{
                background: {Colors.PRIMARY_GRADIENT};
                border-radius: 5px;
            }}
            QSlider::add-page:horizontal {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }}
        """