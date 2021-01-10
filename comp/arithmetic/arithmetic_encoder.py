import sys
from decimal import *
from bitstring import BitArray, BitStream


getcontext().prec = 999

table = dict()
in_bytes = None
with open(sys.argv[1], 'rb') as f:
    in_bytes = bytearray(f.read())
in_stream = BitStream(in_bytes) 
symbol_total = len(in_bytes)
symbol_dict = dict()

for i in range(0, symbol_total):
    symbol = in_stream.read('uint:8')
    if symbol not in symbol_dict:
        symbol_dict[symbol] = 1
    else:
        symbol_dict[symbol] += 1


cum_freq_total = symbol_total - 1
for sym, freq in symbol_dict.items():
    if sym != 10:
        table[sym] = [freq, 0.0, 0.0, 0]

table_keys = list(table.keys())
init_key = table_keys[0]

table[init_key][3] = cum_freq_total - table[init_key][0]
table[init_key][2] = Decimal(1.0)
table[init_key][1] = Decimal(table[init_key][2] - Decimal(table[init_key][0] / cum_freq_total))
for i in range(1, len(table_keys)):
    key = table_keys[i]
    prev_key = table_keys[i-1]
    prob  = Decimal(Decimal(table[key][0]) / Decimal(cum_freq_total))
    table[key][2] = table[prev_key][1]
    table[key][1] = Decimal(table[key][2] - prob)
    table[key][3] = table[prev_key][3] - table[key][0]




print(table)

in_stream.pos = 0
low_int = 000000000
high_int = 999999999
low = 0.0
high = 1.0
out = []

for i in range(0, symbol_total-1):
    in_char = in_stream.read('uint:8')
    diff = high - low
    high = low + diff * float(table[in_char][2])
    low = low + diff * float(table[in_char][1])
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



print(out)
print(low_int)


