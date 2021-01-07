import sys
from bitstring import BitArray, BitStream



MAX_CODE_LEN = 4096
FILE_NAME = sys.argv[1]


# Gen dict
dictionary = dict()
for i in range(256):
    dictionary[bytes([i])] = i

def LZW(b_array):
    start_code = 256
    tmp_buff = b''
    out = []
    for b in b_array:
        b_str = bytes([b])
        if tmp_buff + b_str in dictionary:
            tmp_buff = tmp_buff + b_str
        else:
            out.append(dictionary[tmp_buff])
            if start_code < MAX_CODE_LEN:
                dictionary[tmp_buff + b_str] = start_code
                start_code += 1
            tmp_buff = b_str
    if tmp_buff in dictionary:
        out.append(dictionary[tmp_buff])
    return out

infile = open(FILE_NAME, 'rb')
file_bytes = bytearray(infile.read())
infile.close()
kek = LZW(file_bytes)
out = BitArray()
for b in kek:
    out.append(f'uint:12={b}')

split = FILE_NAME.split('.')
OUT_FILE = split[0] + '.lz'

with open(OUT_FILE, 'wb') as f:
    out.tofile(f)

