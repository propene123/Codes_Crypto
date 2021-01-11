from decimal import *
from bitstring import BitArray, BitStream


class ArithmeticDecoder():
    def __init__(self, symbol_size, symbol_num, init_dict):
        self.table = init_dict
        self.symbol_size = symbol_size
        getcontext().prec = 999


    def decode(self, in_stream):
        low = 000000000
        high = 999999999
        code = in_stream.read('uint:32')
        index = ((code - low)*self.symbol_num-1)/(high-low+1)
        index = int(index)




in_bytes = bytearray()
with open('out.lz', 'rb') as f:
    in_bytes = bytearray(f.read())

in_stream = BitStream(in_bytes)
decoder = ArithmeticDecoder(8, dict())
decoder.decode(in_stream)
