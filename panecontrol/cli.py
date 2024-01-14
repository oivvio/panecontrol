#!/usr/bin/env python3

import os
import subprocess

import typer

from .menu import Menu
from .store import Store
from .config import get_config, get_server, get_session

menuapp = Menu()
app = typer.Typer()

@app.command()
def create_window(name: str):
    """Create window"""
    session, _ = get_session()
    window = session.new_window(attach=False)

    pane = window.panes[0]
    store = Store()
    store.add_pane(name, pane)
    store.add_pane(name, pane)


@app.command()
def attach_pane():
    """Attach pane"""
    config = get_config()
    server = get_server(config)
    session, is_new = get_session()

    n_windows = len(server.windows)
    store = Store()

    if is_new:
        print("Nothing to attach. Run create first")
    else:
        # There is only one window so attach it
        if n_windows == 1:
            print("Nothing to attach. Run create first")

        if n_windows == 2:
            # There are two windows but one is for keeping the session around
            # Pick the session and attach it
            window = server.windows[1]
            cmd = f"tmux -L {config['socket_name']} join-pane -l 80 -h -s {server.name}:{window.id}"
            os.system(cmd)

        if n_windows > 2:
            # There are many windows
            options = []

            for index, window in list(enumerate(server.windows))[1:]:
                shortcut_letter = chr(96 + index)
                pane_id = window.panes[0].id
                if pane_id in store.panes:
                    window_label = store.panes[pane_id]
                else:
                    window_label = "NAN"
                try:
                    options.append(
                        f"{window_label} {shortcut_letter} 'join-pane -l 80 -h -s {server.name}:{window.id}'"
                    )
                except AttributeError:
                    pass

            options = " ".join(options)
            cmd = f"tmux display-menu -x 1 -y 1000 -T 'panecontrol windows' {options}"

            os.system(cmd)


@app.command()
def break_pane():
    """Send the pane window back to background"""
    config = get_config()
    session_name = config["session_name"]

    cmd = "tmux"
    arguments = [cmd, "-L", config['socket_name'], "break-pane", "-t", session_name]

    os.execvp(cmd, arguments)



@app.command()
def menu():
    """Display menu"""

    config = get_config()

    arguments = ["tmux", "-L", config['socket_name'], "display-popup",  "-E",  "panecontrol_menu"]
    subprocess.run(arguments)

    # Pick up users menu selection from store
    store = Store()

    if store.pane_id_to_connect:
        config = get_config()
        arguments = ["tmux", "-L", config['socket_name'], "join-pane", "-h", "-l", "80", "-s", store.pane_id_to_connect]
        subprocess.run(arguments)


@app.command()
def bind_keys():
    """Set up key bindings."""
    config = get_config()
    server = get_server(config)
    server.cmd("bind-key", "-r", "left", "resize-pane", "-L", 2)
    server.cmd("bind-key", "-r", "right", "resize-pane", "-R", 2)

    session_name = config["session_name"]

    # break pane is special
    server.cmd("bind-key", "b", "break-pane", "-t", session_name)

    def bind_key(key: str, command: str) -> None:
        shell_cmd = f"tmux -L {config['socket_name']}  bind-key {key} run-shell 'panecontrol {command}'"
        shell_cmd = f"run-shell 'panecontrol {command}'"
        server.cmd("bind-key", key, shell_cmd)

    bind_key("a", "attach")
    bind_key("m", "menu")


def main():
    app()


if __name__ == "__main__":
    app()
