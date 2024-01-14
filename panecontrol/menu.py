from typing import List

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import (
    Label,
    Input,
)
from textual.widget import Widget
from textual import events
from libtmux import Window, Pane

from .store import Store
from .config import get_config, get_server


class QueryInput(Input):
    pass


class Row(Widget):
    def __init__(
        self, index: int, window: Window, pane: Pane, pane_name: str, **kwargs
    ):
        self.index = index
        self.window = window
        self.pane = pane
        self.pane_name = pane_name
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Label(
            f"{self.pane_name.ljust(10)[:10]} {self.pane.pane_id.ljust(4)[:4]} \[j]oin \[s]teal "
        )


class Rows(ScrollableContainer):
    DEFAULT_CSS = """
    * {
    height: 1;
    }
    """

    filter_query = reactive("")

    def __init__(self, windows: List[Window], *args, **kwargs):
        self.windows = windows
        super().__init__(*args, **kwargs)

    def watch_filter_query(self, filter_query: str) -> None:
        query = filter_query.lower()

        for row in self.query(Row).results():
            if query in row.pane_name.lower():
                row.styles.display = "block"
            else:
                row.styles.display = "none"

    def compose(self) -> ComposeResult:
        row_index = 0
        store = Store()

        # Add panes that where created with panecontrol
        for window in self.windows:
            for pane in window.panes:
                row_index += 1
                try:
                    pane_name = store.panes[pane.id]
                    yield Row(row_index, window, pane, pane_name)
                except KeyError:
                    pane_name = "-"

        # Add panes that where NOT created with panecontrol
        for window in self.windows:
            for pane in window.panes:
                row_index += 1
                try:
                    pane_name = store.panes[pane.id]
                    yield Row(row_index, window, pane, pane_name)
                except KeyError:
                    pane_name = "-"
                    yield Row(row_index, window, pane, pane_name)


class Menu(App):
    CSS_PATH = "menu.tcss"

    focused_row_index = 0
    focused_row = None
    n_visible_rows = 0
    selection_in_progress = False
    store = Store()
    config = get_config()

    # session, _ = get_session()
    server = get_server(config)
    rows = Rows([s for s in server.windows])

    def set_focus_row(self):
        self.selection_in_progress = True
        visible_rows = [
            row for row in self.query(Row).results() if row.styles.display == "block"
        ]
        self.n_visible_rows = len(visible_rows)

        row_index = 0
        for index, row in enumerate(visible_rows):
            if index == self.focused_row_index:
                row_index += 1
                row.index = row_index
                row.styles.text_style = "reverse"
                self.focused_row = row
            else:
                row.styles.text_style = "none"

    def reset_focus_row(self):
        self.selection_in_progress = False
        self.focused_row_index = -1
        for row in self.query(Row).results():
            row.styles.text_style = "none"

    def on_input_changed(self, message: Input.Changed) -> None:
        self.rows.filter_query = message.value

    def compose(self) -> ComposeResult:
        yield QueryInput()
        yield self.rows

    def on_key(self, event: events.Key) -> None:
        if event.name == "down":
            if self.focused_row_index < self.n_visible_rows - 1:
                self.focused_row_index += 1
            self.set_focus_row()

        elif event.name == "up":
            if self.focused_row_index > 0:
                self.focused_row_index -= 1
            self.set_focus_row()

        elif event.name == "backspace":
            self.reset_focus_row()

        else:
            if self.selection_in_progress:
                if event.name == "enter":
                    self.store.pane_id_to_connect = self.focused_row.pane.pane_id
                    self.exit()
            else:
                self.reset_focus_row()

    def on_ready(self) -> None:
        self.store.pane_id_to_connect = None

def main():
    app = Menu()
    app.run()

if __name__ == "__main__":
    main()
