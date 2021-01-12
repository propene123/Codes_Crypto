import sys
from decimal import *
from bitstring import BitArray, BitStream
from arithmetic_encoder_class import ArithmeticEncoder
from arithmetic_decoder_class import ArithmeticDecoder

in_bytes = None
with open(sys.argv[1], 'rb') as f:
    in_bytes = bytearray(f.read())
in_stream = BitStream(in_bytes) 
kek = len(in_bytes) #asfafaf
encoder = ArithmeticEncoder(8, len(in_bytes), dict())
encoder.gen_dict_from_file(in_stream)
in_stream.pos = 0
out_bytes = encoder.encode(in_stream)

with open('out.lz', 'wb') as f:
    out_bytes.tofile(f)

out_bytes = None
with open('out.lz', 'rb') as f:
    in_bytes = bytearray(f.read())
    kek_stream = BitStream(in_bytes)
    decoder = ArithmeticDecoder(8, kek+1, encoder.table)
    out_bytes = decoder.decode(kek_stream)


with open('decoded.txt', 'wb') as f:
    out_bytes.tofile(f)
