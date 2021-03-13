# imports
import server.config as conf
import traceback
from server.views import root
from server.authorize.views import auth
from server.events.views import events
from server.scrap.views import scrap
from server.tables.views import tables
from google.auth.exceptions import RefreshError
from flask import Flask, session, redirect, jsonify
from flask_cors import CORS

from flask.json import JSONEncoder
from datetime import date


class CustomJSONEncoder(JSONEncoder):
    # custom json encoder for date time in ISO8601
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


# create application
app = Flask(__name__, template_folder='../frontend/',
            static_folder='../frontend/')
app.json_encoder = CustomJSONEncoder
app.config.from_object(conf)
app.debug = False

CORS(app, supports_credentials=True)


app.register_blueprint(root)
app.register_blueprint(auth)
app.register_blueprint(events)
app.register_blueprint(scrap)
app.register_blueprint(tables)


@app.errorhandler(Exception)
# define error handler
def show_error(e):
    if type(e) is RefreshError:
        redirect_url = session.get(conf.REDIRECT_URL, "/")
        pop_session(conf.REDIRECT_URL)
        pop_session(conf.CREDENTIALS)
        return redirect(redirect_url)
    else:
        err_msg = {"error": e.args}
        if "name" in dir(e):
            err_msg.update({"error": str(e.code)+" " + str(e.name)})
            err_msg.update({"name": e.name})
            err_msg.update({"code": e.code})

        err_msg.update({"trace": traceback.format_exc()})
        return jsonify(err_msg)


def pop_session(key):
    if key in session:
        session.pop(key)
