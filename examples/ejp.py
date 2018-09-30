code = bytearray()
for i in range(0,20):
    code += i.to_bytes(2,'big')
    print(code)
    decode = int.from_bytes(code,'big')
    #print(decode)
    string = str(i) + 'adf'
    #print(string)

for i in range(0,20):
    print(code[i*2]*256 + code[i*2+1])



