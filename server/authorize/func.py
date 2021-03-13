from server.config import CLIENT_SECRET_FILE, SCOPES, CREDENTIALS, REDIRECT_URL, USERPROFILE, FRONTEND_PATH
from flask import url_for, session, request, redirect, jsonify, request
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

"""
google api利用のための認証情報を取得、利用するための関数群
flask route デコレータに
@route_with_creds(ret_url, **options)
デコレータを追記することで、認証取得後APIを利用できる

"""


def get_user_profile(creds):
    # ログインユーザー名を取得する
    if USERPROFILE not in session:
        user_profile = get_user_profile_from_google(creds)
        session[USERPROFILE] = user_profile
    else:
        user_profile = session[USERPROFILE]
    return user_profile


def get_user_profile_from_google(creds):
    # ログインユーザーの名前をgoogleから取得する
    service = build('people', 'v1', credentials=creds)
    results = service.people().get(
        resourceName='people/me',
        personFields='names,emailAddresses,Photos').execute()
    names = results.get('names', [])
    emailAddresses = results.get('emailAddresses', [])
    photos = results.get('photos', [])

    return {'name': get_item_from_dict(names, 'displayName'),
            'email_adress': get_item_from_dict(emailAddresses, 'value'),
            'photo_url': get_item_from_dict(photos, 'url'),
            'date': datetime.datetime.today()}


def get_item_from_dict(list, item_name):
    # 辞書リストから特定アイテムの値を取得する
    if(len(list)) > 0:
        return list[0].get(item_name, '')
    else:
        return ''


def get_flow(state):
    # google認証フローを生成する
    params = {"scopes": SCOPES}
    if state is not None:
        params["state"] = state
    flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, **params)
    flow.redirect_uri = url_for('auth.callback', _external=True)
    return flow


def credentials_to_dict(credentials):
    # google認証オブジェクトをdict形式に変換する
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def start_flow():
    # google認証取得フローを開始する
    flow = get_flow(None)
    authorization_url, state = flow.authorization_url(
        #        access_type='offline',
        include_granted_scopes='true')
    session['state'] = state
    return authorization_url


def get_return_url():
    # 認証獲得後のリダイレクトURLを取得する
    return_url = session.get(REDIRECT_URL)
    return return_url


def set_credentials_into_session():
    # google認証情報をflask sessionに保管する
    flow = get_flow(session['state'])
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session[CREDENTIALS] = credentials_to_dict(credentials)
    session.pop('state')
    return get_return_url()


def get_credentials(ret_url):
    # google apiを使用するための認証を取得する
    creds = None
    next_url = ret_url
    session[REDIRECT_URL] = ret_url

    if CREDENTIALS not in session:
        next_url = url_for('auth.authorize')
    else:
        creds = Credentials(**session[CREDENTIALS])

    if creds is None or creds.expired:
        session[REDIRECT_URL] = ret_url
        next_url = url_for('auth.authorize')

    return creds, next_url


def route_with_creds(ret_url, **options):
    # URLロケータにgoogle認証取得機能を追加するデコレータ
    def decolator(func):
        creds, next_url = get_credentials(ret_url)
        if creds is None:
            return redirect(next_url)
        return func(creds, **options)
    return decolator


def route_with_creds_ajax(ret_url, **options):
    # URLロケータにgoogle認証取得機能を追加するデコレータ(ajax対応)
    def decolator(func) -> str:
        url = request.headers.get("Referer", ret_url) + FRONTEND_PATH
        creds, next_url = get_credentials(url)
        if creds is None:
            return jsonify({'error': 'credential_err', 'auth_url': next_url})
        return func(creds, **options)
    return decolator


"""
ex:)
from flask import Flask, redirect
from flask.templating import render_template
from server.authorize.func import route_with_creds
from server.events.calendar import get_events_all

app = Flask(__name__)

@app.route('/cal/list')
def cal_list():
    @route_with_creds('/cal/list')
    def show_list(creds):
        events = get_events_all(creds)
        return render_template('eventlist.html', events=events)
    return show_list

"""
