import sanic
from sanic_restful_resources import collect_args


ARGS_KEY = (False, False, 'utf-8', 'replace')


def make_request():
    return sanic.request.Request(b'https://ya.ru/', {}, 0, '', '', None)


def test_collect_args():
    request = make_request()

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
    request = make_request()

    request.parsed_args = {ARGS_KEY: {'key[]': ['val1', 'val2']}}

    data = collect_args(request)

    assert data == {'key': ['val1', 'val2']}


def test_collect_args_safety_net():
    request = make_request()

    request.parsed_args = {ARGS_KEY: {'key': 'val'}}

    data = collect_args(request)

    assert data == {'key': 'val'}
