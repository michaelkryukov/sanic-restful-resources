from sanic import Sanic
from schematics.models import Model
from schematics.types import StringType
from sanic_restful_resources import Api, resource, validate, error


class UserPostSchema(Model):
    name = StringType(required=True)


@resource('/users')
class Users:
    async def get(self, request):
        return request.app.config.store

    @validate(user_data=UserPostSchema)
    async def post(self, request, user_data):
        request.app.config.store.append({'name': user_data.name})
        return '', 204


@resource('/users/<name>')
class User:
    async def get(self, request, name):
        for data in request.app.config.store:
            if data['name'] == name:
                return data

        return error('User not found', status=404)

    async def patch(self, request, name):
        return 1 / 0

    async def delete(self, request, name):
        for index, data in enumerate(request.app.config.store):
            if data['name'] == name:
                request.app.config.store.pop(index)
                return '', 204

        return error('User not found', status=404)


def make_app(store):
    app = Sanic(name='test')
    app.config.store = store

    api = Api(url_prefix='/api')
    api.add_resource(Users)
    api.add_resource(User)
    api.init_app(app)

    return app


def test_happy_path():
    app = make_app([{'name': 'Michael'}, {'name': 'Ivan'}])

    req, res = app.test_client.get('/api/users')
    assert res.json == [{'name': 'Michael'}, {'name': 'Ivan'}]

    req, res = app.test_client.post('/api/users')
    assert res.status == 400
    assert res.json == {
        'description': 'Bad Request',
        'details': {'name': ['This field is required.']}
    }

    req, res = app.test_client.post('/api/users', data={'name': 'Yan'})
    assert res.status == 204
    assert res.body == b''

    req, res = app.test_client.get('/api/users')
    assert res.json
    assert len(res.json) == 3

    req, res = app.test_client.get('/api/users/Yan')
    assert res.json == {'name': 'Yan'}

    req, res = app.test_client.delete('/api/users/Yan')
    assert res.status == 204
    assert res.body == b''

    req, res = app.test_client.delete('/api/users/Yan')
    assert res.status == 404

    req, res = app.test_client.get('/api/users')
    assert res.json
    assert len(res.json) == 2

    req, res = app.test_client.get('/api/users/Yan')
    assert res.json == {'description': 'User not found'}

    req, res = app.test_client.patch('/api/users/Yan')
    assert res.status == 500
    assert res.json == {'description': 'Internal Server Error'}
