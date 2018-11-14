'''
s = bytearray()
for i in range(0,15):
    s += i.to_bytes(1,'big')
    print(len(s))

print(s)

for i in range(0,15):
    print(s.pop())
'''

r = {}
r[1] = "1"
r[2] = "2"
r[3] = "3"
r[4] = "4"
r["asdf"] = "asdf"
print(len(r))