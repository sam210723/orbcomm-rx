"""
stx.py
https://github.com/sam210723/orbcomm-rx

Parsing functions for Orbcomm STX packets
"""

SYNC = 0xA6159F

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
