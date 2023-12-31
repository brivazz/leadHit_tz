"""Данные для заполнения бд при запуске сервиса."""


TEMPLATES = [
    {
        # Шаблон формы "Контактная информация"
        'name': 'Contact Information',
        'first_name': 'text',
        'email': 'email',
        'phone': 'phone',
    },
    {
        # Шаблон формы "Регистрация"
        'name': 'Registration Form',
        'username': 'text',
        'email': 'email',
        'password': 'text',  # pragma: allowlist secret
    },
    {
        # Шаблон формы "Заказ товара"
        'name': 'Order Form',
        'product_name': 'text',
        'quantity': 'text',
        'order_date': 'date',
        'user_phone': 'phone',
    },
    {
        # Шаблон формы "Отзыв"
        'name': 'Feedback Form',
        'username': 'text',
        'email': 'email',
        'rating': 'text',
        'comments': 'text',
    },
    {
        # Шаблон формы "Email"
        'name': 'Email Form',
        'to_email': 'email',
        'subject': 'text',
        'body': 'text',
    },
]
