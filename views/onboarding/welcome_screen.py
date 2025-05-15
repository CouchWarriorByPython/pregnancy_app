from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                          QPushButton, QHBoxLayout, QSpacerItem,
                          QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon

class WelcomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 40, 20, 20)
        main_layout.setSpacing(15)
        
        # Додаємо заголовок
        title = QLabel("Щоденник вагітності")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        main_layout.addWidget(title)
        
        # Додаємо вітальне повідомлення
        welcome_text = QLabel("Ласкаво просимо! Цей додаток допоможе вам відстежувати вагітність та отримувати корисну інформацію")
        welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_text.setWordWrap(True)
        welcome_text.setFont(QFont('Arial', 14))
        main_layout.addWidget(welcome_text)
        
        # Додаємо просторовий елемент
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Додаємо зображення
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Заглушка для зображення - в реальному додатку тут буде завантажене фактичне зображення
        image_label.setText("[Тут буде зображення]")
        image_label.setStyleSheet("background-color: #333333; min-height: 200px; border-radius: 15px;")
        main_layout.addWidget(image_label)
        
        # Додаємо просторовий елемент
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Додаємо кнопки
        button_layout = QVBoxLayout()
        
        start_btn = QPushButton("Почати користування")
        start_btn.setMinimumHeight(50)
        start_btn.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        start_btn.clicked.connect(self.start_onboarding)
        
        login_btn = QPushButton("Увійти з існуючим профілем")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #FF8C00;
                color: #FF8C00;
            }
            QPushButton:hover {
                background-color: rgba(255, 140, 0, 0.2);
            }
        """)
        login_btn.setMinimumHeight(50)
        login_btn.setFont(QFont('Arial', 14))
        login_btn.clicked.connect(self.login)
        
        button_layout.addWidget(start_btn)
        button_layout.addWidget(login_btn)
        button_layout.setSpacing(15)
        
        main_layout.addLayout(button_layout)
        
    def start_onboarding(self):
        """Почати процес онбордингу"""
        # В реальному додатку тут буде перехід до екрану онбордингу
        # Наразі просто переходимо до екрану тижнів
        self.parent.stack_widget.setCurrentIndex(1)
        
    def login(self):
        """Вхід з існуючим профілем"""
        # В реальному додатку тут буде екран входу
        # Наразі просто переходимо до екрану тижнів
        self.parent.stack_widget.setCurrentIndex(1) 