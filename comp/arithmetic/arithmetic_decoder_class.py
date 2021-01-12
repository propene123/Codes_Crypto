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
        blocks = len(in_stream)//32
        block_array = []
        for i in range(blocks):
            block = in_stream.read('uint:32')
            for c in str(block):
                block_array.append(int(c))
        code = ''
        for i in range(9):
            code += str(block_array.pop(0))
        code = int(code)
        cur_char = None
        while cur_char != 'eof':
            print(f'code={code}')
            index = ((code - low+1)*self.symbol_num-1)/(high-low+1)
            index = int(index)
            print(f'index={index}')
            upper_key = keys[3]
            lower_key = keys[0]
            for key in keys:
                current = self.table[key][3]
                if current > index:
                    if self.table[upper_key][3] < index or current < self.table[upper_key][3]:
                        upper_key = key
                if current <= index:
                    if self.table[lower_key][3] > index or current > self.table[lower_key][3]:
                        lower_key = key
            cur_char = lower_key
            out_stream.append(f'uint:8={cur_char}')
            diff = high-low
            high = low + ((diff+1)*self.table[upper_key][3])//10 -1
            low = low + ((diff+1)*self.table[lower_key][3])//10
            high_str = str(high)
            low_str = str(low)
            if high_str[0] == low_str[0]:
                print(f'old high={high}')
                print(f'old low={low}')
                print(f'old code={code}')
                high = (high % 10**8) * 10
                high += 9
                low = (low % 10**8) * 10
                code = (code % 10**8) * 10
                code += block_array.pop(0)
                print(f'new high={high}')
                print(f'new low={low}')
                print(f'in stream={block_array}')
                print(f'new code={code}')





# in_bytes = bytearray()
# with open('out.lz', 'rb') as f:
    # in_bytes = bytearray(f.read())

# in_stream = BitStream(in_bytes)
# decoder = ArithmeticDecoder(8, dict())
# decoder.decode(in_stream)
