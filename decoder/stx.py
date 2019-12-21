"""
stx.py
https://github.com/sam210723/orbcomm-rx

Parsing functions for Orbcomm STX packets
"""

from enum import Enum
import struct
from typing import NamedTuple
import collections

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
        self.t = Tools()
        self.parse()
    
    def parse(self):
        """
        Parse minor frame
        """

        print("[FRAME]")

        # Convert LSB-first data to MSB-first
        self.data = self.t.flip(self.data)

        # Parse Minor Frame Synchronisation Packet
        sync = SyncPacket(self.data[:PACKETLEN])
        sync.print()

        print()


class SyncPacket():
    """
    Parses Minor Frame Synchronisation packet (0x65)
    """

    def __init__(self, data):
        """
        Initialises packet class
        """

        self.data = data
        self.format = ">3xBx2B3x2B"
        self.packet = None
        self.parse()
    
    def parse(self):
        # Unpack packet fields
        packet = self.data[:PACKETLEN]
        fields = struct.unpack(self.format, packet)

        # Parse fields
        scid = "FM-{}".format(fields[0])    # Spacecraft ID
        channel = bin(fields[1])            # Downlink Channel
        counter = fields[2] >> 4            # Frame Counter
        fcs = fields[3] + fields[4]        # 16-bit Fletcher Checksum

        # Create named tuple from parsed fields
        tup = collections.namedtuple('SyncPacket', 'scid downlink counter fcs')
        self.packet = tup(scid, channel, counter, fcs)
    
    def print(self):
        """
        Prints packet info to console
        """

        if self.packet:
            print("  [SYNC] SPACECRAFT: {}    DOWNLINK: {}    COUNTER: {}    CHECKSUM: {}".format(*self.packet))


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


    def fcs(self, data):
        """
        Calculates 16-bit Fletcher Checksum
        """

        # Initialise checksums
        c = [0, 0]

        for byte in data:
            c[0] = (c[0] + byte) % 255
            c[1] = (c[1] + c[0]) % 255

        return c[0] + c[1]
