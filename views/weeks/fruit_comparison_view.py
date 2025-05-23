from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from utils.image_utils import generate_fruit_image
from utils.logger import get_logger
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

        self.setStyleSheet("""
            background-color: #222222;
            border-radius: 15px;
            padding: 20px;
            margin: 10px;
        """)

        self._create_title(layout)
        self._create_image(layout)
        self._create_description(layout)
        self._create_size_info(layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def _create_title(self, layout):
        title = QLabel(f"Ваша дитина зараз як {self.fruit_data['fruit']}")
        title.setObjectName("fruit_title")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FF8C00;")
        layout.addWidget(title)

    def _create_image(self, layout):
        self.image_label = QLabel()
        self.image_label.setObjectName("fruit_image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.image_label.setPixmap(self._load_image_for_week(self.week))
        layout.addWidget(self.image_label)

    def _create_description(self, layout):
        description = QLabel(self.fruit_data.get('description', 'Тіло дитини наповнюється і формуються пропорції'))
        description.setObjectName("fruit_description")
        description.setFont(QFont('Arial', 12))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(description)

    def _create_size_info(self, layout):
        size_info = QLabel(f"Вага: {self.fruit_data.get('weight', 'невідомо')}; "
                           f"Довжина: {self.fruit_data.get('length', 'невідомо')}")
        size_info.setObjectName("fruit_size_info")
        size_info.setFont(QFont('Arial', 12))
        size_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        size_info.setStyleSheet("color: #DDDDDD;")
        layout.addWidget(size_info)

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

        updates = [
            ("fruit_title", f"Ваша дитина зараз як {fruit_data['fruit']}"),
            ("fruit_description", fruit_data.get('description', 'Інформація відсутня')),
            ("fruit_size_info",
             f"Вага: {fruit_data.get('weight', 'невідомо')}; Довжина: {fruit_data.get('length', 'невідомо')}")
        ]

        for object_name, text in updates:
            widget = self.findChild(QLabel, object_name)
            if widget:
                widget.setText(text)

        image = self.findChild(QLabel, "fruit_image")
        if image:
            image.setPixmap(self._load_image_for_week(week))