import requests
import pybreaker
from flask import Flask
from flask_restful import Resource, Api
import redis


class DBListener(pybreaker.CircuitBreakerListener):
    "Listener used by circuit breakers that execute database operations."

    def before_call(self, cb, func, *args, **kwargs):
        print("Called before the circuit breaker `cb` calls `func`.")
        pass

    def state_change(self, cb, old_state, new_state):
        print("Called when the circuit breaker `cb` state changes.")
        pass

    def failure(self, cb, exc):
        print("Called when a function invocation raises a system error.")
        pass

    def success(self, cb):
        print("Called when a function invocation succeeds.")
        pass


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


redis = redis.Redis(host='redis')

app = Flask(__name__)
api = Api(app)
api.add_resource(Test, '/')
api.add_resource(Status, '/status')

db_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=20,
    state_storage=pybreaker.CircuitRedisStorage(pybreaker.STATE_CLOSED, redis),
    listeners=[DBListener()]
    )


@db_breaker
def test():
    r = requests.get('http://test-service:5000')
    print(r.status_code)
    print(r.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
