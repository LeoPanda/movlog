from server.authorize import func
from flask import Blueprint, redirect, jsonify

auth = Blueprint('auth', __name__)


@auth.route('/auth/getprofile')
def get_profile():
    @func.route_with_creds_ajax('/auth/getprofile')
    def user_profile(creds):
        return jsonify(func.get_user_profile(creds))
    return user_profile


@auth.route('/auth/authorize')
def authorize():
    ret_url = func.start_flow()
    return redirect(ret_url)


@auth.route('/auth/oauth2callback')
def callback():
    ret_url = func.set_credentials_into_session()
    return redirect(ret_url)
