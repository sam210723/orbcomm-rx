"""
orbcomm-decoder.py
https://github.com/sam210723/orbcomm-rx

Frontend for Subscriber Transmitter (STX) downlink decoder
"""

import argparse
import bitstring
import configparser
import math
import os
import socket
import stx as STX
import time


# Globals
args = None             # Parsed CLI arguments
config = None           # Config parser object
stime = None            # Processing start time
source = None           # Input source type
sck = None              # Symbol socket object
buflen = 600            # Symbol socket buffer length (one minor frame)
symbolf = None          # Symbol input file
packetf = None          # Packet output file
locked = False          # Decoder lock state
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
    global stime
    global packetf
    
    # Handle arguments and config file
    args = parse_args()
    config = parse_config(args.config)
    print_config()

    # Exit if input config fails
    if not config_input():
        print("Exiting...")
        exit()

    # Open packet file
    if args.dump:
        packetf = open(args.dump, "wb")
        print("Saving packets to \"{}\"".format(args.dump))

    print("──────────────────────────────────────────────────────────────────────────────────\n")

    # Get processing start time
    stime = time.time()

    # Ender main loop
    loop()


def loop():
    """
    Handles data from the symbol socket
    """

    global locked

    buf = None
    loffset = -1

    while True:
        # Get data from input source
        if source == "UDP":
            data = sck.recv(buflen)
        elif source == "FILE":
            # Read symbols from file
            data = symbolf.read(buflen)

            # No more data to read from file
            if data == b'':
                symbolf.close()
                run_time = round(time.time() - stime, 3)
                print("FINISHED PROCESSING SYMBOL FILE IN {}".format(run_time))
                exit()

        # Unpack symbol bytes to bits
        bits = bitstring.BitArray(data)
        
        # Find sync word in symbols
        offset = bits.find(hex(STX.SYNC), bytealigned=False)

        # If sync word found
        if offset:
            # Set lock state
            if not locked: print("LOCKED")
            locked = True

            # Get sync word offset value
            offset = offset[0]
            
            # If offset has changed from previous frame
            if offset != loffset:
                # Start fresh frame
                buf = bits[offset:]
            else:
                # Concat frame data
                buf += bits

                # If frame is full length
                if len(buf) > 4800:
                    fbytes = buf.tobytes()[:600]

                    # Parse frame
                    frame = STX.Frame(fbytes)

                    # Write frame to file
                    if args.dump: packetf.write(fbytes)

                    # Remove parsed frame from buffer
                    buf = buf[4800:]
            
            loffset = offset
        else:
            # Set lock state
            if locked: print("UNLOCKED")
            locked = False


def config_input():
    """
    Configures the selected input source
    """

    global sck
    global symbolf

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
    elif source == "FILE":
        # Check symbol file exists
        if not os.path.exists(args.file):
            print("INPUT FILE DOES NOT EXIST\nExiting...")
            exit()
        
        symbolf = open(args.file, 'rb')
        print("Opened input file: \"{}\"".format(args.file))
        
        return True
    else:
        print("INVALID SOURCE: \"{}\"".format(source))
        exit()


def parse_args():
    """
    Parses command line arguments
    """

    argp = argparse.ArgumentParser()
    argp.description = "Orbcomm STX Downlink Decoder"
    argp.add_argument("--config", action="store", help="Configuration file path (.ini)", default="decoder\\orbcomm-rx.ini")
    argp.add_argument("--file", action="store", help="Path to symbol file", default=None)
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

    if args.file == None:
        source = cfgp.get('rx', 'input').upper()
    else:
        source = "FILE"

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
