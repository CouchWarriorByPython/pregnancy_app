from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base, UserProfile, PregnancyData, WeightRecord, \
    WishlistItem, HealthNote, BabyKick, Contraction, BloodPressure, BellyMeasurement, Reminder
from datetime import datetime, date, timedelta


class Database:
    def __init__(self, db_path='pregnancy_diary.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_user_profile(self, user_id):
        return self.session.query(UserProfile).filter_by(id=user_id).first()

    def get_pregnancy_data(self, user_id):
        pregnancy = self.session.query(PregnancyData).filter_by(user_id=user_id).first()
        if not pregnancy:
            pregnancy = PregnancyData(user_id=user_id, baby_gender="Невідомо", baby_name="")
            self.session.add(pregnancy)
            self.session.commit()
        return pregnancy

    def _parse_date_time(self, date_str, time_str=None):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        if time_str:
            time_obj = datetime.strptime(time_str, '%H:%M:%S' if ':' in time_str[2:] else '%H:%M').time()
            return date_obj, time_obj
        return date_obj

    def _add_record(self, model_class, **kwargs):
        if 'user_id' not in kwargs:
            kwargs['user_id'] = 1
        record = model_class(**kwargs)
        self.session.add(record)
        self.session.commit()
        return record.id

    def _get_records(self, model_class, user_id=1, days=None, order_by=None, format_func=None):
        query = self.session.query(model_class).filter_by(user_id=user_id)

        if days and hasattr(model_class, 'date'):
            start_date = date.today() - timedelta(days=days)
            query = query.filter(model_class.date >= start_date)

        if order_by:
            query = query.order_by(*order_by)

        records = query.all()
        return [format_func(r) for r in records] if format_func else records

    def add_weight_record(self, date_str, weight, user_id=1):
        date_obj = self._parse_date_time(date_str)
        return self._add_record(WeightRecord, date=date_obj, weight=weight, user_id=user_id)

    def get_weight_records(self, user_id=1):
        records = self._get_records(WeightRecord, user_id=user_id, order_by=[WeightRecord.date])
        return [(r.date.strftime('%Y-%m-%d'), r.weight) for r in records]

    def add_baby_kick(self, date_str, time_str, count, user_id=1):
        date_obj, time_obj = self._parse_date_time(date_str, time_str)
        return self._add_record(BabyKick, date=date_obj, time=time_obj, count=count, user_id=user_id)

    def get_baby_kicks(self, user_id=1, days=7):
        def format_kick(k):
            return {'id': k.id, 'date': k.date.strftime('%Y-%m-%d'),
                    'time': k.time.strftime('%H:%M'), 'count': k.count}

        return self._get_records(BabyKick, user_id=user_id, days=days,
                                 order_by=[BabyKick.date.desc(), BabyKick.time.desc()],
                                 format_func=format_kick)

    def add_contraction(self, date_str, start_time_str, end_time_str, duration, intensity, user_id=1):
        date_obj = self._parse_date_time(date_str)
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
        return self._add_record(Contraction, date=date_obj, start_time=start_time,
                                end_time=end_time, duration=duration, intensity=intensity, user_id=user_id)

    def get_contractions(self, user_id=1, days=1):
        def format_contraction(c):
            return {'id': c.id, 'date': c.date.strftime('%Y-%m-%d'),
                    'start_time': c.start_time.strftime('%H:%M:%S'),
                    'end_time': c.end_time.strftime('%H:%M:%S'),
                    'duration': c.duration, 'intensity': c.intensity}

        return self._get_records(Contraction, user_id=user_id, days=days,
                                 order_by=[Contraction.date.desc(), Contraction.start_time.desc()],
                                 format_func=format_contraction)

    def add_blood_pressure(self, date_str, time_str, systolic, diastolic, pulse=None, notes='', user_id=1):
        date_obj, time_obj = self._parse_date_time(date_str, time_str)
        return self._add_record(BloodPressure, date=date_obj, time=time_obj, systolic=systolic,
                                diastolic=diastolic, pulse=pulse, notes=notes, user_id=user_id)

    def get_blood_pressure(self, user_id=1, days=30):
        def format_bp(r):
            return {'id': r.id, 'date': r.date.strftime('%Y-%m-%d'),
                    'time': r.time.strftime('%H:%M'), 'systolic': r.systolic,
                    'diastolic': r.diastolic, 'pulse': r.pulse, 'notes': r.notes}

        return self._get_records(BloodPressure, user_id=user_id, days=days,
                                 order_by=[BloodPressure.date.desc(), BloodPressure.time.desc()],
                                 format_func=format_bp)

    def add_belly_measurement(self, date_str, measurement, notes='', user_id=1):
        date_obj = self._parse_date_time(date_str)
        return self._add_record(BellyMeasurement, date=date_obj, measurement=measurement, notes=notes, user_id=user_id)

    def get_belly_measurements(self, user_id=1):
        def format_measurement(m):
            return {'id': m.id, 'date': m.date.strftime('%Y-%m-%d'),
                    'measurement': m.measurement, 'notes': m.notes}

        return self._get_records(BellyMeasurement, user_id=user_id,
                                 order_by=[BellyMeasurement.date.desc()],
                                 format_func=format_measurement)

    def add_health_note(self, date_str, content, title='', user_id=1):
        date_obj = self._parse_date_time(date_str)
        return self._add_record(HealthNote, date=date_obj, content=content, title=title, user_id=user_id)

    def get_health_notes(self, user_id=1):
        def format_note(n):
            return {'id': n.id, 'date': n.date.strftime('%Y-%m-%d'),
                    'content': n.content, 'title': n.title}

        return self._get_records(HealthNote, user_id=user_id,
                                 order_by=[HealthNote.date.desc()],
                                 format_func=format_note)

    def add_wishlist_item(self, title, description, category, price=None, priority=2, user_id=1):
        return self._add_record(WishlistItem, title=title, description=description,
                                category=category, price=price, priority=priority, user_id=user_id)

    def get_wishlist_items(self, user_id=1, category=None):
        query = self.session.query(WishlistItem).filter_by(user_id=user_id)
        if category:
            query = query.filter_by(category=category)

        def format_item(i):
            return {'id': i.id, 'title': i.title, 'description': i.description,
                    'category': i.category, 'price': i.price, 'is_purchased': i.is_purchased,
                    'purchase_date': i.purchase_date.strftime('%Y-%m-%d') if i.purchase_date else None,
                    'priority': i.priority}

        return [format_item(item) for item in query.all()]

    def _update_item(self, model_class, item_id, user_id=1, **updates):
        item = self.session.query(model_class).filter_by(id=item_id, user_id=user_id).first()
        if item:
            for key, value in updates.items():
                setattr(item, key, value)
            self.session.commit()
            return True
        return False

    def mark_wishlist_item_purchased(self, item_id, user_id=1, purchase_date=None):
        return self._update_item(WishlistItem, item_id, user_id=user_id,
                                 is_purchased=True,
                                 purchase_date=purchase_date or date.today())

    def update_wishlist_item(self, item_id, title, description, category, price, priority, is_purchased, user_id=1):
        updates = {'title': title, 'description': description, 'category': category,
                   'price': price, 'priority': priority, 'is_purchased': is_purchased}

        if is_purchased:
            item = self.session.query(WishlistItem).filter_by(id=item_id, user_id=user_id).first()
            if item and not item.purchase_date:
                updates['purchase_date'] = date.today()
        else:
            updates['purchase_date'] = None

        return self._update_item(WishlistItem, item_id, user_id=user_id, **updates)

    def delete_wishlist_item(self, item_id, user_id=1):
        item = self.session.query(WishlistItem).filter_by(id=item_id, user_id=user_id).first()
        if item:
            self.session.delete(item)
            self.session.commit()
            return True
        return False

    def add_reminder(self, title, description, reminder_date, reminder_time, reminder_type='custom', user_id=1):
        date_obj = self._parse_date_time(reminder_date)
        time_obj = datetime.strptime(reminder_time, '%H:%M').time()
        return self._add_record(Reminder, title=title, description=description,
                                reminder_date=date_obj, reminder_time=time_obj,
                                reminder_type=reminder_type, user_id=user_id)

    def get_active_reminders(self, user_id=1):
        def format_reminder(r):
            return {'id': r.id, 'title': r.title, 'description': r.description,
                    'reminder_date': r.reminder_date.strftime('%Y-%m-%d'),
                    'reminder_time': r.reminder_time.strftime('%H:%M'),
                    'reminder_type': r.reminder_type, 'is_completed': r.is_completed}

        reminders = self.session.query(Reminder).filter_by(user_id=user_id, is_active=True).all()
        return [format_reminder(r) for r in reminders]

    def complete_reminder(self, reminder_id, user_id=1):
        return self._update_item(Reminder, reminder_id, user_id=user_id, is_completed=True)

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()