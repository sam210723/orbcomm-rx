"""
orbcomm_decoder.py
Orbcomm STX Decoder v1.0
https://github.com/sam210723/orbcomm-rx
"""

import argparse
from colorama import init as init_color
from colorama import Fore, Back, Style
import tools

ver = 1.0

# Parse arguments
argparser = argparse.ArgumentParser(description="Orbcomm STX Decoder v{0}".format(ver))
argparser.add_argument("-p", action="store", help="Symbol TCP port", default=1234)
args = argparser.parse_args()


def init():
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃" + Style.BRIGHT + Fore.LIGHTYELLOW_EX + "        Orbcomm STX Decoder v{0}        ".format(ver) + Style.RESET_ALL + "┃")
    print("┃" + Style.BRIGHT + " http://github.com/sam210723/orbcomm-rx " + Style.RESET_ALL + "┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

    print("Listening on port {0}".format(args.p))


init_color()
init()
