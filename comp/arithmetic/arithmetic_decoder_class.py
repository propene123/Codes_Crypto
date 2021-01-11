from decimal import *
from bitstring import BitArray, BitStream


class ArithmeticDecoder():
    def __init__(self, symbol_size, symbol_num, init_dict):
        self.table = init_dict
        self.symbol_size = symbol_size
        self.symbol_num = symbol_num
        getcontext().prec = 999
