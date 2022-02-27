from flask import Flask
from flask import jsonify
from repository import create_repository
from data_fetcher import DataFetcher
from utils import parse_datetime_request, parse_date_request, IllegalArgumentException
from flask_httpauth import HTTPTokenAuth
from session import SessionManager
import logging

ws = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
fetcher = DataFetcher(create_repository())
session_manager = SessionManager()


class AccessForbiddenException(Exception):
    pass


@ws.route("/")
def hello_world():
    return ''


@ws.route('/login/', methods=['GET'])
def login():
    try:
        session_id = session_manager.do_login()
        return jsonify({'session_id': session_id})
    except Exception as e:
        logging.error(e)
        return jsonify({'err': "Unnkown error"}), 500


@auth.verify_token
def verify_token(token):
    try:
        result = session_manager.get_session_data(token)
        session_manager.refresh_session(token)
        return result
    except Exception as e:
        logging.error(e)
        return None


@ws.route('/get_values/', methods=['GET'])
@auth.login_required
def get_values():
    try:
        fields, dt_from, dt_to = parse_datetime_request()
        result = [x for x in fetcher.get_values(fields, dt_from, dt_to)]
        return jsonify(result)
    except IllegalArgumentException as e:
        return jsonify({'err': str(e)}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({'err': "Unknown"}), 500


@ws.route('/get_avg_values/', methods=['GET'])
@auth.login_required
def get_avg_values():
    try:
        fields, dt_from, dt_to = parse_date_request()
        result = [x for x in fetcher.get_avg_values(fields, dt_from, dt_to)]
        return jsonify(result)
    except IllegalArgumentException as e:
        return jsonify({'err': str(e)}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({'err': "Unknown"}), 500


@ws.route('/get_sum_values/', methods=['GET'])
@auth.login_required
def get_sum_values():
    try:
        fields, dt_from, dt_to = parse_date_request()
        result = [x for x in fetcher.get_sum_values(fields, dt_from, dt_to)]
        return jsonify(result)
    except IllegalArgumentException as e:
        return jsonify({'err': str(e)}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({'err': "Unknown"}), 500
