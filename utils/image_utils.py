from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt
from utils.logger import get_logger

logger = get_logger('image_utils')


def _create_base_pixmap(size, bg_color="transparent"):
    pixmap = QPixmap(size, size)
    if bg_color == "transparent":
        pixmap.fill(Qt.GlobalColor.transparent)
    else:
        pixmap.fill(QColor(bg_color))
    return pixmap


def _draw_circle(painter, size, color, filled=False, alpha=50):
    pen = QPen(QColor(color))
    pen.setWidth(2 if not filled else 3)
    painter.setPen(pen)

    if filled:
        fill_color = QColor(color)
        fill_color.setAlpha(200)
        painter.setBrush(QBrush(fill_color))
    else:
        fill_color = QColor(color)
        fill_color.setAlpha(alpha)
        painter.setBrush(QBrush(fill_color))

    margin = 2 if not filled else 3
    painter.drawEllipse(margin, margin, size - 2 * margin, size - 2 * margin)


def generate_circle_image(size=200, color="#FF8C00", bg_color="transparent"):
    try:
        pixmap = _create_base_pixmap(size, bg_color)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        _draw_circle(painter, size, color)
        painter.end()

        logger.debug(f"Згенеровано коло розміром {size}x{size} з кольором {color}")
        return pixmap
    except Exception as e:
        logger.error(f"Помилка при генерації кола: {e}")
        return QPixmap(size, size)


def generate_fruit_image(week, size=200):
    week_colors = {
        **{i: "#7CB342" for i in range(1, 5)},  # Зелені відтінки 1-4
        **{i: "#8BC34A" for i in range(5, 9)},  # 5-8
        **{i: "#9CCC65" for i in range(9, 13)},  # 9-12
        **{i: "#FFB74D" for i in range(13, 17)},  # Помаранчеві 13-16
        **{i: "#FFA726" for i in range(17, 21)},  # 17-20
        **{i: "#FF9800" for i in range(21, 25)},  # 21-24
        **{i: "#F06292" for i in range(25, 29)},  # Рожеві 25-28
        **{i: "#EC407A" for i in range(29, 33)},  # 29-32
        **{i: "#E91E63" for i in range(33, 37)},  # 33-36
        **{i: "#9C27B0" for i in range(37, 41)},  # Фіолетові 37-40
        **{i: "#673AB7" for i in range(41, 43)}  # 41-42
    }

    color = week_colors.get(week, "#FF8C00")

    try:
        pixmap = _create_base_pixmap(size)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        _draw_circle(painter, size, color, filled=True)
        painter.end()

        return pixmap
    except Exception as e:
        logger.error(f"Помилка при генерації фрукта: {e}")
        return QPixmap(size, size)