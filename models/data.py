DEFAULT_MEDICAL_CHECKS = [
    {
        'title': 'Загальний аналіз крові',
        'description': 'До 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Аналіз крові на групу та резус-фактор',
        'description': 'До 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Аналіз крові на ВІЛ',
        'description': 'До 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Аналіз крові на сифіліс',
        'description': 'До 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Загальний аналіз сечі',
        'description': 'До 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Аналіз на TORCH-інфекції',
        'description': 'До 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Перше скринінгове УЗД',
        'description': '11-13 тижнів',
        'trimester': 1,
        'recommended_week': 11,
        'deadline_week': 13
    },
    {
        'title': 'Гінеколог',
        'description': 'Перший візит до 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Терапевт',
        'description': 'До 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Стоматолог',
        'description': 'До 12 тижнів',
        'trimester': 1,
        'recommended_week': 8,
        'deadline_week': 12
    },
    {
        'title': 'Загальний аналіз крові',
        'description': '16-20 тижнів',
        'trimester': 2,
        'recommended_week': 16,
        'deadline_week': 20
    },
    {
        'title': 'Загальний аналіз сечі',
        'description': '16-20 тижнів',
        'trimester': 2,
        'recommended_week': 16,
        'deadline_week': 20
    },
    {
        'title': 'Глюкозотолерантний тест',
        'description': '24-28 тижнів',
        'trimester': 2,
        'recommended_week': 24,
        'deadline_week': 28
    },
    {
        'title': 'Друге скринінгове УЗД',
        'description': '18-22 тижнів',
        'trimester': 2,
        'recommended_week': 18,
        'deadline_week': 22
    },
    {
        'title': 'Гінеколог',
        'description': 'Кожні 4 тижні',
        'trimester': 2,
        'recommended_week': 16,
        'deadline_week': 20
    },
    {
        'title': 'Окуліст',
        'description': 'До 20 тижнів',
        'trimester': 2,
        'recommended_week': 16,
        'deadline_week': 20
    },
    {
        'title': 'Загальний аналіз крові',
        'description': '30 тижнів',
        'trimester': 3,
        'recommended_week': 30,
        'deadline_week': 32
    },
    {
        'title': 'Загальний аналіз сечі',
        'description': '30-32 тижнів',
        'trimester': 3,
        'recommended_week': 30,
        'deadline_week': 32
    },
    {
        'title': 'Аналіз крові на ВІЛ',
        'description': '30 тижнів',
        'trimester': 3,
        'recommended_week': 30,
        'deadline_week': 32
    },
    {
        'title': 'Аналіз крові на сифіліс',
        'description': '30 тижнів',
        'trimester': 3,
        'recommended_week': 30,
        'deadline_week': 32
    },
    {
        'title': 'Мазок на флору',
        'description': '30 тижнів',
        'trimester': 3,
        'recommended_week': 30,
        'deadline_week': 32
    },
    {
        'title': 'Третє скринінгове УЗД',
        'description': '32-34 тижнів',
        'trimester': 3,
        'recommended_week': 32,
        'deadline_week': 34
    },
    {
        'title': 'Доплерометрія',
        'description': '34-36 тижнів',
        'trimester': 3,
        'recommended_week': 34,
        'deadline_week': 36
    },
    {
        'title': 'Гінеколог',
        'description': 'Кожні 2 тижні до 36 тижня, потім щотижня',
        'trimester': 3,
        'recommended_week': 28,
        'deadline_week': 40
    },
    {
        'title': 'Консультація анестезіолога',
        'description': 'За 2-3 тижні до пологів',
        'trimester': 3,
        'recommended_week': 37,
        'deadline_week': 38
    }
]

CHECKLIST_DATA = {
    1: {
        "title": "I Триместр",
        "sections": [
            {
                "name": "Аналізи",
                "items": [
                    ("Загальний аналіз крові", "До 12 тижнів"),
                    ("Аналіз крові на групу та резус-фактор", "До 12 тижнів"),
                    ("Аналіз крові на ВІЛ", "До 12 тижнів"),
                    ("Аналіз крові на сифіліс", "До 12 тижнів"),
                    ("Загальний аналіз сечі", "До 12 тижнів"),
                    ("Аналіз на TORCH-інфекції", "До 12 тижнів"),
                ]
            },
            {
                "name": "УЗД",
                "items": [
                    ("Перше скринінгове УЗД", "11-13 тижнів")
                ]
            },
            {
                "name": "Консультації",
                "items": [
                    ("Гінеколог", "Перший візит до 12 тижнів"),
                    ("Терапевт", "До 12 тижнів"),
                    ("Стоматолог", "До 12 тижнів")
                ]
            }
        ]
    },
    2: {
        "title": "II Триместр",
        "sections": [
            {
                "name": "Аналізи",
                "items": [
                    ("Загальний аналіз крові", "16-20 тижнів"),
                    ("Загальний аналіз сечі", "16-20 тижнів"),
                    ("Глюкозотолерантний тест", "24-28 тижнів"),
                    ("Аналіз крові на RW", "20-22 тижні"),
                    ("Аналіз на групу крові", "16-18 тижнів"),
                    ("Аналіз на резус-фактор", "16-18 тижнів"),
                ]
            },
            {
                "name": "УЗД",
                "items": [
                    ("Друге скринінгове УЗД", "18-22 тижнів"),
                    ("Доплер-УЗД", "20-24 тижні")
                ]
            },
            {
                "name": "Консультації",
                "items": [
                    ("Гінеколог", "Кожні 4 тижні"),
                    ("Окуліст", "До 20 тижнів"),
                    ("Ендокринолог", "18-22 тижні"),
                    ("Терапевт", "20-24 тижні")
                ]
            },
            {
                "name": "Інше",
                "items": [
                    ("Придбати одяг для вагітних", "16-20 тижнів"),
                    ("Вибрати пологовий будинок", "18-24 тижні"),
                    ("Записатись на курси для вагітних", "20-24 тижні")
                ]
            }
        ]
    },
    3: {
        "title": "III Триместр",
        "sections": [
            {
                "name": "Аналізи",
                "items": [
                    ("Загальний аналіз крові", "30 тижнів"),
                    ("Загальний аналіз сечі", "30-32 тижнів"),
                    ("Аналіз крові на ВІЛ", "30 тижнів"),
                    ("Аналіз крові на сифіліс", "30 тижнів"),
                    ("Мазок на флору", "30 тижнів")
                ]
            },
            {
                "name": "УЗД",
                "items": [
                    ("Третє скринінгове УЗД", "32-34 тижнів"),
                    ("Доплерометрія", "34-36 тижнів")
                ]
            },
            {
                "name": "Консультації",
                "items": [
                    ("Гінеколог", "Кожні 2 тижні до 36 тижня, потім щотижня"),
                    ("Консультація анестезіолога", "За 2-3 тижні до пологів")
                ]
            }
        ]
    }
}