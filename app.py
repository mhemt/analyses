from flask import Flask

from database import db_session

app = Flask(__name__)
app.api_path = '/api/v1'


def load_api():
    from api import laboratory
    from api import user


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


load_api()

if __name__ == '__main__':
    app.run(debug=True)
