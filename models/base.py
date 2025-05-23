from sqlalchemy import Column, Integer, String, Text, Boolean, Float, Date, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
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


class PregnancyData(Base):
    __tablename__ = 'pregnancy_data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    last_period_date = Column(Date)
    conception_date = Column(Date)
    baby_gender = Column(String(20), default='Невідомо')
    baby_name = Column(String(100), default='')

    @property
    def due_date(self):
        if self.conception_date:
            from datetime import timedelta
            return self.conception_date + timedelta(days=266)
        return None


class WeightRecord(Base):
    __tablename__ = 'weight_records'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    date = Column(Date)
    weight = Column(Float)


class CalendarEvent(Base):
    __tablename__ = 'calendar_events'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    title = Column(String(200))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    all_day = Column(Boolean, default=True)
    reminder = Column(Boolean, default=False)
    reminder_time = Column(String(10))
    event_type = Column(String(50), default='regular')


class MedicalCheck(Base):
    __tablename__ = 'medical_checks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    title = Column(String(200))
    description = Column(Text)
    trimester = Column(Integer)
    recommended_week = Column(Integer)
    deadline_week = Column(Integer)
    is_completed = Column(Boolean, default=False)
    completion_date = Column(Date)
    is_custom = Column(Boolean, default=False)


class WishlistItem(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    title = Column(String(200))
    description = Column(Text)
    category = Column(String(100))
    price = Column(Float)
    is_purchased = Column(Boolean, default=False)
    purchase_date = Column(Date)
    priority = Column(Integer, default=2)


class HealthNote(Base):
    __tablename__ = 'health_notes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    date = Column(Date)
    title = Column(String(200))
    content = Column(Text)


class BabyKick(Base):
    __tablename__ = 'baby_kicks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    date = Column(Date)
    time = Column(Time)
    count = Column(Integer)


class Contraction(Base):
    __tablename__ = 'contractions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    duration = Column(Integer)
    intensity = Column(Integer)


class BloodPressure(Base):
    __tablename__ = 'blood_pressure'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    date = Column(Date)
    time = Column(Time)
    systolic = Column(Integer)
    diastolic = Column(Integer)
    pulse = Column(Integer)
    notes = Column(Text)


class BellyMeasurement(Base):
    __tablename__ = 'belly_measurements'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    date = Column(Date)
    measurement = Column(Float)
    notes = Column(Text)


class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    title = Column(String(200))
    description = Column(Text)
    reminder_date = Column(Date)
    reminder_time = Column(Time)
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    reminder_type = Column(String(50), default='custom')
    created_at = Column(DateTime, default=datetime.utcnow)