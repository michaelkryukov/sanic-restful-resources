from sanic import Sanic
from sanic_restful_resources import resource, Api

app = Sanic(name='repeater')
api = Api(url_prefix='/api')


@resource('/repeat/<word>')
class Repeater:
    async def get(self, request, word):
        return {
            'word': word
        }


api.add_resource(Repeater)

api.init_app(app)

if __name__ == '__main__':
    app.run(auto_reload=True)
