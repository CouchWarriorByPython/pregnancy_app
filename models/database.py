from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base, UserProfile, PregnancyData, WeightRecord, \
    WishlistItem, HealthNote, BabyKick, Contraction, BloodPressure, BellyMeasurement, Reminder
from datetime import datetime, date, timedelta
from models.base import CalendarEvent


class Database:
    def __init__(self, db_path='pregnancy_diary.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_user_profile(self, user_id):
        return self.session.query(UserProfile).filter_by(id=user_id).first()

    def get_pregnancy_data(self, user_id):
        return self.session.query(PregnancyData).filter_by(user_id=user_id).first()

    def create_pregnancy_data(self, user_id):
        """Створює новий запис даних про вагітність для користувача"""
        pregnancy = PregnancyData(user_id=user_id, baby_gender="Невідомо", baby_name="")
        self.session.add(pregnancy)
        self.session.commit()
        return pregnancy

    def _parse_date_time(self, date_str, time_str=None):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            if time_str:
                # Спочатку пробуємо формат HH:MM, потім HH:MM:SS
                try:
                    time_obj = datetime.strptime(time_str, '%H:%M').time()
                except ValueError:
                    time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
                return date_obj, time_obj
            return date_obj
        except ValueError:
            raise ValueError("Невірний формат дати або часу")

    def _add_record(self, model_class, user_id, **kwargs):
        if not user_id:
            raise ValueError("user_id є обов'язковим")
        kwargs['user_id'] = user_id
        record = model_class(**kwargs)
        self.session.add(record)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Помилка при збереженні даних: {str(e)}")
        return record.id

    def _get_records(self, model_class, user_id, days=None, order_by=None, format_func=None):
        if not user_id:
            raise ValueError("user_id є обов'язковим")

        query = self.session.query(model_class).filter_by(user_id=user_id)

        if days and hasattr(model_class, 'date'):
            start_date = date.today() - timedelta(days=days)
            query = query.filter(model_class.date >= start_date)

        if order_by:
            query = query.order_by(*order_by)

        records = query.all()
        return [format_func(r) for r in records] if format_func else records

    def add_weight_record(self, date_str, weight, user_id):
        if weight <= 0 or weight > 300:
            raise ValueError("Недійсне значення ваги (має бути від 0 до 300 кг)")
        
        date_obj = self._parse_date_time(date_str)
        existing = self.session.query(WeightRecord).filter_by(
            user_id=user_id, 
            date=date_obj
        ).first()
        if existing:
            raise ValueError("Запис ваги на цю дату вже існує")
        
        return self._add_record(WeightRecord, user_id, date=date_obj, weight=weight)

    def get_weight_records(self, user_id):
        records = self._get_records(WeightRecord, user_id=user_id, order_by=[WeightRecord.date])
        return [(r.date.strftime('%Y-%m-%d'), r.weight) for r in records]

    def add_baby_kick(self, date_str, time_str, count, user_id):
        if count <= 0 or count > 100:
            raise ValueError("Недійсна кількість рухів (має бути від 1 до 100)")
        
        date_obj, time_obj = self._parse_date_time(date_str, time_str)
        return self._add_record(BabyKick, user_id, date=date_obj, time=time_obj, count=count)

    def get_baby_kicks(self, user_id, days=7):
        def format_kick(k):
            return {'id': k.id, 'date': k.date.strftime('%Y-%m-%d'),
                    'time': k.time.strftime('%H:%M'), 'count': k.count}

        return self._get_records(BabyKick, user_id=user_id, days=days,
                                 order_by=[BabyKick.date.desc(), BabyKick.time.desc()],
                                 format_func=format_kick)

    def add_contraction(self, date_str, start_time_str, end_time_str, duration, intensity, user_id):
        if duration <= 0 or duration > 300:
            raise ValueError("Недійсна тривалість скорочення (має бути від 1 до 300 секунд)")
        if intensity < 1 or intensity > 10:
            raise ValueError("Недійсна інтенсивність (має бути від 1 до 10)")
        
        date_obj = self._parse_date_time(date_str)
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
        return self._add_record(Contraction, user_id, date=date_obj, start_time=start_time,
                              end_time=end_time, duration=duration, intensity=intensity)

    def get_contractions(self, user_id, days=1):
        def format_contraction(c):
            return {'id': c.id, 'date': c.date.strftime('%Y-%m-%d'),
                    'start_time': c.start_time.strftime('%H:%M:%S'),
                    'end_time': c.end_time.strftime('%H:%M:%S'),
                    'duration': c.duration, 'intensity': c.intensity}

        return self._get_records(Contraction, user_id=user_id, days=days,
                                 order_by=[Contraction.date.desc(), Contraction.start_time.desc()],
                                 format_func=format_contraction)

    def add_blood_pressure(self, date_str, time_str, systolic, diastolic, pulse=None, notes='', user_id=None):
        if systolic <= 0 or systolic > 300:
            raise ValueError("Недійсне значення систолічного тиску")
        if diastolic <= 0 or diastolic > 200:
            raise ValueError("Недійсне значення діастолічного тиску")
        if pulse is not None and (pulse <= 0 or pulse > 250):
            raise ValueError("Недійсне значення пульсу")
        
        date_obj, time_obj = self._parse_date_time(date_str, time_str)
        return self._add_record(BloodPressure, user_id, date=date_obj, time=time_obj, 
                              systolic=systolic, diastolic=diastolic, pulse=pulse, notes=notes)

    def get_blood_pressure(self, user_id, days=30):
        def format_bp(r):
            return {'id': r.id, 'date': r.date.strftime('%Y-%m-%d'),
                    'time': r.time.strftime('%H:%M'), 'systolic': r.systolic,
                    'diastolic': r.diastolic, 'pulse': r.pulse, 'notes': r.notes}

        return self._get_records(BloodPressure, user_id=user_id, days=days,
                                 order_by=[BloodPressure.date.desc(), BloodPressure.time.desc()],
                                 format_func=format_bp)

    def add_belly_measurement(self, date_str, measurement, notes='', user_id=None):
        if measurement <= 0 or measurement > 200:
            raise ValueError("Недійсне значення виміру (має бути від 1 до 200 см)")
        
        date_obj = self._parse_date_time(date_str)
        existing = self.session.query(BellyMeasurement).filter_by(
            user_id=user_id, 
            date=date_obj
        ).first()
        if existing:
            raise ValueError("Вимір на цю дату вже існує")
        
        return self._add_record(BellyMeasurement, user_id, date=date_obj, measurement=measurement, notes=notes)

    def get_belly_measurements(self, user_id):
        def format_measurement(m):
            return {'id': m.id, 'date': m.date.strftime('%Y-%m-%d'),
                    'measurement': m.measurement, 'notes': m.notes}

        return self._get_records(BellyMeasurement, user_id=user_id,
                                 order_by=[BellyMeasurement.date.desc()],
                                 format_func=format_measurement)

    def add_health_note(self, date_str, content, title='', user_id=None):
        date_obj = self._parse_date_time(date_str)
        return self._add_record(HealthNote, user_id, date=date_obj, content=content, title=title)

    def get_health_notes(self, user_id):
        def format_note(n):
            return {'id': n.id, 'date': n.date.strftime('%Y-%m-%d'),
                    'content': n.content, 'title': n.title}

        return self._get_records(HealthNote, user_id=user_id,
                                 order_by=[HealthNote.date.desc()],
                                 format_func=format_note)

    def add_wishlist_item(self, title, description, category, price=None, priority=2, user_id=None):
        if not title or len(title.strip()) == 0:
            raise ValueError("Назва елемента не може бути порожньою")
        if price is not None and (price < 0 or price > 1000000):
            raise ValueError("Недійсна ціна (має бути від 0 до 1000000)")
        if priority < 1 or priority > 3:
            raise ValueError("Недійсний пріоритет (має бути від 1 до 3)")
        
        return self._add_record(WishlistItem, user_id, title=title, description=description,
                              category=category, price=price, priority=priority)

    def get_wishlist_items(self, user_id, category=None):
        query = self.session.query(WishlistItem).filter_by(user_id=user_id)
        if category:
            query = query.filter_by(category=category)

        def format_item(i):
            return {'id': i.id, 'title': i.title, 'description': i.description,
                    'category': i.category, 'price': i.price, 'is_purchased': i.is_purchased,
                    'purchase_date': i.purchase_date.strftime('%Y-%m-%d') if i.purchase_date else None,
                    'priority': i.priority}

        return [format_item(item) for item in query.all()]

    def _update_item(self, model_class, item_id, user_id, **updates):
        item = self.session.query(model_class).filter_by(id=item_id, user_id=user_id).first()
        if item:
            for key, value in updates.items():
                setattr(item, key, value)
            self.session.commit()
            return True
        return False

    def mark_wishlist_item_purchased(self, item_id, user_id, purchase_date=None):
        return self._update_item(WishlistItem, item_id, user_id=user_id,
                                 is_purchased=True,
                                 purchase_date=purchase_date or date.today())

    def update_wishlist_item(self, item_id, title, description, category, price, priority, is_purchased, user_id):
        if not title or len(title.strip()) == 0:
            raise ValueError("Назва елемента не може бути порожньою")
        if price is not None and (price < 0 or price > 1000000):
            raise ValueError("Недійсна ціна (має бути від 0 до 1000000)")
        if priority < 1 or priority > 3:
            raise ValueError("Недійсний пріоритет (має бути від 1 до 3)")
        
        item = self.session.query(WishlistItem).filter_by(id=item_id, user_id=user_id).first()
        if not item:
            raise ValueError("Елемент не знайдено")
        
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
        
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Помилка при оновленні даних: {str(e)}")

    def delete_wishlist_item(self, item_id, user_id):
        item = self.session.query(WishlistItem).filter_by(id=item_id, user_id=user_id).first()
        if not item:
            raise ValueError("Елемент не знайдено")
        
        try:
            self.session.delete(item)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Помилка при видаленні елемента: {str(e)}")

    def add_reminder(self, title, description, reminder_date, reminder_time, reminder_type='custom', user_id=None):
        if not title or len(title.strip()) == 0:
            raise ValueError("Назва нагадування не може бути порожньою")
        
        date_obj = self._parse_date_time(reminder_date)
        time_obj = datetime.strptime(reminder_time, '%H:%M').time()
        
        # Перевірка, чи нагадування не в минулому
        reminder_datetime = datetime.combine(date_obj, time_obj)
        if reminder_datetime < datetime.now():
            raise ValueError("Не можна створити нагадування в минулому")
        
        return self._add_record(Reminder, user_id, title=title, description=description,
                              reminder_date=date_obj, reminder_time=time_obj,
                              reminder_type=reminder_type)

    def get_active_reminders(self, user_id):
        def format_reminder(r):
            return {'id': r.id, 'title': r.title, 'description': r.description,
                    'reminder_date': r.reminder_date.strftime('%Y-%m-%d'),
                    'reminder_time': r.reminder_time.strftime('%H:%M'),
                    'reminder_type': r.reminder_type, 'is_completed': r.is_completed}

        reminders = self.session.query(Reminder).filter_by(user_id=user_id, is_active=True).all()
        return [format_reminder(r) for r in reminders]

    def complete_reminder(self, reminder_id, user_id):
        reminder = self.session.query(Reminder).filter_by(id=reminder_id, user_id=user_id).first()
        if not reminder:
            raise ValueError("Нагадування не знайдено")
        
        if not reminder.is_active:
            raise ValueError("Нагадування вже неактивне")
        
        reminder.is_completed = True
        reminder.is_active = False
        
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Помилка при оновленні нагадування: {str(e)}")

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    def add_calendar_event(self, title, description, start_date, start_time=None, end_time=None, event_type='regular',
                           user_id=None):
        if not title or len(title.strip()) == 0:
            raise ValueError("Назва події не може бути порожньою")
        
        date_obj = self._parse_date_time(start_date)
        
        # Парсимо час якщо він переданий
        start_time_obj = None
        end_time_obj = None
        all_day = True
        
        if start_time:
            if isinstance(start_time, str):
                start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            else:
                start_time_obj = start_time
            all_day = False
            
            # Якщо немає часу закінчення, додаємо годину до початку
            if not end_time:
                start_datetime = datetime.combine(date_obj, start_time_obj)
                end_datetime = start_datetime + timedelta(hours=1)
                end_time_obj = end_datetime.time()
            elif isinstance(end_time, str):
                end_time_obj = datetime.strptime(end_time, '%H:%M').time()
            else:
                end_time_obj = end_time
            
            # Перевірка, чи час закінчення після часу початку
            if end_time_obj <= start_time_obj:
                raise ValueError("Час закінчення має бути після часу початку")
        
        # Перевірка на дублікати подій
        existing = self.session.query(CalendarEvent).filter_by(
            user_id=user_id,
            start_date=date_obj,
            start_time=start_time_obj
        ).first()
        if existing:
            raise ValueError("Подія на цей час вже існує")
        
        event = CalendarEvent(
            user_id=user_id,
            title=title,
            description=description,
            start_date=date_obj,
            end_date=date_obj,
            start_time=start_time_obj,
            end_time=end_time_obj,
            all_day=all_day,
            event_type=event_type
        )
        
        try:
            self.session.add(event)
            self.session.commit()
            return event.id
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Помилка при створенні події: {str(e)}")

    def get_events_for_date(self, date_str, user_id):
        """Отримує події для конкретної дати та користувача"""
        if not user_id:
            raise ValueError("user_id є обов'язковим")

        date_obj = self._parse_date_time(date_str)
        events = self.session.query(CalendarEvent).filter_by(
            user_id=user_id,
            start_date=date_obj
        ).all()

        result = []
        for e in events:
            event_dict = {
                'id': e.id,
                'title': e.title,
                'description': e.description,
                'event_type': e.event_type,
                'all_day': e.all_day
            }

            # Додаємо час якщо подія не на весь день
            if not e.all_day and e.start_time:
                event_dict['time'] = e.start_time.strftime('%H:%M')
                if e.end_time:
                    event_dict['end_time'] = e.end_time.strftime('%H:%M')
            else:
                event_dict['time'] = 'Весь день'

            result.append(event_dict)

        return sorted(result, key=lambda x: x.get('time', ''))

    # Методи для роботи з чекліст даними
    def save_checklist_state(self, user_id, trimester, section, item_text, is_checked):
        """Зберігає стан елемента чекліста"""
        if not user_id:
            raise ValueError("user_id є обов'язковим")
        if trimester not in [1, 2, 3]:
            raise ValueError("Недійсний триместр (має бути 1, 2 або 3)")
        if not section or len(section.strip()) == 0:
            raise ValueError("Назва секції не може бути порожньою")
        if not item_text or len(item_text.strip()) == 0:
            raise ValueError("Текст пункту не може бути порожнім")
        
        from .base import ChecklistItem
        
        # Шукаємо існуючий запис
        existing = self.session.query(ChecklistItem).filter_by(
            user_id=user_id,
            trimester=trimester,
            section=section,
            item_text=item_text
        ).first()
        
        try:
            if existing:
                existing.is_checked = is_checked
            else:
                item = ChecklistItem(
                    user_id=user_id,
                    trimester=trimester,
                    section=section,
                    item_text=item_text,
                    is_checked=is_checked
                )
                self.session.add(item)
            
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Помилка при збереженні стану чекліста: {str(e)}")

    def get_checklist_state(self, user_id):
        """Отримує стан всіх елементів чекліста для користувача"""
        if not user_id:
            raise ValueError("user_id є обов'язковим")

        from .base import ChecklistItem

        items = self.session.query(ChecklistItem).filter_by(user_id=user_id).all()

        result = {}
        for item in items:
            key = f"{item.trimester}_{item.section}_{item.item_text}"
            result[key] = item.is_checked

        return result

    def clear_checklist_state(self, user_id, trimester=None):
        """Видаляє стан чекліста (всього або для конкретного триместру)"""
        if not user_id:
            raise ValueError("user_id є обов'язковим")

        from .base import ChecklistItem

        query = self.session.query(ChecklistItem).filter_by(user_id=user_id)

        if trimester:
            query = query.filter_by(trimester=trimester)

        query.delete()
        self.session.commit()
        return True