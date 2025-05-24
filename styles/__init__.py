"""
Система стилів для Щоденника вагітності
"""

from .base import BaseStyles, Colors
from .weeks import WeeksStyles
from .calendar import CalendarStyles
from .tools import ToolsStyles
from .checklist import ChecklistStyles
from .settings import SettingsStyles
from .auth import AuthStyles
from .onboarding import OnboardingStyles

__all__ = [
    'BaseStyles', 'Colors',
    'WeeksStyles', 'CalendarStyles', 'ToolsStyles',
    'ChecklistStyles', 'SettingsStyles', 'AuthStyles', 'OnboardingStyles'
]