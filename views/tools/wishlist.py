from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QListWidgetItem, QMessageBox, QSplitter,
                             QFormLayout, QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledInput, StyledComboBox, StyledDoubleSpinBox,
                                StyledCheckBox, StyledButton, StyledListWidget, TitleLabel)
from utils.styles import Styles

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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = TitleLabel("Список бажань", 22)
        title.setStyleSheet("color: #673AB7;")
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = StyledCard("Додати нове бажання")
        form_frame.setStyleSheet(form_frame.styleSheet() + "QLabel { color: #673AB7; }")

        input_form = QFormLayout()

        self.title_edit = StyledInput("Введіть назву товару або послуги")
        input_form.addRow("Назва:", self.title_edit)

        self.description_edit = StyledInput("Додаткові деталі (розмір, колір, тощо)")
        input_form.addRow("Опис:", self.description_edit)

        category_items = [
            "Одяг для вагітних",
            "Одяг для дитини",
            "Меблі та інтер'єр",
            "Засоби гігієни",
            "Іграшки та розваги",
            "Медичні та доглядові засоби",
            "Інше"
        ]
        self.category_combo = StyledComboBox(category_items)
        input_form.addRow("Категорія:", self.category_combo)

        self.price_spin = StyledDoubleSpinBox(0.0, 100000.0, 2, " грн")
        input_form.addRow("Ціна:", self.price_spin)

        priority_items = ["Низький", "Середній", "Високий"]
        self.priority_combo = StyledComboBox(priority_items)
        self.priority_combo.setCurrentIndex(1)
        input_form.addRow("Пріоритет:", self.priority_combo)

        self.purchased_check = StyledCheckBox("Вже придбано")
        input_form.addRow("", self.purchased_check)

        form_frame.layout.addLayout(input_form)

        save_btn = StyledButton("Додати в список")
        save_btn.setStyleSheet("background-color: #673AB7; QPushButton:hover { background-color: #5E35B1; }")
        save_btn.clicked.connect(self.add_wishlist_item)
        form_frame.layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = StyledCard("Ваш список бажань")
        list_frame.setStyleSheet(list_frame.styleSheet() + "QLabel { color: #673AB7; }")

        filter_layout = QHBoxLayout()
        filter_label = QLabel("Фільтр категорій:")
        filter_label.setStyleSheet(Styles.text_primary())

        filter_items = ["Всі категорії"] + category_items
        self.filter_combo = StyledComboBox(filter_items)
        self.filter_combo.currentIndexChanged.connect(self.load_wishlist)

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)

        list_frame.layout.addLayout(filter_layout)

        self.wishlist = StyledListWidget()
        self.wishlist.itemDoubleClicked.connect(self.edit_item)
        list_frame.layout.addWidget(self.wishlist)

        buttons_layout = QHBoxLayout()

        refresh_btn = StyledButton("Оновити список", "secondary")
        refresh_btn.clicked.connect(self.load_wishlist)

        mark_purchased_btn = StyledButton("Позначити як придбане", "success")
        mark_purchased_btn.clicked.connect(self.mark_as_purchased)

        delete_btn = StyledButton("Видалити", "error")
        delete_btn.clicked.connect(self.delete_item)

        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(mark_purchased_btn)
        buttons_layout.addWidget(delete_btn)

        list_frame.layout.addLayout(buttons_layout)

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
                priority_text = ""
                if item['priority'] == 1:
                    priority_text = "Низький"
                elif item['priority'] == 2:
                    priority_text = "Середній"
                else:
                    priority_text = "Високий"

                item_text = f"{item['title']}"
                if item['price']:
                    item_text += f" - {item['price']} грн"
                item_text += f" ({priority_text})"

                if item['is_purchased']:
                    item_text = f"✓ {item_text}"

                list_item = QListWidgetItem(item_text)
                list_item.setData(Qt.ItemDataRole.UserRole, item)

                if item['priority'] == 1:
                    list_item.setForeground(QColor('#AAAAAA'))
                elif item['priority'] == 3:
                    list_item.setForeground(QColor('#FF9800'))

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

            priority_text = self.priority_combo.currentText()
            if priority_text == "Низький":
                priority = 1
            elif priority_text == "Високий":
                priority = 3
            else:
                priority = 2

            is_purchased = self.purchased_check.isChecked()

            item_id = self.data_controller.db.add_wishlist_item(title, description, category, price, priority)

            if is_purchased:
                self.data_controller.db.mark_wishlist_item_purchased(item_id)

            self.title_edit.clear()
            self.description_edit.clear()
            self.price_spin.setValue(0.0)
            self.purchased_check.setChecked(False)

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

            if item_data['is_purchased']:
                QMessageBox.information(self, "Інформація", "Цей товар вже позначено як придбаний")
                return

            self.data_controller.db.mark_wishlist_item_purchased(item_data['id'])
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

            confirm = QMessageBox.question(
                self, "Підтвердження видалення",
                f"Ви впевнені, що хочете видалити товар '{item_data['title']}' зі списку бажань?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm == QMessageBox.StandardButton.Yes:
                success = self.data_controller.db.delete_wishlist_item(item_data['id'])

                if success:
                    self.load_wishlist()
                    QMessageBox.information(self, "Успіх", "Товар видалено зі списку бажань")
                    logger.info(f"Товар видалено зі списку бажань: {item_data['title']}")
                else:
                    QMessageBox.warning(self, "Попередження", "Товар не знайдено")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося видалити товар: {str(e)}")
            logger.error(f"Помилка при видаленні товару зі списку бажань: {str(e)}")

    def edit_item(self, item):
        """Редагує вибраний елемент списку бажань"""
        try:
            item_data = item.data(Qt.ItemDataRole.UserRole)

            dialog = QDialog(self)
            dialog.setWindowTitle("Редагування товару")
            dialog.setMinimumWidth(400)
            dialog.setStyleSheet(f"""
                QDialog {{
                    background-color: {Styles.COLORS['surface']};
                }}
            """)

            layout = QVBoxLayout(dialog)

            form = QFormLayout()

            title_edit = StyledInput(item_data['title'])
            form.addRow("Назва:", title_edit)

            description_edit = StyledInput(item_data['description'] or "")
            form.addRow("Опис:", description_edit)

            category_items = [
                "Одяг для вагітних",
                "Одяг для дитини",
                "Меблі та інтер'єр",
                "Засоби гігієни",
                "Іграшки та розваги",
                "Медичні та доглядові засоби",
                "Інше"
            ]
            category_combo = StyledComboBox(category_items)
            if item_data['category'] in category_items:
                category_combo.setCurrentText(item_data['category'])
            form.addRow("Категорія:", category_combo)

            price_spin = StyledDoubleSpinBox(0.0, 100000.0, 2, " грн")
            price_spin.setValue(item_data['price'] or 0.0)
            form.addRow("Ціна:", price_spin)

            priority_items = ["Низький", "Середній", "Високий"]
            priority_combo = StyledComboBox(priority_items)
            if item_data['priority'] == 1:
                priority_combo.setCurrentText("Низький")
            elif item_data['priority'] == 3:
                priority_combo.setCurrentText("Високий")
            else:
                priority_combo.setCurrentText("Середній")
            form.addRow("Пріоритет:", priority_combo)

            purchased_check = StyledCheckBox("Вже придбано")
            purchased_check.setChecked(item_data['is_purchased'])
            form.addRow("", purchased_check)

            layout.addLayout(form)

            buttons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Зберегти")
            buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Скасувати")

            ok_btn = buttons.button(QDialogButtonBox.StandardButton.Ok)
            ok_btn.setStyleSheet(Styles.button_primary())

            cancel_btn = buttons.button(QDialogButtonBox.StandardButton.Cancel)
            cancel_btn.setStyleSheet(Styles.button_secondary())

            layout.addWidget(buttons)

            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                new_title = title_edit.text().strip()
                if not new_title:
                    QMessageBox.warning(self, "Попередження", "Назва товару не може бути порожньою")
                    return

                new_description = description_edit.text().strip()
                new_category = category_combo.currentText()
                new_price = price_spin.value() if price_spin.value() > 0 else None

                priority_text = priority_combo.currentText()
                if priority_text == "Низький":
                    new_priority = 1
                elif priority_text == "Високий":
                    new_priority = 3
                else:
                    new_priority = 2

                new_is_purchased = purchased_check.isChecked()

                success = self.data_controller.db.update_wishlist_item(
                    item_data['id'], new_title, new_description, new_category,
                    new_price, new_priority, new_is_purchased
                )

                if success:
                    self.load_wishlist()
                    QMessageBox.information(self, "Успіх", "Товар успішно оновлено")
                    logger.info(f"Товар оновлено: {new_title}")
                else:
                    QMessageBox.warning(self, "Попередження", "Товар не знайдено")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося оновити товар: {str(e)}")
            logger.error(f"Помилка при редагуванні товару: {str(e)}")