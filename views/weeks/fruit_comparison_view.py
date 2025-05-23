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
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(WeeksStyles.fruit_comparison_card())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_title(main_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(40)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_image(content_layout)
        self._create_size_section(content_layout)

        main_layout.addLayout(content_layout)
        self._create_description(main_layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def _create_title(self, layout):
        title = QLabel(f"Ваша дитина зараз як {self.fruit_data['fruit']}")
        title.setObjectName("fruit_title")
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {Colors.TEXT_ACCENT}; font-weight: 700;")
        layout.addWidget(title)

    def _create_image(self, layout):
        self.image_label = QLabel()
        self.image_label.setObjectName("fruit_image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.image_label.setPixmap(self._load_image_for_week(self.week))
        layout.addWidget(self.image_label)

    def _create_size_section(self, layout):
        size_container = QFrame()
        size_container.setStyleSheet(WeeksStyles.size_info_container())
        size_layout = QVBoxLayout(size_container)
        size_layout.setContentsMargins(20, 20, 20, 20)
        size_layout.setSpacing(12)

        weight_label = QLabel(f"Вага: {self.fruit_data.get('weight', 'невідомо')}")
        weight_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        weight_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 700;")
        weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        size_layout.addWidget(weight_label)

        length_label = QLabel(f"Довжина: {self.fruit_data.get('length', 'невідомо')}")
        length_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        length_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 700;")
        length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        size_layout.addWidget(length_label)

        layout.addWidget(size_container)

    def _create_description(self, layout):
        description_container = QFrame()
        description_container.setStyleSheet(WeeksStyles.description_container())
        desc_layout = QVBoxLayout(description_container)
        desc_layout.setContentsMargins(20, 20, 20, 20)

        description = QLabel(self.fruit_data.get('description', 'Дитина продовжує набирати вагу'))
        description.setObjectName("fruit_description")
        description.setFont(QFont('Arial', 14))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 500; line-height: 1.4;")
        desc_layout.addWidget(description)

        layout.addWidget(description_container)

    def _load_image_for_week(self, week):
        possible_paths = self._get_possible_image_paths(week)

        for image_path in possible_paths:
            logger.info(f"Спроба завантажити зображення: {image_path}")
            if os.path.exists(image_path):
                try:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        logger.info(f"Зображення успішно завантажено: {image_path}")
                        return pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
                except Exception as e:
                    logger.error(f"Помилка завантаження зображення {image_path}: {e}")

        logger.warning(f"Не вдалося знайти зображення для тижня {week}, використовуємо запасний варіант")
        return generate_fruit_image(week, size=200)

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

        self._clear_layout(self.layout())
        self._setup_ui()

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())