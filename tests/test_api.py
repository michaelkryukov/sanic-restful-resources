import pytest
from sanic import Sanic
from schematics.models import Model
from schematics.types import StringType
from sanic_restful_resources import Api, resource, validate, error


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
