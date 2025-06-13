from controllers.data_controller import DataController
from utils.logger import get_logger

logger = get_logger('user_mixin')


class UserMixin:
    """
    Міксін для стандартизації отримання user_id та ініціалізації DataController
    у всіх компонентах додатку
    """

    def get_current_user_id(self):
        """
        Стандартизований метод отримання поточного user_id
        Шукає user_id в ієрархії батьківських компонентів
        """
        # Перевіряємо чи є user_id безпосередньо в parent
        if hasattr(self, 'parent') and self.parent:
            if hasattr(self.parent, 'current_user_id') and self.parent.current_user_id:
                return self.parent.current_user_id

            # Перевіряємо parent.parent (для вкладених компонентів)
            if hasattr(self.parent, 'parent') and self.parent.parent:
                if hasattr(self.parent.parent, 'current_user_id') and self.parent.parent.current_user_id:
                    return self.parent.parent.current_user_id

        # Шукаємо MainWindow в ієрархії
        main_window = self._find_main_window()
        if main_window and hasattr(main_window, 'current_user_id'):
            return main_window.current_user_id

        logger.warning(f"{self.__class__.__name__}: не вдалося знайти user_id")
        return None

    def _find_main_window(self):
        """
        Знаходить MainWindow в ієрархії батьківських віджетів
        """
        widget = self
        while widget:
            if hasattr(widget, '__class__') and 'MainWindow' in str(widget.__class__):
                return widget
            widget = getattr(widget, 'parent', None) if hasattr(widget, 'parent') else None
        return None

    def init_data_controller(self, force_reinit=False):
        """
        Ініціалізує або оновлює DataController з поточним user_id

        Args:
            force_reinit: Якщо True, примусово переініціалізує контролер

        Returns:
            bool: True якщо вдалось ініціалізувати, False якщо ні
        """
        user_id = self.get_current_user_id()

        if not user_id:
            logger.warning(f"{self.__class__.__name__}: неможливо ініціалізувати DataController без user_id")
            self.data_controller = None
            return False

        # Ініціалізуємо тільки якщо потрібно
        if force_reinit or not hasattr(self,
                                       'data_controller') or not self.data_controller or self.data_controller.user_id != user_id:
            self.data_controller = DataController(user_id)
            logger.info(f"{self.__class__.__name__} ініціалізований з user_id: {user_id}")
            return True

        return True

    def get_user_profile(self):
        """
        Отримує профіль поточного користувача

        Returns:
            UserProfile або None
        """
        if self.init_data_controller():
            return self.data_controller.user_profile
        return None

    def get_pregnancy_data(self):
        """
        Отримує дані про вагітність поточного користувача

        Returns:
            PregnancyData або None
        """
        if self.init_data_controller():
            return self.data_controller.pregnancy_data
        return None

    def is_user_authenticated(self):
        """
        Перевіряє чи користувач авторизований

        Returns:
            bool: True якщо авторизований, False якщо ні
        """
        return self.get_current_user_id() is not None