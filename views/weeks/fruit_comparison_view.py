from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from utils.image_utils import generate_fruit_image
from utils.logger import get_logger
from styles.weeks import WeeksStyles
from styles.base import Colors
import os

logger = get_logger('fruit_comparison_view')


class FruitComparisonView(QWidget):
    def __init__(self, week, fruit_data, parent=None):
        super().__init__(parent)
        self.week = week
        self.fruit_data = fruit_data
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(WeeksStyles.fruit_comparison_card())

        self._create_title(layout)
        self._create_image_and_size_section(layout)
        self._create_description(layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def _create_title(self, layout):
        title = QLabel(f"Ваша дитина зараз як {self.fruit_data['fruit']}")
        title.setObjectName("fruit_title")
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {Colors.TEXT_ACCENT}; font-weight: 700;")
        layout.addWidget(title)

    def _create_image_and_size_section(self, layout):
        # Контейнер для картинки та інформації про розмір
        image_size_container = QWidget()
        container_layout = QHBoxLayout(image_size_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(20)

        # Картинка
        self.image_label = QLabel()
        self.image_label.setObjectName("fruit_image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.image_label.setPixmap(self._load_image_for_week(self.week))
        container_layout.addWidget(self.image_label)

        # Інформація про розмір
        size_info_widget = QWidget()
        size_layout = QVBoxLayout(size_info_widget)
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(8)

        weight_label = QLabel(f"Вага: {self.fruit_data.get('weight', 'невідомо')}")
        weight_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        weight_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 600;")
        size_layout.addWidget(weight_label)

        length_label = QLabel(f"Довжина: {self.fruit_data.get('length', 'невідомо')}")
        length_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        length_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 600;")
        size_layout.addWidget(length_label)

        size_layout.addStretch()
        container_layout.addWidget(size_info_widget)
        container_layout.addStretch()

        layout.addWidget(image_size_container)

    def _create_description(self, layout):
        description = QLabel(self.fruit_data.get('description', 'Тіло дитини наповнюється і формуються пропорції'))
        description.setObjectName("fruit_description")
        description.setFont(QFont('Arial', 14))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-weight: 500; line-height: 1.4;")
        layout.addWidget(description)

    def _load_image_for_week(self, week):
        possible_paths = self._get_possible_image_paths(week)

        for image_path in possible_paths:
            logger.info(f"Спроба завантажити зображення: {image_path}")
            if os.path.exists(image_path):
                try:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        logger.info(f"Зображення успішно завантажено: {image_path}")
                        return pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
                except Exception as e:
                    logger.error(f"Помилка завантаження зображення {image_path}: {e}")

        logger.warning(f"Не вдалося знайти зображення для тижня {week}, використовуємо запасний варіант")
        return generate_fruit_image(week, size=180)

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

        # Оновлюємо заголовок
        title_widget = self.findChild(QLabel, "fruit_title")
        if title_widget:
            title_widget.setText(f"Ваша дитина зараз як {fruit_data['fruit']}")

        # Оновлюємо опис
        description_widget = self.findChild(QLabel, "fruit_description")
        if description_widget:
            description_widget.setText(fruit_data.get('description', 'Інформація відсутня'))

        # Оновлюємо картинку
        image_widget = self.findChild(QLabel, "fruit_image")
        if image_widget:
            image_widget.setPixmap(self._load_image_for_week(week))

        # Оновлюємо інформацію про розмір (треба перебудувати весь віджет)
        self._setup_ui()