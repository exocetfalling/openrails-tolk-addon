# openrails-tolk-addon
Python script to add screen reader support to [Open Rails](https://www.openrails.org/) via cytolk.
Tested with Open Rails version 1.5.1 stable.
Note that Open Rails forks are not supported, since testing showed them to be unreliable. 

## Requirements:
- [keyboard](https://pypi.org/project/keyboard/)
- [cytolk](https://pypi.org/project/cytolk/0.1.6/)

## Usage
Download the script from [Releases](https://github.com/exocetfalling/openrails-tolk-addon/releases).
Make sure you have the requirements installed.
After that, run it from the command line.

The script will run in the background as the simulator runs, detecting changes in cab controls and sending them to cytolk.
Speed is not read out automatically to avoid it being irritating, you need to press Shift+V to hear that.
Quit the script using Ctrl+Shift+Q.

For Linux, you'll need root access since this uses the keyboard module.

## Acknowledgements
- [rings2006](https://github.com/rings2006), for giving me the idea and testing it out
- [pauliyobo](https://github.com/pauliyobo), for cytolk module
- [boppreh](https://github.com/boppreh), for keyboard module