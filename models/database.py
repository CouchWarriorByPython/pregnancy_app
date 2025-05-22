from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base, UserProfile, PregnancyData, DietPreference, WeightRecord, MedicalCheck, \
    WishlistItem, HealthNote, BabyKick, Contraction, BloodPressure, BellyMeasurement
from .data import DEFAULT_MEDICAL_CHECKS
from datetime import datetime, date


class Database:
    def __init__(self, db_path='pregnancy_diary.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self._init_default_data()

    def _init_default_data(self):
        if not self.session.query(UserProfile).first():
            user = UserProfile(
                id=1,
                name="",  # Порожнє ім'я для першого запуску
                height=165,
                weight_before_pregnancy=60.0,
                previous_pregnancies=0,
                cycle_length=28
            )
            self.session.add(user)

        if not self.session.query(PregnancyData).first():
            pregnancy = PregnancyData(
                id=1,
                baby_gender="Невідомо",  # Явно встановлюємо для першого запуску
                baby_name=""
            )
            self.session.add(pregnancy)

        if not self.session.query(MedicalCheck).first():
            for check_data in DEFAULT_MEDICAL_CHECKS:
                check = MedicalCheck(**check_data)
                self.session.add(check)

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
            diet_pref = DietPreference(user_id=1, preference=pref)
            self.session.add(diet_pref)
        self.session.commit()

    def add_weight_record(self, date_str, weight):
        record = WeightRecord(date=datetime.strptime(date_str, '%Y-%m-%d').date(), weight=weight)
        self.session.add(record)
        self.session.commit()
        return record.id

    def get_weight_records(self):
        records = self.session.query(WeightRecord).order_by(WeightRecord.date).all()
        return [(record.date.strftime('%Y-%m-%d'), record.weight) for record in records]

    def add_baby_kick(self, date_str, time_str, count):
        kick = BabyKick(
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            time=datetime.strptime(time_str, '%H:%M').time(),
            count=count
        )
        self.session.add(kick)
        self.session.commit()
        return kick.id

    def get_baby_kicks(self, days=7):
        from datetime import timedelta
        start_date = date.today() - timedelta(days=days)
        kicks = self.session.query(BabyKick).filter(BabyKick.date >= start_date).order_by(BabyKick.date.desc(),
                                                                                          BabyKick.time.desc()).all()
        return [{'id': k.id, 'date': k.date.strftime('%Y-%m-%d'), 'time': k.time.strftime('%H:%M'), 'count': k.count}
                for k in kicks]

    def add_contraction(self, date_str, start_time_str, end_time_str, duration, intensity):
        contraction = Contraction(
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            start_time=datetime.strptime(start_time_str, '%H:%M:%S').time(),
            end_time=datetime.strptime(end_time_str, '%H:%M:%S').time(),
            duration=duration,
            intensity=intensity
        )
        self.session.add(contraction)
        self.session.commit()
        return contraction.id

    def get_contractions(self, days=1):
        from datetime import timedelta
        start_date = date.today() - timedelta(days=days)
        contractions = self.session.query(Contraction).filter(Contraction.date >= start_date).order_by(
            Contraction.date.desc(), Contraction.start_time.desc()).all()
        return [{'id': c.id, 'date': c.date.strftime('%Y-%m-%d'), 'start_time': c.start_time.strftime('%H:%M:%S'),
                 'end_time': c.end_time.strftime('%H:%M:%S'), 'duration': c.duration, 'intensity': c.intensity} for c in
                contractions]

    def add_blood_pressure(self, date_str, time_str, systolic, diastolic, pulse=None, notes=''):
        bp = BloodPressure(
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            time=datetime.strptime(time_str, '%H:%M').time(),
            systolic=systolic,
            diastolic=diastolic,
            pulse=pulse,
            notes=notes
        )
        self.session.add(bp)
        self.session.commit()
        return bp.id

    def get_blood_pressure(self, days=30):
        from datetime import timedelta
        start_date = date.today() - timedelta(days=days)
        records = self.session.query(BloodPressure).filter(BloodPressure.date >= start_date).order_by(
            BloodPressure.date.desc(), BloodPressure.time.desc()).all()
        return [
            {'id': r.id, 'date': r.date.strftime('%Y-%m-%d'), 'time': r.time.strftime('%H:%M'), 'systolic': r.systolic,
             'diastolic': r.diastolic, 'pulse': r.pulse, 'notes': r.notes} for r in records]

    def add_belly_measurement(self, date_str, measurement, notes=''):
        belly = BellyMeasurement(
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            measurement=measurement,
            notes=notes
        )
        self.session.add(belly)
        self.session.commit()
        return belly.id

    def get_belly_measurements(self):
        measurements = self.session.query(BellyMeasurement).order_by(BellyMeasurement.date.desc()).all()
        return [{'id': m.id, 'date': m.date.strftime('%Y-%m-%d'), 'measurement': m.measurement, 'notes': m.notes} for m
                in measurements]

    def add_health_note(self, date_str, content, title=''):
        note = HealthNote(
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            content=content,
            title=title
        )
        self.session.add(note)
        self.session.commit()
        return note.id

    def get_health_notes(self):
        notes = self.session.query(HealthNote).order_by(HealthNote.date.desc()).all()
        return [{'id': n.id, 'date': n.date.strftime('%Y-%m-%d'), 'content': n.content, 'title': n.title} for n in
                notes]

    def add_wishlist_item(self, title, description, category, price=None, priority=2):
        item = WishlistItem(
            title=title,
            description=description,
            category=category,
            price=price,
            priority=priority
        )
        self.session.add(item)
        self.session.commit()
        return item.id

    def get_wishlist_items(self, category=None):
        query = self.session.query(WishlistItem)
        if category:
            query = query.filter_by(category=category)
        items = query.all()
        return [{'id': i.id, 'title': i.title, 'description': i.description, 'category': i.category, 'price': i.price,
                 'is_purchased': i.is_purchased,
                 'purchase_date': i.purchase_date.strftime('%Y-%m-%d') if i.purchase_date else None,
                 'priority': i.priority} for i in items]

    def mark_wishlist_item_purchased(self, item_id, purchase_date=None):
        if not purchase_date:
            purchase_date = date.today()
        item = self.session.query(WishlistItem).filter_by(id=item_id).first()
        if item:
            item.is_purchased = True
            item.purchase_date = purchase_date
            self.session.commit()

    def update_wishlist_item(self, item_id, title, description, category, price, priority, is_purchased):
        item = self.session.query(WishlistItem).filter_by(id=item_id).first()
        if item:
            item.title = title
            item.description = description
            item.category = category
            item.price = price
            item.priority = priority
            item.is_purchased = is_purchased

            if is_purchased and not item.purchase_date:
                item.purchase_date = date.today()
            elif not is_purchased:
                item.purchase_date = None

            self.session.commit()
            return True
        return False

    def delete_wishlist_item(self, item_id):
        item = self.session.query(WishlistItem).filter_by(id=item_id).first()
        if item:
            self.session.delete(item)
            self.session.commit()
            return True
        return False

    def get_medical_checks_by_trimester(self, trimester):
        checks = self.session.query(MedicalCheck).filter_by(trimester=trimester).all()
        return [{'id': c.id, 'title': c.title, 'description': c.description, 'trimester': c.trimester,
                 'is_completed': c.is_completed,
                 'completion_date': c.completion_date.strftime('%Y-%m-%d') if c.completion_date else None,
                 'is_custom': c.is_custom} for c in checks]

    def complete_medical_check(self, check_id, completion_date=None):
        if not completion_date:
            completion_date = date.today()
        check = self.session.query(MedicalCheck).filter_by(id=check_id).first()
        if check:
            check.is_completed = True
            check.completion_date = completion_date
            self.session.commit()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()