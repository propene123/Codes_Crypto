
in_bytes = bytearray()
with open('./1mbtext.tex', 'rb') as f:
    in_bytes = bytearray(f.read())

comp_bytes = bytearray()
with open('out.zip', 'rb') as f:
    comp_bytes = bytearray(f.read())


print(len(in_bytes)/len(comp_bytes))
