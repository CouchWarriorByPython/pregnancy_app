from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QLineEdit, QDateEdit, QTimeEdit,
                             QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox,
                             QListWidget, QScrollArea, QFormLayout)
from PyQt6.QtGui import QFont
from .styles import Styles


class StyledWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class StyledFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.frame())


class StyledCard(QFrame):
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.card_frame())
        self.layout = QVBoxLayout(self)

        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
            title_label.setStyleSheet(Styles.text_accent())
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
            self.setStyleSheet(Styles.button_primary())
        elif style_type == 'secondary':
            self.setStyleSheet(Styles.button_secondary())
        elif style_type == 'success':
            self.setStyleSheet(Styles.button_success())
        elif style_type == 'error':
            self.setStyleSheet(Styles.button_error())


class StyledInput(QLineEdit):
    def __init__(self, placeholder=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.input_field())
        self.setMinimumHeight(40)
        if placeholder:
            self.setPlaceholderText(placeholder)


class StyledDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.date_time_edit())
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setMinimumHeight(40)


class StyledTimeEdit(QTimeEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.date_time_edit())
        self.setMinimumHeight(40)


class StyledSpinBox(QSpinBox):
    def __init__(self, min_val=0, max_val=100, suffix=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.spinbox())
        self.setRange(min_val, max_val)
        self.setMinimumHeight(40)
        if suffix:
            self.setSuffix(suffix)


class StyledDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, min_val=0.0, max_val=100.0, decimals=1, suffix=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.spinbox())
        self.setRange(min_val, max_val)
        self.setDecimals(decimals)
        self.setMinimumHeight(40)
        if suffix:
            self.setSuffix(suffix)


class StyledCheckBox(QCheckBox):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(Styles.checkbox())


class StyledComboBox(QComboBox):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.combobox())
        self.setMinimumHeight(40)
        if items:
            self.addItems(items)


class StyledListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.list_widget())


class StyledScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet(Styles.scroll_area())


class HeaderWidget(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Styles.header())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)

        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title_label.setStyleSheet(Styles.text_accent())

        layout.addWidget(title_label)


class TabButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(50)
        self.setStyleSheet(Styles.tab_button())


class TitleLabel(QLabel):
    def __init__(self, text, size=18, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont('Arial', size, QFont.Weight.Bold))
        self.setStyleSheet(Styles.text_accent())