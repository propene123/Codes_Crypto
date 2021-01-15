import sys
import math
from bitstring import BitArray, BitStream

MAX_CODE_LEN = 2**16
FILE_NAME = sys.argv[1]

# Gen dict
dictionary = dict()


def add_to_dict(code, phrase):
    global dictionary
    for i in range(1, len(phrase)+1):
        dictionary[code] = phrase[0:i].encode('utf-8')
        code += 1
    return code


def gen_dict():
    global dictionary
    dictionary = dict()
    for i in range(256):
        dictionary[i] = bytes([i])
    code = 257
    code = add_to_dict(257, '\\section')
    code = add_to_dict(code, '\\label')
    code = add_to_dict(code, '\\begin')
    code = add_to_dict(code, '\\paragraph')
    code = add_to_dict(code, '\\end')
    code = add_to_dict(code, '\\subsection')
    code = add_to_dict(code, '\\text')
    code = add_to_dict(code, '\\frac')
    code = add_to_dict(code, '\\item')
    code = add_to_dict(code, '\\align')
    code = add_to_dict(code, 'width')
    code = add_to_dict(code, 'height')
    code = add_to_dict(code, '\\sqrt')
    code = add_to_dict(code, '\\includegraphics')
    return code




def LZW_decode(in_codes):
    new_key = gen_dict()
    symbol_width = 9
    prev_code = in_codes.read(f'uint:{symbol_width}')
    cur_char = dictionary[prev_code]
    out = []
    buff = b''
    prev_match = cur_char
    out.append(cur_char)
    while in_codes.pos != in_codes.len:
        if in_codes.len - in_codes.pos < symbol_width:
            break
        cur_code = in_codes.read(f'uint:{symbol_width}')
        if cur_code == 256:
            new_key = gen_dict()
            symbol_width = 9
            prev_code = in_codes.read(f'uint:{symbol_width}')
            cur_char = dictionary[prev_code]
            buff = b''
            prev_match = cur_char
            out.append(cur_char)
            continue
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
            if math.log2(new_key) == symbol_width and symbol_width < 16:
                symbol_width += 1
            new_key += 1
        prev_code = cur_code
    return out





split = FILE_NAME.split('.')
OUT_FILE = split[0] + '-decoded.tex'


infile = open(FILE_NAME, 'rb')
file_bytes = bytearray(infile.read())
if len(file_bytes) == 0:
    with open(OUT_FILE, 'wb') as f:
        f.write(file_bytes)
    sys.exit('input file has 0 bytes so will not decompress. Writing original file with new name')
in_stream = BitStream(infile)
infile.close()


bits_rem_from_stream = 0
pad_bits = in_stream.read('uint:8')
rle_blocks = in_stream.read('uint:9')
bits_rem_from_stream += 17
huff_code_lengths = []
current_huff_index = 0
for i in range(rle_blocks):
    rle_or_no = in_stream.read('uint:1')
    bits_rem_from_stream += 1
    if rle_or_no == 1:
        rle_number = in_stream.read('uint:8')
        rle_length = in_stream.read('uint:8')
        bits_rem_from_stream += 16
        for j in range(current_huff_index, current_huff_index+rle_number):
            if rle_length != 0:
                huff_code_lengths.append((j, rle_length))
        current_huff_index += rle_number
    if rle_or_no == 0:
        rle_length = in_stream.read('uint:8')
        bits_rem_from_stream += 8
        if rle_length != 0:
            huff_code_lengths.append((current_huff_index, rle_length))
        current_huff_index += 1
        



# for i in range(256):
    # length = in_stream.read('uint:8')
    # if length != 0:
        # huff_code_lengths.append((i, length))

huff_code_lengths.sort(key=lambda x: (x[1], x[0]))
huff_code_dict = dict()
current_huff_code = 0
for c in range(len(huff_code_lengths)):
    huff_code_dict[current_huff_code] = (huff_code_lengths[c][0], huff_code_lengths[c][1])
    if c == len(huff_code_lengths) - 1:
        break
    current_huff_code = (current_huff_code + 1) << ((huff_code_lengths[c+1][1]) - (huff_code_lengths[c][1]))

current_huff_code = 0
current_code_len = 0
test_out_bytes = BitArray()
# new_stream_len = len(in_stream) - 257 * 8
new_stream_len = len(in_stream) - bits_rem_from_stream

for i in range(new_stream_len):
    if i == new_stream_len - pad_bits:
        break
    tmp_code_bit = in_stream.read('uint:1')
    current_code_len+=1
    current_huff_code = (current_huff_code << 1)+tmp_code_bit
    if current_huff_code in huff_code_dict and current_code_len == huff_code_dict[current_huff_code][1]:
        test_out_bytes.append(f'uint:8={huff_code_dict[current_huff_code][0]}')
        current_huff_code = 0
        current_code_len = 0


in_stream = BitStream(test_out_bytes)

kek = LZW_decode(in_stream)



with open(OUT_FILE, 'wb') as f:
    for b in kek:
        f.write(b)

