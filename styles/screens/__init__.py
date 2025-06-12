"""
Стилі для всіх екранів застосунку
"""

from .auth_screens import AuthScreenStyles
from .onboarding_screens import OnboardingScreenStyles
from .weeks_screen import WeeksScreenStyles
from .calendar_screen import CalendarScreenStyles
from .tools_screens import (
    ToolsScreenStyles, HealthReportStyles, KegelExercisesStyles,
    WeightMonitorStyles, KickCounterStyles, ContractionCounterStyles,
    BellyTrackerStyles, BloodPressureStyles, WishlistStyles, SliderStyles
)
from .checklist_screen import ChecklistScreenStyles
from .settings_screens import (
    SettingsScreenStyles, ProfileEditorStyles, PregnancyEditorStyles,
    ChildInfoEditorStyles, PasswordEditorStyles
)

__all__ = [
    'AuthScreenStyles',
    'OnboardingScreenStyles',
    'WeeksScreenStyles',
    'CalendarScreenStyles',
    'ToolsScreenStyles',
    'ChecklistScreenStyles',
    'SettingsScreenStyles',
    # Стилі інструментів
    'HealthReportStyles',
    'KegelExercisesStyles',
    'WeightMonitorStyles',
    'KickCounterStyles',
    'ContractionCounterStyles',
    'BellyTrackerStyles',
    'BloodPressureStyles',
    'WishlistStyles',
    'SliderStyles',
    # Стилі налаштувань
    'ProfileEditorStyles',
    'PregnancyEditorStyles',
    'ChildInfoEditorStyles',
    'PasswordEditorStyles'
]