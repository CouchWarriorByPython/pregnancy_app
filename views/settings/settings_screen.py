from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                          QPushButton, QTabWidget, QComboBox, QSlider,
                          QSpacerItem, QSizePolicy, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon

from controllers.data_controller import DataController
from .profile_editor import ProfileEditor
from .pregnancy_editor import PregnancyEditor

class SettingsScreen(QWidget):
    """Екран налаштувань додатку"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
    
    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Верхній заголовок
        header = QWidget()
        header.setMinimumHeight(60)
        header.setStyleSheet("background-color: #121212;")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)
        
        settings_label = QLabel("Налаштування")
        settings_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        settings_label.setStyleSheet("color: #FF8C00;")
        
        header_layout.addWidget(settings_label)
        main_layout.addWidget(header)
        
        # Таб-віджет для категорій налаштувань
        tab_widget = QTabWidget()
        tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background-color: #121212;
                color: #AAAAAA;
                padding: 10px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #222222;
                color: #FF8C00;
            }
        """)
        
        # Вкладки для різних категорій налаштувань
        profile_tab = QWidget()
        pregnancy_tab = QWidget()
        appearance_tab = QWidget()
        notifications_tab = QWidget()
        backup_tab = QWidget()
        
        # Налаштовуємо кожну вкладку
        self.setup_profile_tab(profile_tab)
        self.setup_pregnancy_tab(pregnancy_tab)
        self.setup_appearance_tab(appearance_tab)
        self.setup_notifications_tab(notifications_tab)
        self.setup_backup_tab(backup_tab)
        
        # Додаємо вкладки до таб-віджету
        tab_widget.addTab(profile_tab, "Профіль")
        tab_widget.addTab(pregnancy_tab, "Вагітність")
        tab_widget.addTab(appearance_tab, "Зовнішній вигляд")
        tab_widget.addTab(notifications_tab, "Сповіщення")
        tab_widget.addTab(backup_tab, "Резервне копіювання")
        
        main_layout.addWidget(tab_widget)
    
    def setup_profile_tab(self, tab):
        """Налаштування вкладки профілю"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Додаємо редактор профілю
        profile_editor = ProfileEditor()
        layout.addWidget(profile_editor)
    
    def setup_pregnancy_tab(self, tab):
        """Налаштування вкладки вагітності"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Додаємо редактор інформації про вагітність
        pregnancy_editor = PregnancyEditor()
        layout.addWidget(pregnancy_editor)
    
    def setup_appearance_tab(self, tab):
        """Налаштування вкладки зовнішнього вигляду"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок
        title = QLabel("Тема додатку")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Варіанти тем
        theme_frame = QFrame()
        theme_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        theme_frame.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        theme_layout = QVBoxLayout(theme_frame)
        
        # Комбобокс для вибору теми
        theme_combo = QComboBox()
        theme_combo.addItems(["Темна (стандартна)", "Темна з рожевим акцентом", "Темна з блакитним акцентом"])
        theme_combo.setMinimumHeight(40)
        theme_combo.setStyleSheet("""
            background-color: #333333;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        theme_layout.addWidget(theme_combo)
        
        layout.addWidget(theme_frame)
        
        # Акцентний колір
        accent_title = QLabel("Акцентний колір")
        accent_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(accent_title)
        
        accent_frame = QFrame()
        accent_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        accent_frame.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        accent_layout = QVBoxLayout(accent_frame)
        
        # Комбобокс для вибору акцентного кольору
        accent_combo = QComboBox()
        accent_combo.addItems(["Помаранчевий", "Рожевий", "Блакитний", "Зелений", "Фіолетовий"])
        accent_combo.setMinimumHeight(40)
        accent_combo.setStyleSheet("""
            background-color: #333333;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        accent_layout.addWidget(accent_combo)
        
        layout.addWidget(accent_frame)
        
        # Кнопка застосування змін
        apply_btn = QPushButton("Застосувати зміни")
        apply_btn.setMinimumHeight(50)
        apply_btn.setStyleSheet("""
            background-color: #FF8C00;
            border: none;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        """)
        layout.addWidget(apply_btn)
        
        layout.addStretch(1)
    
    def setup_notifications_tab(self, tab):
        """Налаштування вкладки сповіщень"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок
        title = QLabel("Налаштування сповіщень")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Рамка для налаштувань
        notif_frame = QFrame()
        notif_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        notif_frame.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        notif_layout = QVBoxLayout(notif_frame)
        
        # Рівень сповіщень
        level_label = QLabel("Рівень сповіщень:")
        level_label.setFont(QFont('Arial', 14))
        notif_layout.addWidget(level_label)
        
        level_combo = QComboBox()
        level_combo.addItems(["Без сповіщень", "Тільки важливі", "Стандартний", "Всі сповіщення"])
        level_combo.setCurrentIndex(2)  # Стандартно - "Стандартний" рівень
        level_combo.setMinimumHeight(40)
        level_combo.setStyleSheet("""
            background-color: #333333;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        notif_layout.addWidget(level_combo)
        
        # Типи сповіщень
        types_label = QLabel("Типи сповіщень:")
        types_label.setFont(QFont('Arial', 14))
        types_label.setContentsMargins(0, 15, 0, 5)
        notif_layout.addWidget(types_label)
        
        # Чекбокси для типів сповіщень
        for notification_type in ["Нагадування про прийом лікаря", "Нагадування про аналізи", "Важливі етапи вагітності", 
                               "Щотижневі оновлення про розвиток дитини"]:
            checkbox = QPushButton(notification_type)
            checkbox.setCheckable(True)
            checkbox.setChecked(True)
            checkbox.setMinimumHeight(40)
            checkbox.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    border: none;
                    border-radius: 8px;
                    padding: 5px 10px;
                    text-align: left;
                    color: white;
                }
                QPushButton:checked {
                    background-color: #FF8C00;
                }
            """)
            notif_layout.addWidget(checkbox)
        
        layout.addWidget(notif_frame)
        
        # Кнопка збереження
        save_btn = QPushButton("Зберегти налаштування")
        save_btn.setMinimumHeight(50)
        save_btn.setStyleSheet("""
            background-color: #FF8C00;
            border: none;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        """)
        layout.addWidget(save_btn)
        
        layout.addStretch(1)
    
    def setup_backup_tab(self, tab):
        """Налаштування вкладки резервного копіювання"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок
        title = QLabel("Керування даними")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Рамка для кнопок
        backup_frame = QFrame()
        backup_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        backup_frame.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        backup_layout = QVBoxLayout(backup_frame)
        
        # Кнопки управління даними
        for action, description in [
            ("Створити резервну копію", "Зберегти всі ваші дані у вигляді резервної копії"),
            ("Відновити з резервної копії", "Відновити дані з попередньо створеної копії"),
            ("Експортувати дані", "Експортувати дані у форматі JSON для використання в інших програмах"),
            ("Імпортувати дані", "Імпортувати дані з файлу JSON")
        ]:
            action_widget = QWidget()
            action_layout = QVBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 5, 0, 5)
            
            action_btn = QPushButton(action)
            action_btn.setMinimumHeight(40)
            action_btn.setStyleSheet("""
                background-color: #333333;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
                color: white;
                font-weight: bold;
            """)
            
            action_desc = QLabel(description)
            action_desc.setStyleSheet("color: #AAAAAA;")
            
            action_layout.addWidget(action_btn)
            action_layout.addWidget(action_desc)
            
            backup_layout.addWidget(action_widget)
        
        layout.addWidget(backup_frame)
        layout.addStretch(1)
    
    def save_settings(self):
        """Зберегти налаштування"""
        # В реальному додатку тут буде збереження в базу даних або файл
        print("Налаштування збережено!")
        
    def logout(self):
        """Вихід з профілю"""
        # В реальному додатку тут буде очищення сесії та перенаправлення на екран входу
        print("Вихід з профілю")
        # Для прикладу переходимо на екран привітання
        self.parent.stack_widget.setCurrentIndex(0) 