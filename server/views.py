from flask import Blueprint, redirect
from flask.templating import render_template
from server.authorize.func import route_with_creds

root = Blueprint('root', __name__, template_folder='../frontend')


@root.route('/')
def show_root():
    @route_with_creds('/')
    def show_root_with_creds(creds):
        return render_template('index.html')
    return show_root_with_creds
