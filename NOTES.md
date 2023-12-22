break-pane but don't move with the pane to the window i ends up in

    tmux break-pane -d

break-pane and send it to specific destination

    tmux break-pane -d -t session:window

# Plan

Create a special session called "quickpane"

# Commands

## new pane

    X # Check if quickpane session exists if not create it

    # Create new window in session

    # Join to the new window

## attach pane

If there is only one pick that

If there are several display a choice using display-menu

    window = session.attached_window
    pane = window.attached_pane

    # Command to display a menu in tmux
    # This is a basic example; you'll need to modify it based on your actual menu items
    menu_command = "display-menu -T '#[align=centre] Options' 'Option 1' A 'send-keys \"Option1\"' 'Option 2' B 'send-keys \"Option2\"'"

But probably send something like "join-pane -s 1:2" in the options

    # Send the command to the pane
    pane.send_keys(menu_command, suppress_history=False)

    # Send the command to the pane
    pane.send_keys(menu_command, suppress_history=False)

## split pane

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


## TODO

### Rejigg. 

We can attach any window from any session. But sessions created with panecontrol
get special treatment. They get sent to the PANECONTROL session when they are
not active. They get marked in our shelve storage as special so that we can list
them in a menu even when they are not currently attached to PANECONTROL.  

We have two separate attach commands. One attachs panecontrol created windows.
The other attaches "normal" windows. When we attach a "normal window" we use link instead of join. 
So the the window will still be attached in it's original session. 

When we detach a window we have to check if it's a panecontrol  window or a normal window.


### Other stuff
Check name on create, [a-z][A-Z][0-9] only and unique

Create should optionally take input from "tmux input"

    tmux command-prompt -p "Enter input:" "run-shell 'ff %%'"

Either rip out libtmux or run shell tmux commands like this

    session.cmd('new-window', '-n', 'Another Window')
