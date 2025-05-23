from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base, UserProfile, PregnancyData, DietPreference, WeightRecord, MedicalCheck, \
    WishlistItem, HealthNote, BabyKick, Contraction, BloodPressure, BellyMeasurement
from .data import DEFAULT_MEDICAL_CHECKS
from datetime import datetime, date, timedelta


class Database:
    def __init__(self, db_path='pregnancy_diary.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self._init_default_data()

    def _init_default_data(self):
        if not self.session.query(UserProfile).first():
            user = UserProfile(id=1, name="", height=165, weight_before_pregnancy=60.0,
                               previous_pregnancies=0, cycle_length=28)
            self.session.add(user)

        if not self.session.query(PregnancyData).first():
            pregnancy = PregnancyData(id=1, baby_gender="Невідомо", baby_name="")
            self.session.add(pregnancy)

        if not self.session.query(MedicalCheck).first():
            for check_data in DEFAULT_MEDICAL_CHECKS:
                self.session.add(MedicalCheck(**check_data))

        self.session.commit()

    def get_user_profile(self):
        return self.session.query(UserProfile).first()

    def get_pregnancy_data(self):
        return self.session.query(PregnancyData).first()

    def get_diet_preferences(self):
        prefs = self.session.query(DietPreference).filter_by(user_id=1).all()
        return [pref.preference for pref in prefs]

    def update_diet_preferences(self, preferences):
        self.session.query(DietPreference).filter_by(user_id=1).delete()
        for pref in preferences:
            self.session.add(DietPreference(user_id=1, preference=pref))
        self.session.commit()

    def _parse_date_time(self, date_str, time_str=None):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        if time_str:
            time_obj = datetime.strptime(time_str, '%H:%M:%S' if ':' in time_str[2:] else '%H:%M').time()
            return date_obj, time_obj
        return date_obj

    def _add_record(self, model_class, **kwargs):
        record = model_class(**kwargs)
        self.session.add(record)
        self.session.commit()
        return record.id

    def _get_records(self, model_class, days=None, order_by=None, format_func=None):
        query = self.session.query(model_class)

        if days and hasattr(model_class, 'date'):
            start_date = date.today() - timedelta(days=days)
            query = query.filter(model_class.date >= start_date)

        if order_by:
            query = query.order_by(*order_by)

        records = query.all()
        return [format_func(r) for r in records] if format_func else records

    def add_weight_record(self, date_str, weight):
        date_obj = self._parse_date_time(date_str)
        return self._add_record(WeightRecord, date=date_obj, weight=weight)

    def get_weight_records(self):
        records = self._get_records(WeightRecord, order_by=[WeightRecord.date])
        return [(r.date.strftime('%Y-%m-%d'), r.weight) for r in records]

    def add_baby_kick(self, date_str, time_str, count):
        date_obj, time_obj = self._parse_date_time(date_str, time_str)
        return self._add_record(BabyKick, date=date_obj, time=time_obj, count=count)

    def get_baby_kicks(self, days=7):
        def format_kick(k):
            return {'id': k.id, 'date': k.date.strftime('%Y-%m-%d'),
                    'time': k.time.strftime('%H:%M'), 'count': k.count}

        return self._get_records(BabyKick, days=days,
                                 order_by=[BabyKick.date.desc(), BabyKick.time.desc()],
                                 format_func=format_kick)

    def add_contraction(self, date_str, start_time_str, end_time_str, duration, intensity):
        date_obj = self._parse_date_time(date_str)
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
        return self._add_record(Contraction, date=date_obj, start_time=start_time,
                                end_time=end_time, duration=duration, intensity=intensity)

    def get_contractions(self, days=1):
        def format_contraction(c):
            return {'id': c.id, 'date': c.date.strftime('%Y-%m-%d'),
                    'start_time': c.start_time.strftime('%H:%M:%S'),
                    'end_time': c.end_time.strftime('%H:%M:%S'),
                    'duration': c.duration, 'intensity': c.intensity}

        return self._get_records(Contraction, days=days,
                                 order_by=[Contraction.date.desc(), Contraction.start_time.desc()],
                                 format_func=format_contraction)

    def add_blood_pressure(self, date_str, time_str, systolic, diastolic, pulse=None, notes=''):
        date_obj, time_obj = self._parse_date_time(date_str, time_str)
        return self._add_record(BloodPressure, date=date_obj, time=time_obj, systolic=systolic,
                                diastolic=diastolic, pulse=pulse, notes=notes)

    def get_blood_pressure(self, days=30):
        def format_bp(r):
            return {'id': r.id, 'date': r.date.strftime('%Y-%m-%d'),
                    'time': r.time.strftime('%H:%M'), 'systolic': r.systolic,
                    'diastolic': r.diastolic, 'pulse': r.pulse, 'notes': r.notes}

        return self._get_records(BloodPressure, days=days,
                                 order_by=[BloodPressure.date.desc(), BloodPressure.time.desc()],
                                 format_func=format_bp)

    def add_belly_measurement(self, date_str, measurement, notes=''):
        date_obj = self._parse_date_time(date_str)
        return self._add_record(BellyMeasurement, date=date_obj, measurement=measurement, notes=notes)

    def get_belly_measurements(self):
        def format_measurement(m):
            return {'id': m.id, 'date': m.date.strftime('%Y-%m-%d'),
                    'measurement': m.measurement, 'notes': m.notes}

        return self._get_records(BellyMeasurement,
                                 order_by=[BellyMeasurement.date.desc()],
                                 format_func=format_measurement)

    def add_health_note(self, date_str, content, title=''):
        date_obj = self._parse_date_time(date_str)
        return self._add_record(HealthNote, date=date_obj, content=content, title=title)

    def get_health_notes(self):
        def format_note(n):
            return {'id': n.id, 'date': n.date.strftime('%Y-%m-%d'),
                    'content': n.content, 'title': n.title}

        return self._get_records(HealthNote,
                                 order_by=[HealthNote.date.desc()],
                                 format_func=format_note)

    def add_wishlist_item(self, title, description, category, price=None, priority=2):
        return self._add_record(WishlistItem, title=title, description=description,
                                category=category, price=price, priority=priority)

    def get_wishlist_items(self, category=None):
        query = self.session.query(WishlistItem)
        if category:
            query = query.filter_by(category=category)

        def format_item(i):
            return {'id': i.id, 'title': i.title, 'description': i.description,
                    'category': i.category, 'price': i.price, 'is_purchased': i.is_purchased,
                    'purchase_date': i.purchase_date.strftime('%Y-%m-%d') if i.purchase_date else None,
                    'priority': i.priority}

        return [format_item(item) for item in query.all()]

    def _update_item(self, model_class, item_id, **updates):
        item = self.session.query(model_class).filter_by(id=item_id).first()
        if item:
            for key, value in updates.items():
                setattr(item, key, value)
            self.session.commit()
            return True
        return False

    def mark_wishlist_item_purchased(self, item_id, purchase_date=None):
        return self._update_item(WishlistItem, item_id,
                                 is_purchased=True,
                                 purchase_date=purchase_date or date.today())

    def update_wishlist_item(self, item_id, title, description, category, price, priority, is_purchased):
        updates = {'title': title, 'description': description, 'category': category,
                   'price': price, 'priority': priority, 'is_purchased': is_purchased}

        if is_purchased:
            item = self.session.query(WishlistItem).filter_by(id=item_id).first()
            if item and not item.purchase_date:
                updates['purchase_date'] = date.today()
        else:
            updates['purchase_date'] = None

        return self._update_item(WishlistItem, item_id, **updates)

    def delete_wishlist_item(self, item_id):
        item = self.session.query(WishlistItem).filter_by(id=item_id).first()
        if item:
            self.session.delete(item)
            self.session.commit()
            return True
        return False

    def get_medical_checks_by_trimester(self, trimester):
        def format_check(c):
            return {'id': c.id, 'title': c.title, 'description': c.description,
                    'trimester': c.trimester, 'is_completed': c.is_completed,
                    'completion_date': c.completion_date.strftime('%Y-%m-%d') if c.completion_date else None,
                    'is_custom': c.is_custom}

        checks = self.session.query(MedicalCheck).filter_by(trimester=trimester).all()
        return [format_check(c) for c in checks]

    def complete_medical_check(self, check_id, completion_date=None):
        return self._update_item(MedicalCheck, check_id,
                                 is_completed=True,
                                 completion_date=completion_date or date.today())

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()