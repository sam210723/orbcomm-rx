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
