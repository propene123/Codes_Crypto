from decimal import *
from bitstring import BitArray, BitStream


class ArithmeticDecoder():
    def __init__(self, symbol_size, symbol_num, init_dict):
        self.table = init_dict
        self.symbol_size = symbol_size
        self.symbol_num = symbol_num
        getcontext().prec = 999


    def decode(self, in_stream):
        out_stream = BitArray()
        low = 000000000
        high = 999999999
        keys = list(self.table.keys())
        code = in_stream.read('uint:32')
        index = ((code - low+0)*self.symbol_num-1)/(high-low+1)
        index = int(index)
        cur_char = None
        # while cur_char != 'eof':
        upper_key = keys[0]
        lower_key = keys[len(keys)-1]
        for key in keys:
            current = self.table[key]
            if current[3] > index and current[3] < self.table[upper_key][3]:
                upper_key = key
            if current[3] < index and current[3] > self.table[lower_key][3]:
                lower_key = key
        out_stream.append(f'uint:8={self.table[lower_key][0]}')




# in_bytes = bytearray()
# with open('out.lz', 'rb') as f:
    # in_bytes = bytearray(f.read())

# in_stream = BitStream(in_bytes)
# decoder = ArithmeticDecoder(8, dict())
# decoder.decode(in_stream)
