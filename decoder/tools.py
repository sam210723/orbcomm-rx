# Console colour characters
colours = {}
colours['HEADER'] = '\033[95m'
colours['OKBLUE'] = '\033[94m'
colours['OKGREEN'] = '\033[92m'
colours['WARNING'] = '\033[93m'
colours['FAIL'] = '\033[91m'
colours['ENDC'] = '\033[0m'
colours['BOLD'] = '\033[1m'
colours['UNDERLINE'] = '\033[4m'


def set_colour(colour="ENDC"):
    """
    Sets console colour. Defaults to no colour.
    :param colour: Colour to set
    """

    print(colours[colour], end='')


def printc(data, colour="ENDC"):
    set_colour(colour)
    print(data)
    set_colour()