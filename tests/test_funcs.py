import json
import pytest
import sanic
from jwt.exceptions import InvalidTokenError
from sanic_jwt_extended.exceptions import InvalidHeaderError
from sanic_restful_resources import (
    serializer_middleware, exceptions_middleware, error, collect_args
)


ARGS_KEY = (False, False, 'utf-8', 'replace')


def test_collect_args():
    request = sanic.request.Request(b'', {}, 0, '', '', None)

    request.parsed_json = {'key1': 'val'}
    request.parsed_args = {ARGS_KEY: {'key2': ['val']}}
    request.parsed_form = {'key3': ['val']}
    request.parsed_files = {'key4': [b'val']}

    data = collect_args(request)

    assert data == {
        'key1': 'val',
        'key2': 'val',
        'key3': 'val',
        'key4': b'val',
    }


def test_collect_args_with_list():
    request = sanic.request.Request(b'', {}, 0, '', '', None)

    request.parsed_args = {ARGS_KEY: {'key[]': ['val1', 'val2']}}

    data = collect_args(request)

    assert data == {'key': ['val1', 'val2'],}


def test_collect_args_safety_net():
    request = sanic.request.Request(b'', {}, 0, '', '', None)

    request.parsed_args = {ARGS_KEY: {'key': 'val'}}

    data = collect_args(request)

    assert data == {'key': 'val'}
