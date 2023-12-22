#!/usr/bin/env python3

import os
import sys
import shelve
from contextlib import contextmanager
from typing import TypedDict
from libtmux.server import Server, Session


@contextmanager
def shelve_context(filename, *args, **kwargs):
    """Context manager for shelve databases."""
    shelf = shelve.open(filename, *args, **kwargs)
    try:
        yield shelf
    finally:
        shelf.close()

class Config(TypedDict):
    session_name: str
    socket_name: str
    store_path: str


def get_config() -> Config:
    return {
        "session_name": "PANECONTROL",
        "socket_name": "NESTMUX",
        "store_path": "/tmp/store"
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


def create_window(name: str):
    session, session_is_new = get_session()
    config = get_config()

    window = session.new_window(attach=False)

    pane = window.panes[0]

    with shelve_context(config['store_path']) as store:
        store[pane.id] = name

    #session.cmd("join-pane", "-l", 80, "-h", "-s", pane.id)
    #cmd = f"tmux -L {config['socket_name']} join-pane -l 80 -h -s {pane.id}"
    #os.system(cmd)


def attach_pane():
    config = get_config()
    session, is_new = get_session()

    n_windows = len(session.windows)

    if is_new:
        print("Nothing to attach. Run create first")
    else:

        # There is only one window so attach it
        if n_windows == 1:
            print("Nothing to attach. Run create first")
            #window = session.windows[0]


        if n_windows == 2:
            # There are two windows but one is for keeping the session around
            # Pick the session and attach it
            window = session.windows[1]
            cmd = f"tmux -L {config['socket_name']} join-pane -l 80 -h -s {session.name}:{window.id}"
            os.system(cmd)

        if n_windows > 2:
            # There are many windows
            options = []

            with shelve_context(config['store_path']) as store:
                for index, window in list(enumerate(session.windows))[1:]:
                    shortcut_letter = chr(96 + index)
                    pane_id = window.panes[0].id
                    if pane_id in store:
                        window_label = store[pane_id]
                    else:
                        window_label = "NAN"
                    try:
                        options.append(f"{window_label} {shortcut_letter} 'join-pane -l 80 -h -s {session.name}:{window.id}'")
                    except AttributeError:
                        pass

            options = " ".join(options)
            cmd = f"tmux display-menu -x 1 -y 1000 -T 'panecontrol windows' {options}"

            os.system(cmd)



def smallest_integer_not_in_list(lst) -> int:
    result = 1
    done = False
    while not done:
        if result not in lst:
            return result
        result += 1

def break_pane():
    """Send the pane window back to background """
    config = get_config()
    session_name = config["session_name"]
    cmd = f"tmux -L  {config['socket_name']} break-pane -t {session_name}"
    os.system(cmd)


def bind_keys():
    server = get_server(get_config())
    server.cmd("bind-key", "-r", "left", "resize-pane", "-L", 2)
    server.cmd("bind-key", "-r", "right", "resize-pane", "-R", 2)

    server.cmd("bind-key", "a", "run-shell '~/oprepos/panecontrol/panecontrol.tmux attach'")
    server.cmd("bind-key", "b", "run-shell '~/oprepos/panecontrol/panecontrol.tmux break'")


if __name__ == "__main__":
    bind_keys()

    try:
        command = sys.argv[1]

        if command == "attach":
            attach_pane()

        if command == "break":
            break_pane()

        if command == "create":
            try:
                name = sys.argv[2]
                create_window(name)
            except IndexError:
                print("No name given.")

    except IndexError:
        print("no command supplied")
