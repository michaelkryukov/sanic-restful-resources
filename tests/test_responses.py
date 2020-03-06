import json
import pytest
import sanic
from sanic_restful_resources import (
    serializer_middleware, exceptions_middleware, error
)


def _get_description(body):
    return json.loads(body)['description']


def test_error_with_details():
    response = error('Bad Request', {'name': 'Field is required.'}, 400)

    assert response.status == 400
    assert json.loads(response.body) == {
        'description': 'Bad Request',
        'details': {'name': 'Field is required.'},
    }


async def test_exceptions():
    @exceptions_middleware
    async def f():
        raise Exception

    response = await f()
    assert response.status == 500
    assert _get_description(response.body) == 'Internal Server Error'


async def test_serialization():
    @serializer_middleware
    async def f():
        return 'Data', 200, {'X-Name': 'Ann'}

    response = await f()

    assert response.body == b'"Data"'
    assert response.status == 200
    assert response.headers['X-Name'] == 'Ann'


async def test_serialization_sanic():
    @serializer_middleware
    async def f():
        return sanic.response.json('Bruh')

    response = await f()

    assert response.body == b'"Bruh"'
    assert response.status == 200


async def test_bad_handler_response():
    @serializer_middleware
    async def f1():
        return ()

    with pytest.raises(ValueError):
        await f1()

    # ---

    @serializer_middleware
    async def f2():
        return (0, 0, 0, 0)

    with pytest.raises(ValueError):
        await f2()
