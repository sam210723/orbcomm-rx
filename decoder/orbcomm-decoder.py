"""
orbcomm-decoder.py
https://github.com/sam210723/orbcomm-rx

Frontend for Subscriber Transmitter (STX) downlink decoder
"""

import argparse
import socket


# Globals
args = None             # Parsed CLI arguments
sck = None              # UDP socket object
buflen = 96             # Socket buffer length (one packet)
ver = "1.0"             # orbcomm-rx version

# Constants
ADDR = "127.0.0.1"      # Default symbol address
PORT = 1234             # Default symbol port


def init():
    print("┌──────────────────────────────────────────────┐")
    print("│                  orbcomm-rx                  │")
    print("│         Orbcomm STX Downlink Decoder         │")
    print("├──────────────────────────────────────────────┤")
    print("│     @sam210723      vksdr.com/orbcomm-rx     │")
    print("└──────────────────────────────────────────────┘\n")

    global args
    
    args = parse_args()
    print_config()

    print("──────────────────────────────────────────────────────────────────────────────────\n")

    if config_socket(): loop()


def loop():
    """
    Handles data from the symbol socket
    """

    while True:
        data = sck.recv(buflen)


def config_socket():
    """
    Configures symbol UDP socket
    """

    global sck

    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sck.bind((ADDR, args.p))
        return True
    except socket.error as e:
        print(e)
        return False


def parse_args():
    """
    Parses command line arguments
    """

    argp = argparse.ArgumentParser()
    argp.description = "Orbcomm STX Downlink Decoder"
    argp.add_argument("-v", action="store_true", help="Enable verbose console output")
    argp.add_argument("-p", action="store", help="Symbol UDP port", default=PORT)

    return argp.parse_args()


def print_config():
    """
    Prints configuration information
    """

    print("INPUT PORT:    {}".format(args.p))
    print("VERSION:       {}".format(ver))


try:
    init()
except KeyboardInterrupt:
    print("Exiting...")
    exit()
