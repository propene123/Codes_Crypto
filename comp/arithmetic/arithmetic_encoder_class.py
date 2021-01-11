from decimal import *
from bitstring import BitArray, BitStream

class ArithmeticEncoder():
    def __init__(self, symbol_size, symbol_num, init_dict):
        self.table = init_dict
        self.symbol_size = symbol_size
        self.symbol_num = symbol_num +1
        getcontext().prec = 999

    def gen_dict_from_file(self, in_stream):
        symbol_dict = dict()
        for i in range(0, self.symbol_num-1):
            symbol = in_stream.read(f'uint:{self.symbol_size}')
            if symbol not in symbol_dict:
                symbol_dict[symbol] = 1
            else:
                symbol_dict[symbol] += 1
        self.table['eof'] = [1,0.0,0.0,0]
        for sym, freq in symbol_dict.items():
            self.table[sym] = [freq, 0.0, 0.0, 0]

        table_keys = list(self.table.keys())
        init_key = table_keys[0]

        self.table[init_key][3] = self.symbol_num - self.table[init_key][0]
        self.table[init_key][2] = Decimal(1.0)
        self.table[init_key][1] = Decimal(Decimal(self.table[init_key][2]) - Decimal(Decimal(self.table[init_key][0]) / Decimal(self.symbol_num)))
        for i in range(1, len(table_keys)):
            key = table_keys[i]
            prev_key = table_keys[i-1]
            prob  = Decimal(Decimal(self.table[key][0]) / Decimal(self.symbol_num))
            self.table[key][2] = self.table[prev_key][1]
            self.table[key][1] = Decimal(Decimal(self.table[key][2]) - prob)
            self.table[key][3] = self.table[prev_key][3] - self.table[key][0]
        self.table[table_keys[len(table_keys)-1]][1] = Decimal(0)
        print(self.table)


    def enc_char(self, char, low, high, low_int, high_int, out):
            diff = high - low
            high = low + diff * float(self.table[char][2])
            low = low + diff * float(self.table[char][1])
            high_int = int(high * (10**9)) -1
            low_int = int(low * (10**9))
            high_str = str(high_int)
            low_str = str(low_int)
            if high_str[0] == low_str[0]:
                out.append(high_int // 10**8)
                high_int = (high_int % 10**8) * 10
                high_int += 9
                low_int = (low_int % 10**8) * 10
                high = (high_int+1) / (10**9)
                low = low_int / (10**9)
            return low, high, low_int, high_int


    def encode(self, in_stream):
        low_int = 000000000
        high_int = 999999999
        low = 0.0
        high = 1.0
        out = []
        for i in range(0, self.symbol_num-1):
            in_char = in_stream.read(f'uint:{self.symbol_size}')
            low, high, low_int, high_int = self.enc_char(in_char, low, high, low_int, high_int, out)
        low, high, low_int, high_int = self.enc_char('eof', low, high, low_int, high_int, out)
        out_bytes = BitArray()
        block_idx = 0
        tmp_out = ''
        for i in range(len(out)):
            tmp_out += str(out[i])
            block_idx+=1
            if block_idx==9:
                out_bytes.append(f'uint:32={int(tmp_out)}')
                block_idx = 0
                tmp_out = ''
        if tmp_out != '':
            out_bytes.append(f'uint:32={int(tmp_out)}')
        out_bytes.append(f'uint:32={low_int}')
        print(out)
        print(low_int)
        return out_bytes
