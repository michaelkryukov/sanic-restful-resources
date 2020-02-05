from sanic import Sanic
from schematics import Model
from schematics.types import StringType, IntType
from sanic_restful_resources import resource, Api, validate

app = Sanic(name='example')
api = Api(url_prefix='/api')


users = [{'name': 'Michael', 'age': 20}, {'name': 'Ivan', 'age': 30}]


class UserPostSchema(Model):
    name = StringType(required=True)


class UserGetSchema(Model):
    age = IntType()


class PaginationSchema(Model):
    limit = IntType(default=10)
    offset = IntType(default=0)


@resource('/users')
class Users:
    @staticmethod
    def _paginate_list(data, limit, offset):
        return data[limit * offset: limit * (offset + 1)]

    @validate(filters=UserGetSchema, pagination=PaginationSchema)
    async def get(self, request, filters, pagination):
        if filters.age is not None:
            filtered_users = list(
                filter(lambda user: user['age'] == filters.age, users)
            )
        else:
            filtered_users = users

        return self._paginate_list(
            data=filtered_users,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    @validate(user_data=UserPostSchema)
    async def post(self, request, user_data):
        users.append({'name': user_data.name})
        return '', 204


api.add_resource(Users)

api.init_app(app)

if __name__ == '__main__':
    app.run(auto_reload=True)
