from flask import Flask
from flask_restful import Api
from flask_restful.utils import cors

#   Need to check that app run under uWSGI context
#   In case of pytest we run out of uWSGI context then it can't
#   import uwsgi
import uwsgidecorators
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from splunk_otel.tracing import start_tracing


from resource.health_check import HealthCheck


def add_routes(router):
    router.add_resource(HealthCheck, "/healthz")


app = Flask(__name__)

start_tracing()
FlaskInstrumentor().instrument_app(app)

api = Api(app)
api.decorators = [
    cors.crossdomain(
        origin="*",
        headers=[
            "accept",
            "Content-Type",
            "X-Requested-With",
            "publicToken",
            "device",
            "privateToken",
            "memberId",
            "uuid",
            "admin-email",
        ],
        methods=["OPTIONS", "GET", "POST", "PUT", "DELETE", "PATCH"],
        max_age=300,
    )
]
add_routes(api)


def start_app():
    app.run(host="0.0.0.0", port=5004, threaded=True)


if __name__ == "__main__":
    start_app()
