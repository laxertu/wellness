from flask import Flask
from flask import request
from flask import jsonify
from repository import create_repository
from data_fetcher import DataFetcher
from datetime import datetime
from utils import parse_datetime_request, parse_date_request, IllegalArgumentException

ws = Flask(__name__)
fetcher = DataFetcher(create_repository())


@ws.route("/")
def hello_world():
    return jsonify([])


@ws.route('/get_values/', methods=['GET'])
def get_values():
    try:
        fields, dt_from, dt_to = parse_datetime_request()
        result = [x for x in fetcher.get_values(fields, dt_from, dt_to)]
        return jsonify(result)
    except IllegalArgumentException as e:
        return jsonify({'err': str(e)}), 400
    except Exception as e:
        return jsonify({'err': "Unknown"}), 500



@ws.route('/get_avg_values/', methods=['GET'])
def get_avg_values():
    try:
        fields, dt_from, dt_to = parse_date_request()
        result = [x for x in fetcher.get_avg_values(fields, dt_from, dt_to)]
        return jsonify(result)
    except IllegalArgumentException as e:
        return jsonify({'err': str(e)}), 400
    except Exception as e:
        return jsonify({'err': "Unknown"}), 500


@ws.route('/get_sum_values/', methods=['GET'])
def get_sum_values():
    try:
        fields, dt_from, dt_to = parse_date_request()
        result = [x for x in fetcher.get_sum_values(fields, dt_from, dt_to)]
        return jsonify(result)
    except IllegalArgumentException as e:
        return jsonify({'err': str(e)}), 400
    except Exception as e:
        return jsonify({'err': "Unknown"}), 500

