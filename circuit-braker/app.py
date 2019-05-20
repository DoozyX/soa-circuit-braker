import requests
import pybreaker
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
db_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=20)


class Test(Resource):
    def get(self):
        try:
            test()
        except:
            return {'ERROR': True}
        return {'OK': True}


class Status(Resource):
    def get(self):
        return {"FAILS": db_breaker.fail_counter, "CURRENT_STATE": db_breaker.current_state}


api.add_resource(Test, '/')
api.add_resource(Status, '/status')


@db_breaker
def test():
    r = requests.get('http://test-service:5000')
    print(r.status_code)
    print(r.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
