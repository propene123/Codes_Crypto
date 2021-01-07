from bitstring import BitArray, BitStream



MAX_CODE_LEN = 4096

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

infile = open("./testFile.tex", 'rb')
file_bytes = bytearray(infile.read())
infile.close()
kek = LZW(file_bytes)
out = BitArray()
for b in kek:
    out.append(f'uint:12={b}')

with open('out.lz', 'wb') as f:
    out.tofile(f)


kek_bytes = None
with open('out.lz', 'rb') as f:
    kek_bytes = bytearray(f.read())

print(len(kek_bytes))
print(len(file_bytes))
print(len(kek))
print(kek[len(kek)-2])
