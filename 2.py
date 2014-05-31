#!/usr/bin/python
import PIL.Image
import lsb,sys
source = PIL.Image.open('quelle.png')
r,g,b,a = source.split()

# src: r,g,b,a
src = [list(i.getdata()) for i in (r,g,b,a)]

for i in xrange(0, 4): 
    src[i] = [x & 0x01 for x in src[i]]

length = len(src[0])
combined = []
for i in xrange(0, length):
    value = (src[0][i] << 0) + (src[1][i] << 1) + (src[2][i] << 2) + (src[3][i] << 3)
    combined.append(value)

output = []
length = len(combined)
i=0
while i + 1 < length:
    l = combined[i]
    r = combined[i+1]
    output.append((r << 4) + l)
    i += 2

output = output[:141*1024]
outputStr = ''.join([chr(i) for i in output])

open('extracted_data_littleendian.bin', 'w+').write(outputStr)
