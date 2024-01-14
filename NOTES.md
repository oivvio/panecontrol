# TODOs

+ Check how normal vs panecontrol panes behave when attached / detached.

+ Make proper python package.

+ Make runnable as tmux plugin

+ Implement join vs steal from menu


## Split pane

    detach the current pane

## list all panes on session quickpane

    tmux list-panes -s -t quickpane

## Names

panecontrol

## Stuff I've figured out

window id does not persist.

Apply this to session on startup.

    set-option -g allow-rename off

does not work


### Rejigg.

We can attach any window from any session. But sessions created with panecontrol
get special treatment. They get sent to the PANECONTROL session when they are
not active. They get marked in our shelve storage as special so that we can list
them in a menu even when they are not currently attached to PANECONTROL.

When we detach a window we have to check if it's a panecontrol window or a normal window.

### Other stuff

Check name on create, [a-z][A-Z][0-9] only and unique

Create should optionally take input from "tmux input"

    tmux command-prompt -p "Enter input:" "run-shell 'ff %%'"

Either rip out libtmux or run shell tmux commands like this

    session.cmd('new-window', '-n', 'Another Window')

### Textual

Only Input, Button and the like are focusable.

Input + rows

Input listens for up down. If it has focus it will loose focus.
