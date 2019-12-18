"""
orbcomm-decoder.py
https://github.com/sam210723/orbcomm-rx

Frontend for Subscriber Transmitter (STX) downlink decoder
"""

import argparse
import bitstring
import math
import socket


# Globals
args = None             # Parsed CLI arguments
sck = None              # Symbol socket object
buflen = 600            # Symbol socket buffer length (two minor frames)
packetf = None          # Packet output file
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
    global packetf
    
    args = parse_args()
    print_config()

    # Open packet file
    if args.dump:
        packetf = open(args.dump, "wb")
        print("Saving packets to \"{}\"".format(args.dump))

    print("──────────────────────────────────────────────────────────────────────────────────\n")

    if config_socket(): loop()


def loop():
    """
    Handles data from the symbol socket
    """

    while True:
        data = sck.recv(buflen)

        SYNC = '0xA6159F'
        bits = bitstring.BitArray(data)
        
        offset = bits.find(SYNC, bytealigned=False)

        if offset:
            offset = offset[0]
            print("OFFSET: {} bits".format(offset))
            
            l = 4800-offset-(offset%8)
            frame = bits[offset:offset+l]
        
            if args.dump:
                packetf.write(frame.tobytes())
        



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
    argp.add_argument("--dump", action="store", help="Path to save aligned packets to")

    return argp.parse_args()


def print_config():
    """
    Prints configuration information
    """

    print("INPUT PORT:    {}".format(args.p))
    print("VERSION:       {}\n".format(ver))


try:
    init()
except KeyboardInterrupt:
    if args.dump: packetf.close()
    print("Exiting...")
    exit()
