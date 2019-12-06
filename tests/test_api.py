import pytest
from sanic_restful_resources import Api, resource


@resource('/users')
class Users:
    pass


def test_warning():
    with pytest.warns(UserWarning):
        Api(url_prefix='/api/')


def test_replaced_url():
    api = Api()
    api.add_resource(Users, '/hotel/users')
    api.add_resource(Users, '/marketplace/users')
