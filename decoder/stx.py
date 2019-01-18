"""
stx.py
Orbcomm STX Decoder v1.0
https://github.com/sam210723/orbcomm-rx
"""


def decode(symbols):
    #symMap = [0, 1, 3, 2]
    symMap = [3, 2, 0, 1]
    lastSym = None
    buf = ''

    # Differential Decoding
    for i in range(len(symbols)):
        # Require two symbols for differential decoding
        if lastSym is None:
            pass

        lastSym = symbols[i - 1]
        currSym = symbols[i]
        lastMapI = symMap.index(lastSym)
        currMapI = symMap.index(currSym)

        if currMapI == 0 and lastMapI == 3:
            # Positive shift
            dir = "+"
            buf += '1'
        elif currMapI == 3 and lastMapI == 0:
            # Negative shift
            dir = "-"
            buf += '0'
        elif currMapI > lastMapI:
            # Positive shift
            dir = "+"
            buf += '1'
        elif currMapI < lastMapI:
            # Negative shift
            dir = "-"
            buf += '0'

        #print("{0} -> {1}  {2}".format(lastMapI, currMapI, dir))

    if len(buf) < 96:
        print("DROPPING SHORT FRAME: Demodulator lost lock?")
        return
    else:
        print(buf)
