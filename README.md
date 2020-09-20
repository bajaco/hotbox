# Hotbox

Hotbox: A CLI hotkey configurator for Openbox.

Obkey in the Arch Linux AUR relies on an outdated python version.
I wanted to create a quick and easy-to-use tool to set hotkeys with minimal dependancies.

## Installation

Clone the repo.
Arch users: Available in aur:
1. clone https://aur.archlinux.org/hotbox-git.git
2 cd hotbox-git
3. run makepkg -si

## Usage

In the main directory execute python -m hotbox.
Then simply follow on-screen instructions.

Example usage to set Alt+t to open a terminal:
1. Open hotbox by typing python -m hotbox
2. Type '4' to add a hotkey
3. Enter 'A-t'
4. Confirm any y/n prompts that appear
5. Enter '1' to choose Execute
6. Type in 'xterm', or the command to open your favorite terminal
7. Choose any other options as presented

That's it. Alt+t should now open a terminal window.

For more information see http://openbox.org/wiki/Help:Actions

## License

MIT license
