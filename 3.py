#!/usr/bin/python
import PIL.Image
import lsb
source = PIL.Image.open('source.png')
data = open('answer/brief.txt.asc', 'r').read()
r,g,b,a = source.split()


# src: r,g,b,a
src = [list(i.getdata()) for i in (r,g,b,a)]

data = [ord(i) for i in data]
data = [(i & 0x0f, ((i & 0xf0) >> 4)) for i in data]

embed = []
for a, b in data:
    embed.append(a)
    embed.append(b)

length = len(embed)
for j in xrange(0, length):
    for i in xrange(0, 4): 
        src[i][j] = (src[i][j] & 0xfe) | ((embed[j] >> i) & 0x01)

r = ''.join([chr(i) for i in src[0]])
g = ''.join([chr(i) for i in src[1]])
b = ''.join([chr(i) for i in src[2]])
a = ''.join([chr(i) for i in src[3]])

r = PIL.Image.fromstring('L', source.size, r)
g = PIL.Image.fromstring('L', source.size, g)
b = PIL.Image.fromstring('L', source.size, b)
a = PIL.Image.fromstring('L', source.size, a)


output = PIL.Image.merge('RGBA',(r,g,b,a))
output.save('output.png','PNG')
output.show()
