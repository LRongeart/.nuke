import datetime


try:
    import colorama
    colorama.init()
    from colorama import Fore, Style
except ImportError:
    # fallback: define dummy Fore/Style
    class Dummy:
        RESET_ALL = ''
    class DummyFore(Dummy):
        GREEN = YELLOW = RED = CYAN = MAGENTA = GREY = ''
    Fore = DummyFore()
    Style = Dummy()

import re

def cprint(*args, **kwargs):
    text = ' '.join(str(a) for a in args)
    # List of (pattern, color) tuples, multi-character patterns first
    patterns = [
        (r'[><]', Fore.LIGHTYELLOW_EX),
        (r'\+', Fore.YELLOW),
        (r'=', Fore.YELLOW),
        (r'-', Fore.YELLOW),
        (r'!', Fore.RED),
        (r'\|', Fore.YELLOW),
        (r'NUKE', Fore.RED),
        (r'NUKE_LOG', Fore.RED),
        (r'SUCCESS', Fore.GREEN),
    ]
    for pat, color in patterns:
        text = re.sub(pat, lambda m: color + m.group(0) + Style.RESET_ALL, text)
    print(text, **kwargs)


def nukeHello():
    cprint("""
+=======================================+    
  WELCOME IN NUKE & HAPPY COMPOSITING !!
+=======================================+
          """)

def nukeReady():
    cprint("""| >> NUKE is up & running.""")


def nukeTime():
    cprint("| >>",datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))))