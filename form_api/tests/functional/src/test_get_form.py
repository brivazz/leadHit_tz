import os
import sys
from http import HTTPStatus

import pytest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from settings import test_settings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            # получение шаблона формы "Контактная информация"
            {'first_name': 'text', 'email': 'email', 'phone': 'phone'},
            {'status': HTTPStatus.OK, 'name': 'Contact Information'},
        ),
        (
            # получение шаблона формы "Регистрация"
            {'username': 'text', 'email': 'email', 'password': 'text'},
            {'status': HTTPStatus.OK, 'name': 'Registration Form'},
        ),
        (
            # получение шаблона формы "Заказ товара"
            {'product_name': 'text', 'quantity': 'text', 'order_date': 'date', 'phone': 'phone'},
            {'status': HTTPStatus.OK, 'name': 'Order Form'},
        ),
        (
            # получение шаблона формы "Отзыв"
            {'username': 'text', 'email': 'email', 'rating': 'text', 'comments': 'text'},
            {'status': HTTPStatus.OK, 'name': 'Feedback Form'},
        ),
        (
            # получение шаблона формы "Email"
            {'to_email': 'text', 'subject': 'email', 'body': 'text'},
            {'status': HTTPStatus.OK, 'name': 'Email Form'},
        ),
    ],
)
async def test_form(make_get_request, query_data: dict, expected_answer: dict):
    url = f'{test_settings.service_url}/api/v1/get_form'
    message, status = await make_get_request(url, method='POST', data=query_data)

    assert message['name'] == expected_answer['name']
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            # получение шаблона формы согласно правил валидации
            {
                'field_name_1': 'date',
                'field_name_2': 'text',
                'field_name_3': 'email',
                'field_name_4': 'text',
                'field_name_5': 'date',
            },
            {
                'status': HTTPStatus.OK,
                'fields': {
                    'field_name_1': 'date',
                    'field_name_2': 'phone',
                    'field_name_3': 'email',
                    'field_name_4': 'text',
                    'field_name_5': 'date',
                },
            },
        ),
    ],
)
async def test_bad_form(make_get_request, query_data: dict, expected_answer: dict):
    url = f'{test_settings.service_url}/api/v1/get_form'
    message, status = await make_get_request(url, method='POST', data=query_data)

    assert status == expected_answer['status']
    assert message == expected_answer['fields']
