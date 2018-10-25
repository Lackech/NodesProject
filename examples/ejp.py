list = bytearray()
for a in range(0,10):
    list += a.to_bytes(1,'big')

list += int(ord('a')).to_bytes(1,'big')
list += int(ord('b')).to_bytes(1,'big')
list += int(ord('c')).to_bytes(1,'big')

for a in range(0,13):
    print(chr(list.pop()))


