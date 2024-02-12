import subprocess
import sys

if __name__ == "__main__":
    subprocess.Popen([sys.executable, "gytmdl_gui.py"], creationflags=subprocess.CREATE_NO_WINDOW)
