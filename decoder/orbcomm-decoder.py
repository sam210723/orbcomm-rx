"""
orbcomm-decoder.py
https://github.com/sam210723/orbcomm-rx

Frontend for Subscriber Transmitter (STX) downlink decoder
"""

import argparse
import bitstring
import configparser
import math
import socket
import stx


# Globals
args = None             # Parsed CLI arguments
config = None           # Config parser object
source = None           # Input source type
sck = None              # Symbol socket object
buflen = 600            # Symbol socket buffer length (one minor frame)
packetf = None          # Packet output file
ver = "1.0"             # orbcomm-rx version


def init():
    print("┌──────────────────────────────────────────────┐")
    print("│                  orbcomm-rx                  │")
    print("│         Orbcomm STX Downlink Decoder         │")
    print("├──────────────────────────────────────────────┤")
    print("│     @sam210723      vksdr.com/orbcomm-rx     │")
    print("└──────────────────────────────────────────────┘\n")

    global args
    global config
    global packetf
    
    # Handle arguments and config file
    args = parse_args()
    config = parse_config(args.config)
    print_config()

    # Exit if input config fails
    if not config_input():
        if args.dump: packetf.close()
        print("Exiting...")
        exit(1)

    # Open packet file
    if args.dump:
        packetf = open(args.dump, "wb")
        print("Saving packets to \"{}\"".format(args.dump))

    print("──────────────────────────────────────────────────────────────────────────────────\n")

    # Ender main loop
    loop()


def loop():
    """
    Handles data from the symbol socket
    """

    frame = None

    loffset = -1
    while True:
        data = sck.recv(buflen)

        SYNC = '0xA6159F'
        bits = bitstring.BitArray(data)
        
        offset = bits.find(SYNC, bytealigned=False)

        if offset:
            offset = offset[0]
            print("OFFSET: {} bits".format(offset))
            
            if offset != loffset:
                frame = None
                frame = bits[offset:]
            else:
                frame += bits
                if len(frame) > 4800 and args.dump:
                    packetf.write(frame[:4800].tobytes())
                    frame = frame[4800:]
            
            loffset = offset


def config_input():
    """
    Configures the selected input source
    """

    global sck

    if source == "UDP":
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        ip = config.get('udp', 'ip')
        port = int(config.get('udp', 'port'))
        addr = (ip, port)

        try:
            sck.bind(addr)
            print("Binding UDP socket to {}:{}".format(ip, port))

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
    argp.add_argument("--config", action="store", help="Configuration file path (.ini)", default="decoder\\orbcomm-rx.ini")
    argp.add_argument("-v", action="store_true", help="Enable verbose console output")
    argp.add_argument("--dump", action="store", help="Path to save aligned packets to")

    return argp.parse_args()


def parse_config(path):
    """
    Parses configuration file
    """

    global source

    cfgp = configparser.ConfigParser()
    cfgp.read(path)

    source = cfgp.get('rx', 'input').upper()

    return cfgp


def print_config():
    """
    Prints configuration information
    """

    print("INPUT:      {}".format(source))
    print("VERSION:    {}\n".format(ver))


try:
    init()
except KeyboardInterrupt:
    if args.dump: packetf.close()
    print("Exiting...")
    exit()
