from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
                             QLineEdit, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QCheckBox,
                             QComboBox, QListWidget, QScrollArea, QFormLayout)
from PyQt6.QtGui import QFont
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
        self._apply_common_style(self)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setStyleSheet(BaseStyles.form_controls())

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