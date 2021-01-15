import sys
import math
from bitstring import BitArray, BitStream
from heapq import heapify, heappush, heappop
from functools import total_ordering



MAX_CODE_LEN = 2**16
FILE_NAME = sys.argv[1]

# Gen dict
dictionary = dict()
def add_to_dict(phrase, code):
    global dictionary
    for i in range(1,len(phrase)+1):
        dictionary[phrase[0:i].encode('utf-8')] = code
        code += 1
    return code



def gen_dict():
    global dictionary
    dictionary = dict()
    for i in range(256):
        dictionary[bytes([i])] = i
    # 256 reserved for clear code
    code = 257
    code = add_to_dict('\\section', 257)
    code = add_to_dict('\\label', code)
    code = add_to_dict('\\begin', code)
    code = add_to_dict('\\paragraph', code)
    code = add_to_dict('\\end', code)
    code = add_to_dict('\\subsection', code)
    code = add_to_dict('\\text', code)
    code = add_to_dict('\\frac', code)
    code = add_to_dict('\\item', code)
    code = add_to_dict('\\align', code)
    code = add_to_dict('width', code)
    code = add_to_dict('height', code)
    code = add_to_dict('\\sqrt', code)
    code = add_to_dict('\\includegraphics', code)
    return code
    





def LZW(b_array):
    start_code = gen_dict()
    symbol_width = 9
    tmp_buff = b''
    out = BitArray()
    old_c_ratio = 0
    new_c_ratio = 0
    c_threshold = 1.1
    comp_len = 0
    code_len = 0
    for b in b_array:
        comp_len += 1
        b_str = bytes([b])
        if tmp_buff + b_str in dictionary:
            # extend input
            tmp_buff = tmp_buff + b_str
        else:
            # output dict match
            out.append(f'uint:{symbol_width}={dictionary[tmp_buff]}')
            if math.ceil(math.log2(start_code)) > symbol_width and symbol_width < 16:
                symbol_width += 1
            code_len += symbol_width
            if start_code < MAX_CODE_LEN:
                old_c_ratio = ((comp_len-1)*8)/(code_len)
                dictionary[tmp_buff + b_str] = start_code
                start_code += 1
            if start_code == MAX_CODE_LEN:
                new_c_ratio = ((comp_len-1)*8)/(code_len)
                if (old_c_ratio/new_c_ratio) > c_threshold:
                    start_code = gen_dict()
                    # out clear code
                    out.append(f'uint:{symbol_width}=256')
                    symbol_width = 9
            tmp_buff = b_str
    if tmp_buff in dictionary:
        out.append(f'uint:{symbol_width}={dictionary[tmp_buff]}')
    return out

infile = open(FILE_NAME, 'rb')
file_bytes = bytearray(infile.read())
infile.close()
split = FILE_NAME.split('.')
OUT_FILE = split[0] + '.lz'

if len(file_bytes) == 0:
    with open(OUT_FILE, 'wb') as f:
        f.write(file_bytes)
    sys.exit('Input file contains 0 bytes will not compress. Writing original file as output with new name')

kek = LZW(file_bytes)
out = BitArray()
# for b in kek:
    # out.append(f'uint:16={b}')

if len(kek) % 8 != 0:
    for i in range(8-(len(kek) % 8)):
        kek.append('0b0')


with open(OUT_FILE, 'wb') as f:
    kek.tofile(f)

kek = bytearray()
with open(OUT_FILE, 'rb') as f:
    kek = bytearray(f.read())



# This was huffman testing

prob_dict = dict()
for c in kek:
    if c in prob_dict:
        prob_dict[c] += 1
    else:
        prob_dict[c] = 1
for key, value in prob_dict.items():
    prob_dict[key] = value/len(kek)



@total_ordering
class Node():
    def __init__(self, prob, cont=None):
        self.cont = cont
        self.left_child = None
        self.right_child = None
        self.prob = prob

    def __eq__(self, x):
        return self.prob == x.prob

    def __lt__(self, x):
        return self.prob < x.prob

    def get_prob(self):
        return self.prob

    def get_cont(self):
        return self.cont

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def set_right_child(self, child):
        self.right_child = child

    def set_left_child(self, child):
        self.left_child = child



# More huffman testing

heap = []
for key, var in prob_dict.items():
    heap.append(Node(var, key))
heapify(heap)


while len(heap) != 1:
    right_child = heappop(heap)
    left_child = heappop(heap)
    new_node = Node(right_child.get_prob() + left_child.get_prob())
    new_node.set_right_child(right_child)
    new_node.set_left_child(left_child)
    heappush(heap, new_node)

huff_code_dict = dict()


def gen_huff_codes(cur_code, node):
    global huff_code_dict
    if node.get_left_child() is not None:
        gen_huff_codes(cur_code+'0', node.get_left_child())
    if node.get_right_child() is not None:
        gen_huff_codes(cur_code+'1', node.get_right_child())
    else:
        huff_code_dict[node.get_cont()] = cur_code


# More huffman testing

gen_huff_codes('0b', heap[0])

huff_tuple_list = []
for key, value in huff_code_dict.items():
    huff_tuple_list.append((key, len(value)-2))

huff_tuple_list.sort(key=lambda x: (x[1], x[0]))
huff_code_dict = dict()
current_huff_code = 0
for c in range(len(huff_tuple_list)):
    huff_code_dict[huff_tuple_list[c][0]] = (current_huff_code, huff_tuple_list[c][1])
    if c == len(huff_tuple_list) - 1:
        break
    current_huff_code = (current_huff_code + 1) << ((huff_tuple_list[c+1][1]) - (huff_tuple_list[c][1]))


out_huff_bytes = BitArray()
for k in kek:
    out_huff_bytes.append(f'uint:{huff_code_dict[k][1]}={huff_code_dict[k][0]}')

pad_bits = 8 - (len(out_huff_bytes) % 8)
for i in range(pad_bits):
    out_huff_bytes.append('0b0')

huff_tree_enc = BitArray()
for i in range(256):
    if i not in huff_code_dict:
        huff_tree_enc.append(f'uint:8={0}')
    else:
        huff_tree_enc.append(f'uint:8={huff_code_dict[i][1]}')

huff_tree_enc.append(out_huff_bytes)
huff_tree_enc.prepend(f'uint:8={pad_bits}')


with open(OUT_FILE, 'wb') as f:
    huff_tree_enc.tofile(f)


in_huff_stream = BitStream()
with open(OUT_FILE, 'rb') as f:
    in_huff_stream = BitStream(f)

new_huff_dict = dict()
for key, value in huff_code_dict.items():
    new_huff_dict[value[0]] = (key, value[1])


current_huff_code = 0
current_code_len = 0
test_out_bytes = BitArray()
for i in range(len(in_huff_stream)):
    if i == len(in_huff_stream) - pad_bits:
        break
    tmp_code_bit = in_huff_stream.read('uint:1')
    current_code_len+=1
    current_huff_code = (current_huff_code << 1)+tmp_code_bit
    if current_huff_code in new_huff_dict and current_code_len == new_huff_dict[current_huff_code][1]:
        test_out_bytes.append(f'uint:8={new_huff_dict[current_huff_code][0]}')
        current_huff_code = 0
        current_code_len = 0

# with open(OUT_FILE, 'wb') as f:
    # test_out_bytes.tofile(f)
