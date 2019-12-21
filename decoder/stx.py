"""
stx.py
https://github.com/sam210723/orbcomm-rx

Parsing functions for Orbcomm STX packets
"""

from enum import Enum
import struct
from typing import NamedTuple

# Constants
SYNCWORD = 0xA6159F     # Frame synchronisation word
PACKETLEN = 12          # Packet length (bytes)
FRAMELEN = 600          # Minor frame length (bytes)

class Frame():
    """
    Parses minor frame
    """

    def __init__(self, data):
        """
        Initialises frame class
        """

        self.data = data
        self.parse()
    
    def parse(self):
        """
        Parse minor frame
        """

        print("[FRAME]")

class Packets(Enum):
    """
    Packet types
    """

    SYNC      = 0x65    # Synchronisation
    MSG       = 0x1A    # Message
    UPLINK    = 0x1B    # Uplink channel info
    DOWNLINK  = 0x1C    # Downlink channel info
    NCC       = 0x1D    # Network Control Centre
    FILL      = 0x1E    # Fill data
    EPHEMERIS = 0x1F    # Satellite ephemeris
    ORBIT     = 0x22    # Orbital elements


class Tools():
    """
    Various utility functions
    """

    def flip(self, n):
        """
        Flip bits in bytes
        """

        out = b''

        for i in n:
            bits = '{:0{width}b}'.format(i, width=8)
            out += bytes([int(bits[::-1], 2)])
        
        return out


    def hex(self, n):
        """
        Convert bytes to hex string
        """

        integer = int.from_bytes(n, byteorder="little")
        return hex(integer)[2:].upper()
