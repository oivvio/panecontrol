from typing import TypedDict
from libtmux.server import Server, Session


class Config(TypedDict):
    session_name: str
    socket_name: str
    store_path: str


def get_config() -> Config:
    return {
        "session_name": "PANECONTROL",
        "socket_name": "NESTMUX",
        "store_path": "/tmp/store",
    }


def get_server(config: Config) -> Server:
    return Server(socket_name=config["socket_name"])


def get_session() -> (Session, bool):
    """Return panecontrol session. Create if needed."""
    config = get_config()
    server = get_server(config)
    session_name = config["session_name"]

    try:
        is_new = False
        session = [s for s in server.sessions if s.session_name == session_name][0]
    except IndexError:
        is_new = True
        session = server.new_session(session_name=session_name)

    return (session, is_new)
