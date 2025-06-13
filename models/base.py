from sqlalchemy import Column, Integer, String, Text, Boolean, Float, Date, Time, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), default='Користувач')
    birth_date = Column(Date)
    height = Column(Integer, default=165)
    weight_before_pregnancy = Column(Float, default=60.0)
    previous_pregnancies = Column(Integer, default=0)
    cycle_length = Column(Integer, default=28)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    pregnancy_data = relationship("PregnancyData", back_populates="user", uselist=False)
    weight_records = relationship("WeightRecord", back_populates="user")
    calendar_events = relationship("CalendarEvent", back_populates="user")
    medical_checks = relationship("MedicalCheck", back_populates="user")
    wishlist_items = relationship("WishlistItem", back_populates="user")
    health_notes = relationship("HealthNote", back_populates="user")
    baby_kicks = relationship("BabyKick", back_populates="user")
    contractions = relationship("Contraction", back_populates="user")
    blood_pressure_records = relationship("BloodPressure", back_populates="user")
    belly_measurements = relationship("BellyMeasurement", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    checklist_items = relationship("ChecklistItem", back_populates="user")


class PregnancyData(Base):
    __tablename__ = 'pregnancy_data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    last_period_date = Column(Date)
    conception_date = Column(Date)
    baby_gender = Column(String(20), default='Невідомо')
    baby_name = Column(String(100), default='')

    user = relationship("UserProfile", back_populates="pregnancy_data")

    @property
    def due_date(self):
        if self.conception_date:
            from datetime import timedelta
            return self.conception_date + timedelta(days=266)
        elif self.last_period_date:
            from datetime import timedelta
            return self.last_period_date + timedelta(days=280)
        return None


class WeightRecord(Base):
    __tablename__ = 'weight_records'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    date = Column(Date, nullable=False)
    weight = Column(Float, nullable=False)

    user = relationship("UserProfile", back_populates="weight_records")


class CalendarEvent(Base):
    __tablename__ = 'calendar_events'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    all_day = Column(Boolean, default=False)
    reminder = Column(Boolean, default=False)
    reminder_time = Column(String(10))
    event_type = Column(String(50), default='regular')

    user = relationship("UserProfile", back_populates="calendar_events")


class MedicalCheck(Base):
    __tablename__ = 'medical_checks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    trimester = Column(Integer)
    recommended_week = Column(Integer)
    deadline_week = Column(Integer)
    is_completed = Column(Boolean, default=False)
    completion_date = Column(Date)
    is_custom = Column(Boolean, default=False)

    user = relationship("UserProfile", back_populates="medical_checks")


class WishlistItem(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    price = Column(Float)
    is_purchased = Column(Boolean, default=False)
    purchase_date = Column(Date)
    priority = Column(Integer, default=2)

    user = relationship("UserProfile", back_populates="wishlist_items")


class HealthNote(Base):
    __tablename__ = 'health_notes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    date = Column(Date, nullable=False)
    title = Column(String(200))
    content = Column(Text, nullable=False)

    user = relationship("UserProfile", back_populates="health_notes")


class BabyKick(Base):
    __tablename__ = 'baby_kicks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    count = Column(Integer, nullable=False)

    user = relationship("UserProfile", back_populates="baby_kicks")


class Contraction(Base):
    __tablename__ = 'contractions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)
    intensity = Column(Integer, nullable=False)

    user = relationship("UserProfile", back_populates="contractions")


class BloodPressure(Base):
    __tablename__ = 'blood_pressure'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    systolic = Column(Integer, nullable=False)
    diastolic = Column(Integer, nullable=False)
    pulse = Column(Integer)
    notes = Column(Text)

    user = relationship("UserProfile", back_populates="blood_pressure_records")


class BellyMeasurement(Base):
    __tablename__ = 'belly_measurements'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    date = Column(Date, nullable=False)
    measurement = Column(Float, nullable=False)
    notes = Column(Text)

    user = relationship("UserProfile", back_populates="belly_measurements")


class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    reminder_date = Column(Date, nullable=False)
    reminder_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    reminder_type = Column(String(50), default='custom')
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserProfile", back_populates="reminders")


class ChecklistItem(Base):
    __tablename__ = 'checklist_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    trimester = Column(Integer, nullable=False)  # 1, 2, або 3
    section = Column(String(100), nullable=False)  # Назва секції (Аналізи, УЗД, тощо)
    item_text = Column(String(200), nullable=False)  # Текст пункту
    is_checked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserProfile", back_populates="checklist_items")