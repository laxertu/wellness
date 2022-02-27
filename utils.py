from datetime import datetime
from flask import request

DATE_FORMAT = "%d %b %Y %H:%M:%S"
ALLOWED_FIELDS = ['date_time', 'energy', 'reactive_energy', 'power', 'maximeter',
                  'reactive_power', 'voltage', 'intensity', 'power_factor']


class IllegalArgumentException(Exception):
    pass


def convert_datetime(dt: str) -> datetime:
    try:
        return datetime.strptime(dt, DATE_FORMAT)
    except Exception:
        raise IllegalArgumentException(f"Wrong date format {dt}")


def parse_request():
    fields = request.args.getlist("fields")
    dt_from_txt = request.args.get("dt_from")
    dt_to_txt = request.args.get("dt_to")
    if len(fields) == 0:
        raise IllegalArgumentException("Empty fields")

    unknown_fields = set(fields) - set(ALLOWED_FIELDS)
    if len(unknown_fields) > 0:
        txt = ",".join(list(unknown_fields))
        raise IllegalArgumentException(f"Unknown fields {txt}")

    return fields, dt_from_txt, dt_to_txt

def parse_datetime_request():

    fields, dt_from_txt, dt_to_txt = parse_request()

    try:
        dt_from = datetime.strptime(dt_from_txt, "%Y-%m-%d %H:%M:%S")
    except Exception:
        raise IllegalArgumentException(f"Wrong date from format {dt_from_txt}")

    try:
        dt_to = datetime.strptime(dt_to_txt, "%Y-%m-%d %H:%M:%S")
    except Exception:
        raise IllegalArgumentException(f"Wrong date to format {dt_to_txt}")

    return fields, dt_from, dt_to


def parse_date_request():
    fields, dt_from_txt, dt_to_txt = parse_request()

    try:
        dt_from = datetime.strptime(dt_from_txt, "%Y-%m-%d").date()
    except Exception:
        raise IllegalArgumentException(f"Wrong date from format {dt_from_txt}")

    try:
        dt_to = datetime.strptime(dt_to_txt, "%Y-%m-%d").date()
    except Exception:
        raise IllegalArgumentException(f"Wrong date to format {dt_to_txt}")

    return fields, dt_from, dt_to
