"""
Система стилів для Щоденника вагітності
Централізований імпорт всіх стилів
"""

# Базові стилі
from .base import BaseStyles, Colors
from .components import ComponentStyles
from .navigation import NavigationStyles

# Стилі екранів (включають стилі інструментів та налаштувань)
from .screens import (
    AuthScreenStyles, OnboardingScreenStyles, WeeksScreenStyles,
    CalendarScreenStyles, ToolsScreenStyles, ChecklistScreenStyles,
    SettingsScreenStyles, HealthReportStyles, KegelExercisesStyles,
    WeightMonitorStyles, KickCounterStyles, ContractionCounterStyles,
    BellyTrackerStyles, BloodPressureStyles, WishlistStyles, SliderStyles,
    ProfileEditorStyles, PregnancyEditorStyles, ChildInfoEditorStyles,
    PasswordEditorStyles
)

__all__ = [
    # Базові
    'BaseStyles', 'Colors', 'ComponentStyles', 'NavigationStyles',

    # Екрани
    'AuthScreenStyles', 'OnboardingScreenStyles', 'WeeksScreenStyles',
    'CalendarScreenStyles', 'ToolsScreenStyles', 'ChecklistScreenStyles',
    'SettingsScreenStyles',

    # Інструменти
    'HealthReportStyles', 'KegelExercisesStyles', 'WeightMonitorStyles',
    'KickCounterStyles', 'ContractionCounterStyles', 'BellyTrackerStyles',
    'BloodPressureStyles', 'WishlistStyles', 'SliderStyles',

    # Налаштування
    'ProfileEditorStyles', 'PregnancyEditorStyles', 'ChildInfoEditorStyles',
    'PasswordEditorStyles'
]