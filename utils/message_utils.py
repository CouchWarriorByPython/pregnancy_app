"""
Утилітні функції для створення стилізованих повідомлень
"""

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from styles.base import BaseStyles


class StyledMessageBox:
    """Клас для створення стилізованих повідомлень з зеленими кнопками"""
    
    @staticmethod
    def _apply_style(msg_box):
        """Застосовує стиль та прибирає фон з іконок"""
        msg_box.setStyleSheet(BaseStyles.message_box())
        msg_box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        
        # Прибираємо фон з усіх дочірніх елементів
        for child in msg_box.findChildren(QMessageBox):
            child.setStyleSheet("background: transparent; border: none;")
    
    @staticmethod
    def information(parent, title, message):
        """Показує інформаційне повідомлення"""
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        StyledMessageBox._apply_style(msg_box)
        return msg_box.exec()
    
    @staticmethod
    def warning(parent, title, message):
        """Показує попереджувальне повідомлення"""
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        StyledMessageBox._apply_style(msg_box)
        return msg_box.exec()
    
    @staticmethod
    def critical(parent, title, message):
        """Показує критичне повідомлення"""
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        StyledMessageBox._apply_style(msg_box)
        return msg_box.exec()
    
    @staticmethod
    def question(parent, title, message, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No):
        """Показує питання з кнопками"""
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(buttons)
        StyledMessageBox._apply_style(msg_box)
        return msg_box.exec()


# Зручні функції для швидкого використання
def show_info(parent, title, message):
    """Швидка функція для показу інформаційного повідомлення"""
    return StyledMessageBox.information(parent, title, message)

def show_warning(parent, title, message):
    """Швидка функція для показу попереджувального повідомлення"""
    return StyledMessageBox.warning(parent, title, message)

def show_error(parent, title, message):
    """Швидка функція для показу повідомлення про помилку"""
    return StyledMessageBox.critical(parent, title, message)

def show_question(parent, title, message, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No):
    """Швидка функція для показу питання"""
    return StyledMessageBox.question(parent, title, message, buttons) 