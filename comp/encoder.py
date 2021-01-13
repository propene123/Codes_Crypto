import sys
import math
from bitstring import BitArray, BitStream
from heapq import heapify, heappush, heappop
from functools import total_ordering



MAX_CODE_LEN = 65536
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
    symbol_width = 16
    tmp_buff = b''
    out = BitArray()
    old_c_ratio = 0
    new_c_ratio = 0
    c_threshold = 1
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
            code_len += 16
            if start_code < MAX_CODE_LEN:
                old_c_ratio = ((comp_len-1)*8)/(code_len)
                dictionary[tmp_buff + b_str] = start_code
                start_code += 1
            if start_code == MAX_CODE_LEN:
                new_c_ratio = ((comp_len-1)*8)/(code_len)
                if (old_c_ratio/new_c_ratio) > c_threshold:
                    start_code = gen_dict()
            tmp_buff = b_str
    if tmp_buff in dictionary:
        out.append(f'uint:{symbol_width}={dictionary[tmp_buff]}')
    return out

infile = open(FILE_NAME, 'rb')
file_bytes = bytearray(infile.read())
infile.close()
kek = LZW(file_bytes)
out = BitArray()
# for b in kek:
    # out.append(f'uint:16={b}')

split = FILE_NAME.split('.')
OUT_FILE = split[0] + '.lz'

with open(OUT_FILE, 'wb') as f:
    kek.tofile(f)

kek = bytearray()
with open(OUT_FILE, 'rb') as f:
    kek = bytearray(f.read())


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

gen_huff_codes('0b', heap[0])

