#!/usr/bin/env python3

# import os
# import sys

# from menu import Menu
# from store import Store
# from config import get_config, get_server, get_session


# menuapp = Menu()


# def create_window(name: str):
#     session, _ = get_session()
#     window = session.new_window(attach=False)

#     pane = window.panes[0]
#     store = Store()
#     store.add_pane(name, pane)
#     store.add_pane(name, pane)


# def attach_pane():
#     config = get_config()
#     session, is_new = get_session()

#     n_windows = len(session.windows)

#     store = Store()

#     if is_new:
#         print("Nothing to attach. Run create first")
#     else:
#         # There is only one window so attach it
#         if n_windows == 1:
#             print("Nothing to attach. Run create first")

#         if n_windows == 2:
#             # There are two windows but one is for keeping the session around
#             # Pick the session and attach it
#             window = session.windows[1]
#             cmd = f"tmux -L {config['socket_name']} join-pane -l 80 -h -s {session.name}:{window.id}"
#             os.system(cmd)

#         if n_windows > 2:
#             # There are many windows
#             options = []

#             for index, window in list(enumerate(session.windows))[1:]:
#                 shortcut_letter = chr(96 + index)
#                 pane_id = window.panes[0].id
#                 if pane_id in store.panes:
#                     window_label = store.panes[pane_id]
#                 else:
#                     window_label = "NAN"
#                 try:
#                     options.append(
#                         f"{window_label} {shortcut_letter} 'join-pane -l 80 -h -s {session.name}:{window.id}'"
#                     )
#                 except AttributeError:
#                     pass

#             options = " ".join(options)
#             cmd = f"tmux display-menu -x 1 -y 1000 -T 'panecontrol windows' {options}"

#             os.system(cmd)


# # def smallest_integer_not_in_list(lst) -> int:
# #     result = 1
# #     done = False
# #     while not done:
# #         if result not in lst:
# #             return result
# #         result += 1


# def break_pane():
#     """Send the pane window back to background"""
#     config = get_config()
#     session_name = config["session_name"]
#     cmd = f"tmux -L  {config['socket_name']} break-pane -t {session_name}"
#     os.system(cmd)


# def menu():
#     python = "/Users/Oivvio/Library/Caches/pypoetry/virtualenvs/panecontrol-V_7Q8mZ2-py3.9/bin/python"
#     textual = "/Users/Oivvio/Library/Caches/pypoetry/virtualenvs/panecontrol-V_7Q8mZ2-py3.9/bin/textual"
#     # cmd = f"tmux display-popup -x 1 -y 1 -w 40 '{textual} run --dev ~/oprepos/panecontrol/panecontrol/menu.py' "
#     # cmd = f"tmux display-popup -x 1 -y 1 -w 100 '{python}  ~/oprepos/panecontrol/panecontrol/menu.py' "

#     cmd = (
#         f"tmux display-popup  -E '{python}  ~/oprepos/panecontrol/panecontrol/menu.py' "
#         # f"tmux display-popup   -x 1 -y 1 -h 30 -w 120 '{python}  ~/oprepos/panecontrol/panecontrol/menu.py' "
#         # f"{python}  ~/oprepos/panecontrol/panecontrol/menu.py "
#     )
#     os.system(cmd)
#     store = Store()
#     if store.pane_id_to_connect:
#         config = get_config()
#         cmd = f"tmux -L {config['socket_name']} join-pane -l 80 -h -s {store.pane_id_to_connect}"
#         os.system(cmd)


# def bind_keys():
#     # print("bind keys")
#     server = get_server(get_config())
#     server.cmd("bind-key", "-r", "left", "resize-pane", "-L", 2)
#     server.cmd("bind-key", "-r", "right", "resize-pane", "-R", 2)
#     python = "/Users/Oivvio/Library/Caches/pypoetry/virtualenvs/panecontrol-V_7Q8mZ2-py3.9/bin/python"
#     config = get_config()

#     def bind_key(key: str, command: str) -> None:
#         # shell_cmd = f"run-shell {python} '~/oprepos/panecontrol/panecontrol/panecontrol.tmux {command}'"
#         shell_cmd = f"tmux -L {config['socket_name']}  bind-key {key} run-shell '{python} ~/oprepos/panecontrol/panecontrol/panecontrol.tmux {command}'"

#         # print(shell_cmd)
#         # print(shell_cmd)
#         shell_cmd = f"run-shell '{python} ~/oprepos/panecontrol/panecontrol/panecontrol.tmux {command}'"
#         server.cmd("bind-key", key, shell_cmd)

#     bind_key("a", "attach")
#     bind_key("b", "break")
#     bind_key("m", "menu")

from cli import bind_keys, attach_pane, menu, break_pane, create_window

if __name__ == "__main__":
    bind_keys()

    try:
        command = sys.argv[1]

        if command == "bindkeys":
            pass

        if command == "attach":
            attach_pane()

        if command == "menu":
            menu()

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
