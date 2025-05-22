from sqlalchemy import Column, Integer, String, Text, Boolean, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), default='Користувач')
    birth_date = Column(Date)
    height = Column(Integer, default=165)
    weight_before_pregnancy = Column(Float, default=60.0)
    previous_pregnancies = Column(Integer, default=0)
    cycle_length = Column(Integer, default=28)


class PregnancyData(Base):
    __tablename__ = 'pregnancy_data'

    id = Column(Integer, primary_key=True)
    last_period_date = Column(Date)
    due_date = Column(Date)
    conception_date = Column(Date)
    baby_gender = Column(String(20), default='Невідомо')
    baby_name = Column(String(100), default='')


class DietPreference(Base):
    __tablename__ = 'diet_preferences'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    preference = Column(String(100))


class WeightRecord(Base):
    __tablename__ = 'weight_records'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    weight = Column(Float)


class CalendarEvent(Base):
    __tablename__ = 'calendar_events'

    id = Column(Integer, primary_key=True)
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
    date = Column(Date)
    title = Column(String(200))
    content = Column(Text)


class BabyKick(Base):
    __tablename__ = 'baby_kicks'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    count = Column(Integer)


class Contraction(Base):
    __tablename__ = 'contractions'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    duration = Column(Integer)
    intensity = Column(Integer)


class BloodPressure(Base):
    __tablename__ = 'blood_pressure'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    systolic = Column(Integer)
    diastolic = Column(Integer)
    pulse = Column(Integer)
    notes = Column(Text)


class BellyMeasurement(Base):
    __tablename__ = 'belly_measurements'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    measurement = Column(Float)
    notes = Column(Text)