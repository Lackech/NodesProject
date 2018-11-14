s = bytearray()
for i in range(0,15):
    s += i.to_bytes(1,'big')
    print(len(s))

print(s)

for i in range(0,15):
    print(s.pop())


