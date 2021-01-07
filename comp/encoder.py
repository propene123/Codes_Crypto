import sys
from bitstring import BitArray, BitStream
from heapq import heapify, heappush, heappop
from functools import total_ordering



MAX_CODE_LEN = 4096
FILE_NAME = sys.argv[1]


# Gen dict
dictionary = dict()
def gen_dict():
    global dictionary
    dictionary = dict()
    for i in range(256):
        dictionary[bytes([i])] = i
    dictionary['\\section'.encode('utf-8')] = 256
    dictionary['\\label'.encode('utf-8')] = 257
    dictionary['\\begin'.encode('utf-8')] = 258
    dictionary['\\paragraph'.encode('utf-8')] = 259
    dictionary['\\end'.encode('utf-8')] = 260
    dictionary['\\subsection'.encode('utf-8')] = 261
    dictionary['\\text'.encode('utf-8')] = 262
    dictionary['\\frac'.encode('utf-8')] = 263
    dictionary['\\item'.encode('utf-8')] = 264
    dictionary['\\align'.encode('utf-8')] = 265


gen_dict()


def LZW(b_array):
    start_code = 266
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



out = BitArray()
for b in kek:
    out.append(huff_code_dict[b])

split = FILE_NAME.split('.')
OUT_FILE = split[0] + '.lz'

with open(OUT_FILE, 'wb') as f:
    out.tofile(f)

