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
            # получение шаблона формы успешное
            {'date': '2023-12-31', 'phone': '+70123456789', 'email': 'tvori@dobro.org', 'text': 'hello world'},
            {'status': HTTPStatus.OK, 'name': 'Contact Information'},
        ),
        (
            # получение шаблона формы по полю дата и телефон
            {'date': '2023-12-12', 'phone': '+70123456789'},
            {'status': HTTPStatus.OK, 'name': 'Order Form'},
        ),
        (
            # получение шаблона формы успешное по полю email и телефон
            {'email': 'tvori@dobro.org', 'phone': '+70123456789'},
            {'status': HTTPStatus.OK, 'name': 'Contact Information'},
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
            # получение шаблона формы c невалидной датой
            {'date': '121212', 'phone': '', 'email': '', 'text': ''},
            {
                'status': HTTPStatus.BAD_REQUEST,
                'detail': "Invalid date format, should be 'DD.MM.YYYY' or 'YYYY-MM-DD'",
            },
        ),
        (
            # получение шаблона формы c невалидным номером телефона
            {'phone': '333 333', 'email': '', 'text': ''},
            {
                'status': HTTPStatus.BAD_REQUEST,
                'detail': "Phone number must be in format '+7 XXX XXX XX XX' without spaces",
            },
        ),
        (
            # получение шаблона формы c невалидным адресом электронной почты
            {'email': 'hello world', 'text': ''},
            {'status': HTTPStatus.BAD_REQUEST, 'detail': 'Invalid email address. Example: example@example.com'},
        ),
        (
            # получение шаблона формы согласно правил валидации
            {'text': 'spasibo'},
            {'status': HTTPStatus.OK, 'date': {'date': 'date'}},
        ),
    ],
)
async def test_bad_form(make_get_request, query_data: dict, expected_answer: dict):
    url = f'{test_settings.service_url}/api/v1/get_form'
    message, status = await make_get_request(url, method='POST', data=query_data)

    assert status == expected_answer['status']

    if status == HTTPStatus.BAD_REQUEST:
        assert message['detail'] == expected_answer['detail']
    else:
        assert message == expected_answer['date']
