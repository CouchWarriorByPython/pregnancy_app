from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from utils.image_utils import generate_fruit_image
from utils.logger import get_logger
from styles.weeks import WeeksStyles
from styles.base import Colors
import os

logger = get_logger('fruit_comparison_view')


class FruitComparisonView(QFrame):
    def __init__(self, week, fruit_data, parent=None):
        super().__init__(parent)
        self.week = week
        self.fruit_data = fruit_data
        self.setFixedWidth(760)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(WeeksStyles.fruit_comparison_card())

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(25)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Заголовок безпосередньо в основному блоці
        self.title_label = QLabel()
        self.title_label.setObjectName("fruit_title")
        self.title_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"color: {Colors.TEXT_ACCENT}; font-weight: 700;")
        self.main_layout.addWidget(self.title_label)

        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(30)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel()
        self.image_label.setObjectName("fruit_image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(200, 200)
        self.image_label.setStyleSheet(WeeksStyles.fruit_image_style())
        self.content_layout.addWidget(self.image_label)

        self.size_container = QFrame()
        self.size_container.setStyleSheet(WeeksStyles.size_info_container())
        self.size_container.setFixedWidth(250)
        self.size_layout = QVBoxLayout(self.size_container)
        self.size_layout.setContentsMargins(20, 20, 20, 20)
        self.size_layout.setSpacing(12)

        self.weight_label = QLabel()
        self.weight_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.weight_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 700;")
        self.weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_layout.addWidget(self.weight_label)

        self.length_label = QLabel()
        self.length_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.length_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 700;")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_layout.addWidget(self.length_label)

        self.content_layout.addWidget(self.size_container)

        self.main_layout.addLayout(self.content_layout)

        # Опис безпосередньо в основному блоці
        self.description_label = QLabel()
        self.description_label.setObjectName("fruit_description")
        self.description_label.setFont(QFont('Arial', 14))
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(
            f"color: {Colors.TEXT_PRIMARY}; font-weight: 500; line-height: 1.6; padding: 15px 20px; background: {Colors.GLASS_SURFACE}; border: 1px solid {Colors.GLASS_BORDER}; border-radius: 20px; margin-top: 15px;")
        self.main_layout.addWidget(self.description_label)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        self._update_content()

    def _update_content(self):
        self.title_label.setText(f"Ваша дитина зараз як {self.fruit_data['fruit']}")
        self.weight_label.setText(f"Вага: {self.fruit_data.get('weight', 'невідомо')}")
        self.length_label.setText(f"Довжина: {self.fruit_data.get('length', 'невідомо')}")
        self.description_label.setText(self.fruit_data.get('description', 'Дитина продовжує набирати вагу'))
        self.image_label.setPixmap(self._load_image_for_week(self.week))

    def _load_image_for_week(self, week):
        possible_paths = self._get_possible_image_paths(week)

        for image_path in possible_paths:
            logger.info(f"Спроба завантажити зображення: {image_path}")
            if os.path.exists(image_path):
                try:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        logger.info(f"Зображення успішно завантажено: {image_path}")
                        scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                                      Qt.TransformationMode.SmoothTransformation)
                        return self._create_circular_pixmap(scaled_pixmap)
                except Exception as e:
                    logger.error(f"Помилка завантаження зображення {image_path}: {e}")

        logger.warning(f"Не вдалося знайти зображення для тижня {week}, використовуємо запасний варіант")
        fallback_pixmap = generate_fruit_image(week, size=200)
        return self._create_circular_pixmap(fallback_pixmap)

    def _create_circular_pixmap(self, pixmap):
        """Створює кругле зображення з пікселарта"""
        from PyQt6.QtGui import QPainter, QBrush, QPainterPath

        size = 200
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Створюємо круглий шлях
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        # Масштабуємо та центруємо зображення
        if pixmap.width() != size or pixmap.height() != size:
            pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                   Qt.TransformationMode.SmoothTransformation)

        # Центруємо зображення
        x = (size - pixmap.width()) // 2
        y = (size - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)

        painter.end()
        return circular_pixmap

    def _get_possible_image_paths(self, week):
        base_path = "resources/images/fruits"
        formats = ['.png', '.jpg', '.jpeg']
        prefixes = ['', 'week', 'week_', 'тиждень', 'тиждень_']

        paths = []

        if 'image' in self.fruit_data and self.fruit_data['image']:
            paths.append(self.fruit_data['image'])

        for prefix in prefixes:
            for fmt in formats:
                if prefix:
                    paths.append(f"{base_path}/{prefix}{week}{fmt}")
                else:
                    paths.append(f"{base_path}/{week}{fmt}")

        return paths

    def update_fruit_data(self, week, fruit_data):
        logger.info(f"Оновлення даних порівняння для тижня {week}")
        self.week = week
        self.fruit_data = fruit_data
        self._update_content()