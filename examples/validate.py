from sanic import Sanic
from schematics import Model
from schematics.types import StringType
from sanic_restful_resources import resource, Api, validate

app = Sanic(name='repeater')
api = Api(url_prefix='/api')


class RepeaterSchema(Model):
    word = StringType(required=True)


@resource('/repeat')
class Repeater:
    @validate(data=RepeaterSchema)
    async def get(self, request, data):
        return {
            'word': data.word
        }


api.add_resource(Repeater)

api.init_app(app)

if __name__ == '__main__':
    app.run(auto_reload=True)
