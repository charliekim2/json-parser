from parsing import *


def load(fs: io.TextIOBase):
    p = Parser(fs)

    return p.parse()
