import traceback
import warnings
from functools import wraps
from sanic.blueprints import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView
from jwt.exceptions import InvalidTokenError
from sanic_jwt_extended.exceptions import InvalidHeaderError
from schematics.exceptions import DataError


class Api:
    """
    Object for incapsulating interactions with resource. This object
    stores bluprint, that actually responsible for routing and stuff.
    """

    def __init__(self, name='API', url_prefix=''):
        if url_prefix.endswith('/'):
            warnings.warn('You used "url_prefix" with trailing slash')

        self.blueprint = Blueprint(name, url_prefix=url_prefix)

    def init_app(self, app):
        app.blueprint(self.blueprint)

    def add_resource(self, res, new_uri=None, *args, **kwargs):
        if new_uri:
            uri = new_uri
        else:
            uri = res.uri

        self.blueprint.add_route(res.as_view(), uri, *args, **kwargs)


def _api_ok_response(response, status=200, **kwargs):
    return json(response, status=status, **kwargs)


def _api_err_response(description, details=None, status=500, **kwargs):
    response = {}

    if description:
        response['description'] = description

    if details:
        response['details'] = details

    return json(response, status=status, **kwargs)


def exceptions_middleware(method):
    """
    Middleware used to catch exceptions and sending users correct response
    with some information. This middleware also used to catch special
    exceptions to return correct data (for example, DataError from schematics)
    """

    async def method_with_try(*args, **kwargs):
        try:
            return await method(*args, **kwargs)
        except DataError as e:
            return _api_err_response(
                'Bad Request', e.to_primitive(), status=400
            )
        except InvalidTokenError:
            return _api_err_response(
                'Invalid JWT Token Provided', status=401
            )
        except InvalidHeaderError:
            return _api_err_response(
                'Invalid Header Provided', status=401
            )
        except Exception:
            traceback.print_exc()
            return _api_err_response('Internal Server Error')

    return method_with_try


def serializer_middleware(method):
    """
    Middleware to allow simple types of data to be returned from routes in
    resource.

    Possible return values:

        return "data", 200, {"X-Custom-Header": "Value"}
        return "data", 200
        return "data"
        return {"arg": "val"}
        return ["val1", "val2"]
        return "", 201

        return sanic.response.*
    """

    async def method_with_serialization(*args, **kwargs):
        response = await method(*args, **kwargs)
        response_kwargs = {'status': 200, 'headers': {}}

        if isinstance(response, tuple):
            if len(response) < 1 or len(response) > 3:
                raise ValueError(f'Wrong length of returned '
                                 f'response: {response}')

            if len(response) > 1:
                response_kwargs['status'] = response[1]

            if len(response) > 2:
                response_kwargs['headers'] = response[2]

            response = response[0]

        if isinstance(response, (list, dict, str)):
            return _api_ok_response(response, **response_kwargs)
        else:
            return response

    return method_with_serialization


DEFAULT_MIDDLEWARES = [
    exceptions_middleware,
    serializer_middleware,
]


def resource(uri=''):
    """
    Decorator that turn class to instance of resource. Resource bases
    decorated class and HTTPMethodView. You can (and should) specify uri
    for this resource (relative to api).
    """

    def decorator(cls):
        # Create new class based on passed class and HTTPMethodView.
        return type(f'resource({cls.__name__})', (cls, HTTPMethodView), {
            'uri': getattr(cls, 'uri', uri),
            'decorators': getattr(cls, 'decorators', DEFAULT_MIDDLEWARES),
        })
    return decorator


def validate(**models):
    """
    Decorator that makes method throw if any of passed models will
    fail validation. Coroutine only.

    Validated models will be passed after other args.
    """

    def decorator(method):
        @wraps(method)
        async def wrapper(self, request, *args, **kwargs):
            collected_args = collect_args(request)

            for output, model in models.items():
                instance = model(collected_args, strict=False)
                instance.validate()
                kwargs[output] = instance

            return await method(self, request, *args, **kwargs)

        return wrapper

    return decorator


def error(
    description=None,
    details=None,
    status=400,
    **kwargs
):
    return _api_err_response(
        description=description or '',
        details=details or {},
        status=status,
        **kwargs,
    )


def _save_value(store, key, value):
    if key[-2:] == '[]':
        store[key[:-2]] = value
    elif isinstance(value, (list, tuple)):
        store[key] = value[0]
    else:
        store[key] = value


def collect_args(request) -> dict:
    """Collect and return data from different places in request."""

    args = {}

    try:
        json_data = request.json
    except Exception:
        json_data = None

    if json_data and isinstance(json_data, dict):
        args.update(json_data)

    if request.args:
        for k, v in request.args.items():
            _save_value(args, k, v)

    if request.files:
        for k, v in request.files.items():
            _save_value(args, k, v)

    if request.form:
        for k, v in request.form.items():
            _save_value(args, k, v)

    return args
