from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from utils.image_utils import generate_fruit_image
from utils.logger import get_logger
import os

logger = get_logger('fruit_comparison_view')


class FruitComparisonView(QWidget):
    """Віджет для порівняння розміру дитини з фруктами/овочами"""

    def __init__(self, week, fruit_data, parent=None):
        super().__init__(parent)
        self.week = week
        self.fruit_data = fruit_data
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Віджет надається у вигляді картки
        self.setStyleSheet("""
            background-color: #222222;
            border-radius: 15px;
            padding: 20px;
            margin: 10px;
        """)

        # Заголовок
        title = QLabel(f"Ваша дитина зараз як {self.fruit_data['fruit']}")
        title.setObjectName("fruit_title")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FF8C00;")
        layout.addWidget(title)

        # Зображення фрукта/овоча
        image_label = QLabel()
        image_label.setObjectName("fruit_image")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Завантажуємо зображення з розширеною логікою пошуку
        pixmap = self.load_image_for_week(self.week)
        image_label.setPixmap(pixmap)

        layout.addWidget(image_label)

        # Текст з описом
        description = QLabel(self.fruit_data.get('description', 'Тіло дитини наповнюється і формуються пропорції'))
        description.setObjectName("fruit_description")
        description.setFont(QFont('Arial', 12))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(description)

        # Розмір дитини
        size_info = QLabel(f"Вага: {self.fruit_data.get('weight', 'невідомо')}; "
                           f"Довжина: {self.fruit_data.get('length', 'невідомо')}")
        size_info.setObjectName("fruit_size_info")
        size_info.setFont(QFont('Arial', 12))
        size_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        size_info.setStyleSheet("color: #DDDDDD;")
        layout.addWidget(size_info)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def load_image_for_week(self, week):
        """Розширена логіка завантаження зображення з перевіркою різних шляхів і форматів"""
        # Спершу перевіряємо наявність шляху в даних
        if 'image' in self.fruit_data and self.fruit_data['image']:
            image_path = self.fruit_data['image']
            logger.info(f"Спроба завантажити зображення з шляху з даних: {image_path}")
            if os.path.exists(image_path):
                try:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        logger.info(f"Зображення успішно завантажено: {image_path}")
                        return pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
                except Exception as e:
                    logger.error(f"Помилка завантаження зображення {image_path}: {e}")

        # Перевіряємо альтернативні шляхи і формати
        base_path = "resources/images/fruits"
        possible_formats = ['.png', '.jpg', '.jpeg']

        # Перевіряємо всі можливі варіанти
        for fmt in possible_formats:
            image_path = f"{base_path}/{week}{fmt}"
            logger.info(f"Спроба завантажити зображення з альтернативного шляху: {image_path}")
            if os.path.exists(image_path):
                try:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        logger.info(f"Зображення успішно завантажено: {image_path}")
                        return pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
                except Exception as e:
                    logger.error(f"Помилка завантаження зображення {image_path}: {e}")

        # Додатково перевіряємо варіанти з текстом (week1, week01, тощо)
        for prefix in ['week', 'week_', 'тиждень', 'тиждень_']:
            for fmt in possible_formats:
                image_path = f"{base_path}/{prefix}{week}{fmt}"
                logger.info(f"Спроба завантажити зображення з префіксом: {image_path}")
                if os.path.exists(image_path):
                    try:
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            logger.info(f"Зображення успішно завантажено: {image_path}")
                            return pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)
                    except Exception as e:
                        logger.error(f"Помилка завантаження зображення {image_path}: {e}")

        # Якщо всі спроби невдалі, генеруємо колір за допомогою запасного методу
        logger.warning(f"Не вдалося знайти зображення для тижня {week}, використовуємо запасний варіант")
        return generate_fruit_image(week, size=200)

    def update_fruit_data(self, week, fruit_data):
        """Оновлює дані для порівняння з іншим фруктом/овочем"""
        logger.info(f"Оновлення даних порівняння для тижня {week}")
        self.week = week
        self.fruit_data = fruit_data

        # Знаходимо і оновлюємо заголовок
        title = self.findChild(QLabel, "fruit_title")
        if title:
            title.setText(f"Ваша дитина зараз як {self.fruit_data['fruit']}")

        # Знаходимо і оновлюємо зображення
        image = self.findChild(QLabel, "fruit_image")
        if image:
            # Завантажуємо зображення з розширеною логікою пошуку
            pixmap = self.load_image_for_week(week)
            image.setPixmap(pixmap)

        # Знаходимо і оновлюємо опис
        description = self.findChild(QLabel, "fruit_description")
        if description:
            description.setText(self.fruit_data.get('description', 'Інформація відсутня'))

        # Знаходимо і оновлюємо інформацію про розмір
        size_info = self.findChild(QLabel, "fruit_size_info")
        if size_info:
            size_info.setText(f"Вага: {self.fruit_data.get('weight', 'невідомо')}; "
                              f"Довжина: {self.fruit_data.get('length', 'невідомо')}")
