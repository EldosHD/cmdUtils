# cmdUtils

This is just a repo for me to store my cmdutils

ignore me *~nyaa*

## ball.sh

This is just a simple bash script that displays a "ball" bouncing horizontally across the screen. You can use the `-h` flag to get a few more options

## Bruteforce serverfolders

This is a simple script that tries to find all possible urls on a server via bruteforce. There is not really a point to it allthough. The only real use is to find folders that were left public by accident and access the files in them. You have to specify an url in the format of `https://www.google.com/`. Use the `-h` flag to view all the possible options.

Ignore the rust version. I didn't build it.
But the python version works.

### Installation

```bash
git clone https://github.com/EldosHD/cmdUtils.git
pip install -r cmdUtils/bruteForceServerFolders/pythonBased/requirements.txt
```

## Color Snitch

This script runs and color the output of [snitch](https://github.com/tsoding/snitch). You can either pipe the output of `snitch list` to `colorSnitch` or you can use the `-r` flag to run it directly. Use the `-h` flag to view all the possible options. A binary release can be found under [releases](https://github.com/EldosHD/cmdUtils/releases).

NOTE: The binary was build under `Ubuntu 20.04` with `Python3.8.10`. To build the binary yourself use [pyinstaller](https://pyinstaller.org/en/stable/operating-mode.html). You can do that with: 
```bash
pip install pyinstaller
pyinstaller --onefile colorSnitch.py
```
The binary will be placed in the `dist` folder.
