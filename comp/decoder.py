from bitstring import BitArray, BitStream

MAX_CODE_LEN = 4096

# Gen dict
dictionary = dict()
for i in range(256):
    dictionary[i] = bytes([i])


def LZW_decode(in_codes):
    new_key = 256
    prev_code = in_codes[0]
    cur_char = dictionary[prev_code]
    out = []
    buff = b''
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





infile = open('out.lz', 'rb')
in_stream = BitStream(infile)
infile.close()
in_codes = []
for i in range(len(in_stream) // 12):
    in_codes.append(in_stream.read('uint:12'))


kek = LZW_decode(in_codes)

with open("decoded.tex", 'wb') as f:
    for b in kek:
        f.write(b)






