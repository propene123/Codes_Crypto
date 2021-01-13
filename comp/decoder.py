import sys
from bitstring import BitArray, BitStream

MAX_CODE_LEN = 65536
FILE_NAME = sys.argv[1]

# Gen dict
dictionary = dict()
def gen_dict():
    global dictionary
    dictionary = dict()
    for i in range(256):
        dictionary[i] = bytes([i])
    dictionary[256] = '\\section'.encode('utf-8')
    dictionary[257] = '\\label'.encode('utf-8')
    dictionary[258] = '\\begin'.encode('utf-8')
    dictionary[259] = '\\paragraph'.encode('utf-8')
    dictionary[260] = '\\end'.encode('utf-8')
    dictionary[261] = '\\subsection'.encode('utf-8')
    dictionary[262] = '\\text'.encode('utf-8')
    dictionary[263] = '\\frac'.encode('utf-8')
    dictionary[264] = '\\item'.encode('utf-8')
    dictionary[265] = '\\align'.encode('utf-8')


gen_dict()


def LZW_decode(in_codes):
    new_key = 266
    prev_code = in_codes[0]
    cur_char = dictionary[prev_code]
    out = []
    buff = b''
    prev_match = cur_char
    out.append(cur_char)
    for i in range(1, len(in_codes)):
        cur_code = in_codes[i]
        if cur_code not in dictionary:
            buff = dictionary[prev_code]
            buff += cur_char
        else:
            buff = dictionary[cur_code]
        out.append(buff)
        cur_char = bytes([buff[0]])
        if new_key < MAX_CODE_LEN:
            tmp = dictionary[prev_code] + cur_char
            dictionary[new_key] = tmp
            new_key += 1
        prev_code = cur_code
    return out





infile = open(FILE_NAME, 'rb')
in_stream = BitStream(infile)
infile.close()
in_codes = []
for i in range(len(in_stream) // 12):
    in_codes.append(in_stream.read('uint:12'))


kek = LZW_decode(in_codes)

split = FILE_NAME.split('.')
OUT_FILE = split[0] + '-decoded.tex'


with open(OUT_FILE, 'wb') as f:
    for b in kek:
        f.write(b)

