from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QSize
from utils.logger import get_logger

logger = get_logger('image_utils')


def generate_circle_image(size=200, color="#FF8C00", bg_color="transparent"):
    """Генерує зображення кола замість реальних зображень"""
    try:
        pixmap = QPixmap(size, size)

        # Встановлюємо прозорий фон, якщо потрібно
        if bg_color == "transparent":
            pixmap.fill(Qt.GlobalColor.transparent)
        else:
            pixmap.fill(QColor(bg_color))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Налаштовуємо колір і пензель
        pen = QPen(QColor(color))
        pen.setWidth(2)
        painter.setPen(pen)

        # Додаємо заливку з 20% прозорості
        fill_color = QColor(color)
        fill_color.setAlpha(50)  # 20% непрозорості
        painter.setBrush(QBrush(fill_color))

        # Малюємо коло
        painter.drawEllipse(2, 2, size - 4, size - 4)

        painter.end()
        logger.debug(f"Згенеровано коло розміром {size}x{size} з кольором {color}")
        return pixmap
    except Exception as e:
        logger.error(f"Помилка при генерації кола: {e}")
        # Повертаємо порожнє зображення у випадку помилки
        return QPixmap(size, size)


def generate_fruit_image(week, size=200):
    """Генерує зображення для порівняння розміру плоду по тижнях"""
    # Визначаємо колір залежно від тижня
    colors = {
        # Перший триместр - відтінки зеленого
        1: "#7CB342", 2: "#8BC34A", 3: "#9CCC65", 4: "#AED581",
        5: "#C5E1A5", 6: "#DCEDC8", 7: "#F1F8E9", 8: "#689F38",
        9: "#558B2F", 10: "#33691E", 11: "#CDDC39", 12: "#AFB42B",
        # Другий триместр - відтінки помаранчевого
        13: "#FFB74D", 14: "#FFA726", 15: "#FF9800", 16: "#FB8C00",
        17: "#F57C00", 18: "#EF6C00", 19: "#E65100", 20: "#FFA000",
        21: "#FF8F00", 22: "#FF6F00", 23: "#FFEB3B", 24: "#FDD835",
        # Третій триместр - відтінки червоного/фіолетового
        25: "#F06292", 26: "#EC407A", 27: "#E91E63", 28: "#D81B60",
        29: "#C2185B", 30: "#AD1457", 31: "#880E4F", 32: "#8E24AA",
        33: "#7B1FA2", 34: "#6A1B9A", 35: "#4A148C", 36: "#9C27B0",
        37: "#673AB7", 38: "#5E35B1", 39: "#512DA8", 40: "#4527A0",
        41: "#311B92", 42: "#B39DDB"
    }

    # Вибираємо колір за тижнем або базовий, якщо тиждень поза діапазоном
    color = colors.get(week, "#FF8C00")

    # Генеруємо коло відповідного кольору
    return generate_circle_image(size=size, color=color)