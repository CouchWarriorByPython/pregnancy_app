from datetime import date, timedelta
from .data import DEFAULT_MEDICAL_CHECKS

class PregnancyService:
    @staticmethod
    def calculate_current_week(last_period_date):
        if not last_period_date:
            return None
        days_pregnant = (date.today() - last_period_date).days
        return max(1, min(days_pregnant // 7, 42))

    @staticmethod
    def calculate_days_left(due_date):
        if not due_date:
            return None
        return max(0, (due_date - date.today()).days)

    @staticmethod
    def calculate_due_date_from_lmp(last_period_date):
        return last_period_date + timedelta(days=280) if last_period_date else None

    @staticmethod
    def calculate_due_date_from_conception(conception_date):
        return conception_date + timedelta(days=266) if conception_date else None

    @staticmethod
    def get_trimester(week):
        if not week:
            return None
        return 1 if week <= 13 else (2 if week <= 27 else 3)

class UserService:
    @staticmethod
    def calculate_age(birth_date):
        if not birth_date:
            return None
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    @staticmethod
    def calculate_bmi(weight, height):
        if not weight or not height:
            return None
        height_m = height / 100
        return round(weight / (height_m * height_m), 1)

class MedicalCheckService:
    @staticmethod
    def get_checks_by_trimester(trimester):
        return [check for check in DEFAULT_MEDICAL_CHECKS if check['trimester'] == trimester]

    @staticmethod
    def get_upcoming_checks(current_week):
        return sorted([
            check for check in DEFAULT_MEDICAL_CHECKS
            if (check['recommended_week'] and
                current_week <= check['recommended_week'] <= current_week + 4)
        ], key=lambda x: x['recommended_week'])

    @staticmethod
    def get_overdue_checks(current_week):
        return [check for check in DEFAULT_MEDICAL_CHECKS
                if check['deadline_week'] and check['deadline_week'] < current_week]