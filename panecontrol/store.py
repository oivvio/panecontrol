from contextlib import contextmanager
import shelve
from libtmux import Pane
from .config import get_config


@contextmanager
def shelve_context(filename, *args, **kwargs):
    """Context manager for shelve databases."""
    shelf = shelve.open(filename, *args, **kwargs)

    try:
        yield shelf
    finally:
        shelf.close()


class Store:
    def __init__(self):
        self.config = get_config()
        with shelve_context(self.config["store_path"]) as store:
            if not "panes" in store:
                store["panes"] = {}

    def add_pane(self, name: str, pane: Pane) -> None:
        with shelve_context(self.config["store_path"]) as store:
            store["panes"] = {pane.id: name, **store["panes"]}

    @property
    def panes(self):
        with shelve_context(self.config["store_path"]) as store:
            result = store["panes"]
        return result

    @property
    def pane_id_to_connect(self):
        with shelve_context(self.config["store_path"]) as store:
            try:
                return store["pane_id_to_connect"]
            except KeyError:
                return None

    @pane_id_to_connect.setter
    def pane_id_to_connect(self, value) -> None:
        with shelve_context(self.config["store_path"]) as store:
            store["pane_id_to_connect"] = value
