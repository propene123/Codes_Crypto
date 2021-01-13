import sys
from bitstring import BitArray, BitStream

MAX_CODE_LEN = 65536
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
for i in range(len(in_stream) // 16):
    in_codes.append(in_stream.read('uint:16'))


kek = LZW_decode(in_codes)

split = FILE_NAME.split('.')
OUT_FILE = split[0] + '-decoded.tex'


with open(OUT_FILE, 'wb') as f:
    for b in kek:
        f.write(b)

