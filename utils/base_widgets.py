from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
                             QLineEdit, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QCheckBox,
                             QComboBox, QListWidget, QScrollArea, QFormLayout)
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QPolygon
from PyQt6.QtCore import Qt, QRect, QPoint
from styles.base import BaseStyles

class BaseWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

class BaseFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(BaseStyles.card_frame())

class StyledCard(QFrame):
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet(BaseStyles.card_frame())
        self.layout = QVBoxLayout(self)
        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
            title_label.setStyleSheet(BaseStyles.text_accent())
            self.layout.addWidget(title_label)

class StyledFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_layout = QFormLayout(self)
        self.form_layout.setContentsMargins(15, 15, 15, 15)
        self.form_layout.setSpacing(15)

class StyledButton(QPushButton):
    def __init__(self, text, style_type='primary', parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(50)
        if style_type == 'primary':
            self.setStyleSheet(BaseStyles.button_primary())
        elif style_type == 'secondary':
            self.setStyleSheet(BaseStyles.button_secondary())
        elif style_type == 'success':
            self.setStyleSheet(BaseStyles.button_success())
        elif style_type == 'error':
            self.setStyleSheet(BaseStyles.button_error())

class BaseInput(QWidget):
    def _apply_common_style(self, widget):
        widget.setStyleSheet(BaseStyles.input_field())
        widget.setMinimumHeight(40)
        return widget

class StyledInput(QLineEdit, BaseInput):
    def __init__(self, placeholder=None, parent=None):
        super().__init__(parent)
        self._apply_common_style(self)
        if placeholder:
            self.setPlaceholderText(placeholder)

class StyledDateEdit(QDateEdit, BaseInput):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setCalendarPopup(False)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setMinimumHeight(24)
        self.setMaximumHeight(40)
        
        # МАКСИМАЛЬНО агресивний стиль - приховуємо ВСЕ
        ultra_aggressive_style = """
            StyledDateEdit {
                background: transparent !important;
                color: white !important;
                border: none !important;
                border-bottom: 2px solid rgba(139, 92, 246, 1) !important;
                border-radius: 0px !important;
                padding: 4px 4px 4px 4px !important;
                font-size: 16px !important;
                min-height: 20px !important;
            }
            StyledDateEdit:focus {
                border-bottom: 2px solid rgba(236, 72, 153, 1) !important;
                background: transparent !important;
            }
            QDateEdit {
                background: transparent !important;
                color: white !important;
                border: none !important;
                border-bottom: 2px solid rgba(139, 92, 246, 1) !important;
                border-radius: 0px !important;
                padding: 4px 4px 4px 4px !important;
                font-size: 16px !important;
                min-height: 20px !important;
            }
            QDateEdit:focus {
                border-bottom: 2px solid rgba(236, 72, 153, 1) !important;
                background: transparent !important;
            }
            QDateEdit::drop-down, StyledDateEdit::drop-down {
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
                subcontrol-position: right;
                subcontrol-origin: margin;
                image: none !important;
            }
            QDateEdit::down-arrow, StyledDateEdit::down-arrow {
                image: none !important;
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
            }
            QDateEdit::up-button, QDateEdit::down-button, 
            StyledDateEdit::up-button, StyledDateEdit::down-button {
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
                image: none !important;
            }
            QDateEdit QAbstractSpinBox::up-button, QDateEdit QAbstractSpinBox::down-button,
            StyledDateEdit QAbstractSpinBox::up-button, StyledDateEdit QAbstractSpinBox::down-button {
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
                image: none !important;
            }
            QDateEdit QAbstractSpinBox::up-arrow, QDateEdit QAbstractSpinBox::down-arrow,
            StyledDateEdit QAbstractSpinBox::up-arrow, StyledDateEdit QAbstractSpinBox::down-arrow {
                image: none !important;
                width: 0px !important;
                height: 0px !important;
                border: none !important;
                background: transparent !important;
            }
            QDateEdit::section, StyledDateEdit::section {
                background: transparent !important;
                color: white !important;
                border: none !important;
                selection-background-color: transparent !important;
                selection-color: white !important;
            }
            QDateEdit::separator, StyledDateEdit::separator {
                color: white !important;
                background: transparent !important;
                border: none !important;
                image: none !important;
                width: 0px !important;
                height: 0px !important;
            }
        """
        self.setStyleSheet(ultra_aggressive_style)
        
        # Додатково прибираємо кнопки програмно
        self.setButtonSymbols(QDateEdit.ButtonSymbols.NoButtons)
    
    # Remove custom arrow drawing - just use clean input field
    pass

class StyledTimeEdit(QTimeEdit, BaseInput):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_common_style(self)
        self.setStyleSheet(BaseStyles.form_controls())

class StyledSpinBox(QSpinBox, BaseInput):
    def __init__(self, min_val=0, max_val=100, suffix=None, parent=None):
        super().__init__(parent)
        self._apply_common_style(self)
        self.setRange(min_val, max_val)
        if suffix:
            self.setSuffix(suffix)
        self.setStyleSheet(BaseStyles.form_controls())

class StyledDoubleSpinBox(QDoubleSpinBox, BaseInput):
    def __init__(self, min_val=0.0, max_val=100.0, decimals=1, suffix=None, parent=None):
        super().__init__(parent)
        self._apply_common_style(self)
        self.setRange(min_val, max_val)
        self.setDecimals(decimals)
        if suffix:
            self.setSuffix(suffix)
        self.setStyleSheet(BaseStyles.form_controls())

class StyledCheckBox(QCheckBox):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(BaseStyles.checkbox())

class StyledComboBox(QComboBox, BaseInput):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self._apply_common_style(self)
        if items:
            self.addItems(items)
        self.setStyleSheet(BaseStyles.form_controls())

class StyledListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(BaseStyles.list_widget())

class StyledScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet(BaseStyles.scroll_area())

class HeaderWidget(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet(BaseStyles.header())
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title_label.setStyleSheet(BaseStyles.text_accent())
        layout.addWidget(title_label)

class TabButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(50)

class TitleLabel(QLabel):
    def __init__(self, text, size=18, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont('Arial', size, QFont.Weight.Bold))
        self.setStyleSheet(BaseStyles.text_accent())