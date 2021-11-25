from flask_restful import Resource


class HealthCheck(Resource):
    def get(self):
        return {"result": 200}, 200
