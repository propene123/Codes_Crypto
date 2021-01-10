import sys
from bitstring import BitArray, BitStream

table = []
in_bytes = None
with open(sys.argv[1], 'rb') as f:
    in_bytes = bytearray(f.read())
in_stream = BitStream(in_bytes)
symbol_total = len(in_bytes)

for i in range(0, 256):
    table.append([0, 0.0, 0.0, 0])

for i in range(0, symbol_total):
    table[in_stream.read('uint:8')][0] += 1

table[0][2] = 1.0
table[0][1] = table[0][2] - table[0][0] / symbol_total
table[0][3] = symbol_total - table[0][0]
for i in range(1, len(table)):
    prob = table[i][0] / symbol_total
    table[i][2] = table[i-1][1]
    table[i][1] = table[i][2] - prob
    table[i][3] = table[i-1][3] - table[i][0]

in_stream.pos = 0

