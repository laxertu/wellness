import datetime as dt
from secrets import token_hex

SESSION_EXPIRE_SECONDS = 3600


class SessionException(Exception):
    pass


class SessionManager:
    def __init__(self):
        self._sessions = {}

    def refresh_session(self, session_id):
        self.get_session_data(session_id)['ts'] = dt.datetime.now()

    def do_login(self) -> str:
        session_id = token_hex(20)
        self._sessions[session_id] = {'ts': dt.datetime.now()}
        return session_id

    def get_session_data(self, session_id: str):
        try:
            return self._sessions[session_id]
        except KeyError:
            raise SessionException('Unexistent session')

    def session_has_expired(self, session_id: str):
        now = dt.datetime.now()
        session_data = self.get_session_data(session_id)
        return (now - session_data['ts']).total_seconds() > SESSION_EXPIRE_SECONDS
