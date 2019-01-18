"""
stx.py
Orbcomm STX Decoder v1.0
https://github.com/sam210723/orbcomm-rx
"""


class STX:
    def __init__(self):
        self.df = 0

    def decode(self, symbols):
        # Gray coded symbol maps
        symMap = [0, 1, 3, 2]
        #symMap = [3, 2, 0, 1]

        lastSym = None
        frame = ''

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
                frame += '1'
            elif currMapI == 3 and lastMapI == 0:
                # Negative shift
                dir = "-"
                frame += '0'
            elif currMapI > lastMapI:
                # Positive shift
                dir = "+"
                frame += '1'
            elif currMapI < lastMapI:
                # Negative shift
                dir = "-"
                frame += '0'

            #print("{0} -> {1}  {2}".format(lastMapI, currMapI, dir))

        if len(frame) < 96:
            self.df += 1
            print("SHORT FRAME ({}): {} bits, {}%".format(self.df, 96-len(frame), round((len(frame)/96)*100, 1)))
            return
        else:
            return
            print(frame)
