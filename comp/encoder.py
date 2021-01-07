from bitstring import BitArray, BitStream



# Gen dict
dictionary = dict()
for i in range(255):
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
            dictionary[tmp_buff + b_str] = start_code
            start_code += 1
            tmp_buff = b_str
    if tmp_buff in dictionary:
        out.append(tmp_buff)
    return out






infile = open("./testFile.tex", 'rb')
file_bytes = bytearray(infile.read())
infile.close()
kek = LZW(file_bytes)

