"""Данные для заполнения бд при запуске сервиса."""

TEMPLATES = [
    {
        # Шаблон формы "Контактная информация"
        'name': 'Contact Information',
        'fields': {'name': 'text', 'email': 'email', 'phone': 'phone'},
    },
    {
        # Шаблон формы "Регистрация"
        'name': 'Registration Form',
        'fields': {'username': 'text', 'email': 'email', 'password': 'text'},  # pragma: allowlist secret
    },
    {
        # Шаблон формы "Заказ товара"
        'name': 'Order Form',
        'fields': {'product_name': 'text', 'quantity': 'text', 'date': 'date', 'phone': 'phone'},
    },
    {
        # Шаблон формы "Отзыв"
        'name': 'Feedback Form',
        'fields': {'name': 'text', 'email': 'email', 'rating': 'text', 'comments': 'text'},
    },
    {
        # Шаблон формы "Email"
        'name': 'Email Form',
        'fields': {'to_email': 'text', 'subject': 'email', 'body': 'text', 'text': 'text'},
    },
]
