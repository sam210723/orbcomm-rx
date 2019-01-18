"""
orbcomm_decoder.py
Orbcomm STX Decoder v1.0
https://github.com/sam210723/orbcomm-rx
"""

import argparse
from colorama import init as init_color
from colorama import Fore, Back, Style
from socket import *
import stx
import tools

ver = 1.0
udpIP = "0.0.0.0"
udpTimeout = 10
udpSocket = socket(AF_INET, SOCK_DGRAM)

# Parse arguments
argparser = argparse.ArgumentParser(description="Orbcomm STX Decoder v{0}".format(ver))
argparser.add_argument("-p", action="store", help="Symbol TCP port", default=1234)
args = argparser.parse_args()


def init():
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃" + Style.BRIGHT + Fore.LIGHTYELLOW_EX + "        Orbcomm STX Decoder v{0}        ".format(ver) + Style.RESET_ALL + "┃")
    print("┃" + Style.BRIGHT + " http://github.com/sam210723/orbcomm-rx " + Style.RESET_ALL + "┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

    start_socket()


def start_socket():
    # Bind socket to port on all interfaces
    udpSocket.settimeout(udpTimeout)
    udpSocket.bind((udpIP, int(args.p)))
    print("UDP listening on port {0}\n".format(args.p))

    while True:
        try:
            data, addr = udpSocket.recvfrom(1024)
            stx.decode(data)
        except timeout:
            print("No data received for {0} seconds".format(udpTimeout))
            break


init_color()

try:
    init()
except KeyboardInterrupt:
    print("Exiting...")
