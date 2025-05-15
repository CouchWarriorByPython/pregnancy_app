import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QLineEdit, QComboBox, QHBoxLayout, QListWidget,
                             QListWidgetItem, QMessageBox, QSplitter, QFrame,
                             QFormLayout, QDoubleSpinBox, QCheckBox, QDialog,
                             QDialogButtonBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from controllers.data_controller import DataController
from utils.logger import get_logger

logger = get_logger('wishlist')


class WishlistScreen(QWidget):
    """Екран для управління списком бажань"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_wishlist()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Список бажань")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #673AB7;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Додаємо спліттер для розділення форми додавання і списку записів
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # === Ліва частина - форма для додавання записів ===
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #222222; border-radius: 10px; padding: 10px;")
        form_layout = QVBoxLayout(form_frame)

        form_title = QLabel("Додати нове бажання")
        form_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        form_title.setStyleSheet("color: #673AB7;")
        form_layout.addWidget(form_title)

        # Форма для введення даних
        input_form = QFormLayout()

        # Назва товару
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Введіть назву товару або послуги")
        self.title_edit.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        input_form.addRow("Назва:", self.title_edit)

        # Опис
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Додаткові деталі (розмір, колір, тощо)")
        self.description_edit.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        input_form.addRow("Опис:", self.description_edit)

        # Категорія
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Одяг для вагітних",
            "Одяг для дитини",
            "Меблі та інтер'єр",
            "Засоби гігієни",
            "Іграшки та розваги",
            "Медичні та доглядові засоби",
            "Інше"
        ])
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: #444444;
                border-left-style: solid;
            }
            QComboBox QAbstractItemView {
                background-color: #333333;
                border: 1px solid #444444;
                color: white;
                selection-background-color: #673AB7;
            }
        """)
        input_form.addRow("Категорія:", self.category_combo)

        # Ціна
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0.0, 100000.0)
        self.price_spin.setDecimals(2)
        self.price_spin.setValue(0.0)
        self.price_spin.setSuffix(" грн")
        self.price_spin.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        input_form.addRow("Ціна:", self.price_spin)

        # Пріоритет
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Низький", "Середній", "Високий"])
        self.priority_combo.setCurrentIndex(1)  # Середній за замовчуванням
        self.priority_combo.setStyleSheet("""
            QComboBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: #444444;
                border-left-style: solid;
            }
            QComboBox QAbstractItemView {
                background-color: #333333;
                border: 1px solid #444444;
                color: white;
                selection-background-color: #673AB7;
            }
        """)
        input_form.addRow("Пріоритет:", self.priority_combo)

        # Статус "Придбано"
        self.purchased_check = QCheckBox("Вже придбано")
        self.purchased_check.setStyleSheet("""
            QCheckBox {
                color: white;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border-radius: 3px;
                border: 1px solid #444444;
            }
            QCheckBox::indicator:checked {
                background-color: #673AB7;
                border: 1px solid #673AB7;
                image: url(resources/images/icons/check.png);
            }
        """)
        input_form.addRow("", self.purchased_check)

        form_layout.addLayout(input_form)

        # Кнопка збереження
        save_btn = QPushButton("Додати в список")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #673AB7;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5E35B1;
            }
        """)
        save_btn.clicked.connect(self.add_wishlist_item)
        form_layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        # === Права частина - список записів ===
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = QFrame()
        list_frame.setStyleSheet("background-color: #222222; border-radius: 10px; padding: 10px;")
        list_layout = QVBoxLayout(list_frame)

        list_title = QLabel("Ваш список бажань")
        list_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        list_title.setStyleSheet("color: #673AB7;")
        list_layout.addWidget(list_title)

        # Фільтр категорій
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Фільтр категорій:")
        filter_label.setStyleSheet("color: white;")

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Всі категорії")
        self.filter_combo.addItems([
            "Одяг для вагітних",
            "Одяг для дитини",
            "Меблі та інтер'єр",
            "Засоби гігієни",
            "Іграшки та розваги",
            "Медичні та доглядові засоби",
            "Інше"
        ])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: #444444;
                border-left-style: solid;
            }
            QComboBox QAbstractItemView {
                background-color: #333333;
                border: 1px solid #444444;
                color: white;
                selection-background-color: #673AB7;
            }
        """)
        self.filter_combo.currentIndexChanged.connect(self.load_wishlist)

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)

        list_layout.addLayout(filter_layout)

        # Список бажань
        self.wishlist = QListWidget()
        self.wishlist.setStyleSheet("""
            QListWidget {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #444444;
            }
            QListWidget::item:selected {
                background-color: #673AB7;
            }
        """)
        self.wishlist.itemDoubleClicked.connect(self.edit_item)
        list_layout.addWidget(self.wishlist)

        # Кнопки дій
        buttons_layout = QHBoxLayout()

        refresh_btn = QPushButton("Оновити список")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        refresh_btn.clicked.connect(self.load_wishlist)

        mark_purchased_btn = QPushButton("Позначити як придбане")
        mark_purchased_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        mark_purchased_btn.clicked.connect(self.mark_as_purchased)

        delete_btn = QPushButton("Видалити")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        delete_btn.clicked.connect(self.delete_item)

        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(mark_purchased_btn)
        buttons_layout.addWidget(delete_btn)

        list_layout.addLayout(buttons_layout)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_wishlist(self):
        """Завантажує список бажань з бази даних"""
        try:
            category = None
            if self.filter_combo.currentIndex() > 0:
                category = self.filter_combo.currentText()

            items = self.data_controller.db.get_wishlist_items(category)

            self.wishlist.clear()

            for item in items:
                # Визначаємо пріоритет
                priority_text = ""
                if item['priority'] == 1:
                    priority_text = "Низький"
                elif item['priority'] == 2:
                    priority_text = "Середній"
                else:
                    priority_text = "Високий"

                # Створюємо текст для елемента списку
                item_text = f"{item['title']}"
                if item['price']:
                    item_text += f" - {item['price']} грн"
                item_text += f" ({priority_text})"

                # Додаємо статус "Придбано"
                if item['is_purchased']:
                    item_text = f"✓ {item_text}"

                list_item = QListWidgetItem(item_text)
                list_item.setData(Qt.ItemDataRole.UserRole, item)

                # Змінюємо колір для різних пріоритетів
                if item['priority'] == 1:  # Низький
                    list_item.setForeground(QColor('#AAAAAA'))
                elif item['priority'] == 3:  # Високий
                    list_item.setForeground(QColor('#FF9800'))

                # Закреслюємо текст для придбаних товарів
                if item['is_purchased']:
                    font = list_item.font()
                    font.setStrikeOut(True)
                    list_item.setFont(font)
                    list_item.setForeground(QColor('#777777'))

                self.wishlist.addItem(list_item)

            logger.info(f"Завантажено {len(items)} елементів списку бажань")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити список бажань: {str(e)}")
            logger.error(f"Помилка при завантаженні списку бажань: {str(e)}")

    def add_wishlist_item(self):
        """Додає новий елемент до списку бажань"""
        try:
            title = self.title_edit.text().strip()
            if not title:
                QMessageBox.warning(self, "Попередження", "Введіть назву товару")
                return

            description = self.description_edit.text().strip()
            category = self.category_combo.currentText()
            price = self.price_spin.value() if self.price_spin.value() > 0 else None

            # Перетворення пріоритету з тексту в число
            priority_text = self.priority_combo.currentText()
            if priority_text == "Низький":
                priority = 1
            elif priority_text == "Високий":
                priority = 3
            else:  # Середній
                priority = 2

            is_purchased = self.purchased_check.isChecked()

            # Зберігаємо запис у базу
            item_id = self.data_controller.db.add_wishlist_item(title, description, category, price, priority)

            # Якщо відмічено як "Придбано", встановлюємо відповідний статус
            if is_purchased:
                self.data_controller.db.mark_wishlist_item_purchased(item_id)

            # Очищаємо поля
            self.title_edit.clear()
            self.description_edit.clear()
            self.price_spin.setValue(0.0)
            self.purchased_check.setChecked(False)

            # Оновлюємо список
            self.load_wishlist()

            QMessageBox.information(self, "Успіх", "Товар успішно додано до списку бажань")
            logger.info(f"Додано новий товар до списку бажань: {title}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося додати товар: {str(e)}")
            logger.error(f"Помилка при додаванні товару до списку бажань: {str(e)}")

    def mark_as_purchased(self):
        """Позначає вибраний елемент як придбаний"""
        try:
            selected_items = self.wishlist.selectedItems()

            if not selected_items:
                QMessageBox.warning(self, "Попередження", "Виберіть товар зі списку")
                return

            item = selected_items[0]
            item_data = item.data(Qt.ItemDataRole.UserRole)

            # Якщо товар вже придбаний, пропускаємо
            if item_data['is_purchased']:
                QMessageBox.information(self, "Інформація", "Цей товар вже позначено як придбаний")
                return

            # Позначаємо як придбаний
            self.data_controller.db.mark_wishlist_item_purchased(item_data['id'])

            # Оновлюємо список
            self.load_wishlist()

            QMessageBox.information(self, "Успіх", "Товар позначено як придбаний")
            logger.info(f"Товар позначено як придбаний: {item_data['title']}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося оновити статус товару: {str(e)}")
            logger.error(f"Помилка при позначенні товару як придбаного: {str(e)}")

    def delete_item(self):
        """Видаляє вибраний елемент зі списку бажань"""
        try:
            selected_items = self.wishlist.selectedItems()

            if not selected_items:
                QMessageBox.warning(self, "Попередження", "Виберіть товар зі списку")
                return

            item = selected_items[0]
            item_data = item.data(Qt.ItemDataRole.UserRole)

            # Запитуємо підтвердження
            confirm = QMessageBox.question(
                self, "Підтвердження видалення",
                f"Ви впевнені, що хочете видалити товар '{item_data['title']}' зі списку бажань?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                # Видаляємо з бази
                self.data_controller.db.execute_update(
                    "DELETE FROM wishlist WHERE id = ?",
                    (item_data['id'],)
                )

                # Оновлюємо список
                self.load_wishlist()

                QMessageBox.information(self, "Успіх", "Товар видалено зі списку бажань")
                logger.info(f"Товар видалено зі списку бажань: {item_data['title']}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося видалити товар: {str(e)}")
            logger.error(f"Помилка при видаленні товару зі списку бажань: {str(e)}")

    def edit_item(self, item):
        """Редагує вибраний елемент списку бажань"""
        try:
            item_data = item.data(Qt.ItemDataRole.UserRole)

            # Створюємо діалог редагування
            dialog = QDialog(self)
            dialog.setWindowTitle("Редагування товару")
            dialog.setMinimumWidth(400)
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #222222;
                }
                QLabel {
                    color: white;
                }
                QLineEdit, QComboBox, QDoubleSpinBox {
                    background-color: #333333;
                    border: none;
                    border-radius: 5px;
                    color: white;
                    padding: 5px;
                }
                QCheckBox {
                    color: white;
                }
                QCheckBox::indicator {
                    width: 15px;
                    height: 15px;
                    border-radius: 3px;
                    border: 1px solid #444444;
                }
                QCheckBox::indicator:checked {
                    background-color: #673AB7;
                    border: 1px solid #673AB7;
                }
            """)

            layout = QVBoxLayout(dialog)

            form = QFormLayout()

            # Назва товару
            title_edit = QLineEdit(item_data['title'])
            form.addRow("Назва:", title_edit)

            # Опис
            description_edit = QLineEdit(item_data['description'] or "")
            form.addRow("Опис:", description_edit)

            # Категорія
            category_combo = QComboBox()
            category_combo.addItems([
                "Одяг для вагітних",
                "Одяг для дитини",
                "Меблі та інтер'єр",
                "Засоби гігієни",
                "Іграшки та розваги",
                "Медичні та доглядові засоби",
                "Інше"
            ])
            if item_data['category'] in [category_combo.itemText(i) for i in range(category_combo.count())]:
                category_combo.setCurrentText(item_data['category'])

            form.addRow("Категорія:", category_combo)

            # Ціна
            price_spin = QDoubleSpinBox()
            price_spin.setRange(0.0, 100000.0)
            price_spin.setDecimals(2)
            price_spin.setValue(item_data['price'] or 0.0)
            price_spin.setSuffix(" грн")
            form.addRow("Ціна:", price_spin)

            # Пріоритет
            priority_combo = QComboBox()
            priority_combo.addItems(["Низький", "Середній", "Високий"])

            # Перетворюємо числовий пріоритет у текст
            if item_data['priority'] == 1:
                priority_combo.setCurrentText("Низький")
            elif item_data['priority'] == 3:
                priority_combo.setCurrentText("Високий")
            else:
                priority_combo.setCurrentText("Середній")

            form.addRow("Пріоритет:", priority_combo)

            # Статус "Придбано"
            purchased_check = QCheckBox("Вже придбано")
            purchased_check.setChecked(item_data['is_purchased'])
            form.addRow("", purchased_check)

            layout.addLayout(form)

            # Кнопки
            buttons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Зберегти")
            buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Скасувати")
            buttons.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet("""
                QPushButton {
                    background-color: #673AB7;
                    color: white;
                    border-radius: 5px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #5E35B1;
                }
            """)
            buttons.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border-radius: 5px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
            """)
            layout.addWidget(buttons)

            # Показуємо діалог
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                # Збираємо дані з форми
                new_title = title_edit.text().strip()
                if not new_title:
                    QMessageBox.warning(self, "Попередження", "Назва товару не може бути порожньою")
                    return

                new_description = description_edit.text().strip()
                new_category = category_combo.currentText()
                new_price = price_spin.value() if price_spin.value() > 0 else None

                # Перетворення пріоритету з тексту в число
                priority_text = priority_combo.currentText()
                if priority_text == "Низький":
                    new_priority = 1
                elif priority_text == "Високий":
                    new_priority = 3
                else:  # Середній
                    new_priority = 2

                new_is_purchased = purchased_check.isChecked()

                # Оновлюємо дані в базі
                self.data_controller.db.execute_update(
                    """UPDATE wishlist
                       SET title        = ?,
                           description  = ?,
                           category     = ?,
                           price        = ?,
                           priority     = ?,
                           is_purchased = ?
                       WHERE id = ?""",
                    (new_title, new_description, new_category, new_price, new_priority,
                     new_is_purchased, item_data['id'])
                )

                # Якщо статус "Придбано" змінився на True, встановлюємо дату придбання
                if new_is_purchased and not item_data['is_purchased']:
                    purchase_date = datetime.date.today().strftime("%Y-%m-%d")
                    self.data_controller.db.execute_update(
                        "UPDATE wishlist SET purchase_date = ? WHERE id = ?",
                        (purchase_date, item_data['id'])
                    )

                # Оновлюємо список
                self.load_wishlist()

                QMessageBox.information(self, "Успіх", "Товар успішно оновлено")
                logger.info(f"Товар оновлено: {new_title}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося оновити товар: {str(e)}")
            logger.error(f"Помилка при редагуванні товару: {str(e)}")