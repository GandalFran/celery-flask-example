import logging

from log import LOG

from celery import Celery

from config import APP_NAME

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Resource, reqparse
from werkzeug.exceptions import BadRequest, NotFound

# flask configuration
app = Flask(APP_NAME)
app.config.from_object('config')
api = Api(app, version=app.config['VERSION'], title=app.config['TITLE'], description=app.config['DESCRIPTION'])
apiv1 = api.namespace('v1', description=app.config['DESCRIPTION'])

# flask anti CORS policy configuration
CORS(app)

# celery configuration
celery = Celery(app.config['APP_NAME'], broker=app.config['CELERY_BROKER'], backend=app.config['CELERY_BACKEND'])


@api.errorhandler(BadRequest)
def handle_bad_request_exception(error):
    return {"message": str(error)}, 403


@api.errorhandler(NotFound)
def handle_not_found_exception(error):
    return {"message": "resource not found"}, 404


@api.errorhandler
def default_error_handler():
    return {"message": "Unknown error occured"}, 500


@apiv1.route("/")
class CheckStatus(Resource):
    """check status"""

    def get(self):
        return {"status": "OK"}


@apiv1.route("/sum")
@apiv1.doc(params={'num1': 'int', 'num2': 'int'})
class SumEndpoint(Resource):
    """sum two numbers"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_parser = self._define_args_parser(location='args')
        self.post_parser = self._define_args_parser(location='form')

    def get(self):
        """sums two numbers and return result"""
        num1, num2 = self._get_args(self.get_parser)
        # throw the task (WARNING: not to be confused with do_sum_and_return_result(num1, num2), because this would)
        # call the method in local without passing throw celery.
        task = do_sum_and_return_result.delay(num1, num2)
        # wait for the task to complete
        task.wait()
        # retrieve the result
        result = task.result
        return {
            "status": task.status,
            "result": result
        }

    def post(self):
        """sums two numbers"""
        num1, num2 = self._get_args(self.post_parser)
        task = do_sum_and_print_result.delay(num1, num2)
        return {
            "status": task.status,
        }

    def _get_args(self, args_parser):
        args = args_parser.parse_args()
        num1 = args['num1']
        num2 = args['num2']
        return num1, num2

    @classmethod
    def _define_args_parser(cls, location=None):
        parser = reqparse.RequestParser()
        parser.add_argument('num1', required=True, type=int, location=location)
        parser.add_argument('num2', required=True, type=int, location=location)
        return parser


@celery.task
def do_sum_and_return_result(number1, number2):
    result = int(number1) + int(number2)
    return result


@celery.task
def do_sum_and_print_result(number1, number2):
    result = int(number1) + int(number2)
    LOG.log(logging.WARNING, "this is printed because loglevel is set in each worker cluster")
    LOG.log(logging.WARNING, f" {number1} + {number2} = {result}")
