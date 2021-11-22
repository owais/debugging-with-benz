

from flask import Flask

import uwsgidecorators
from splunk_otel.tracing import start_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from flask_restful import Api
from flask_restful.utils import cors


app = Flask(__name__)


@uwsgidecorators.postfork
def setup_tracing():
   start_tracing()
   # Instrument the Flask app instance explicitly
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


# def start_app():
#     app.run(host="0.0.0.0", port=5004, threaded=True)
#
#
# if __name__ == "__main__":
#     start_app()

@app.route('/')
def hello_world():
    return 'Hello Benz!'


application = app