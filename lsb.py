#!/usr/bin/python
# -*- coding: utf-8 -*-

import PIL.Image as Image
def getlayer(srcLimg,layer):
    s = list(srcLimg.getdata())
    r = ''

    testlayer = 1 << layer

    for i in s:
        if i & testlayer:
            r += chr(255)
        else:
            r += chr(0)
    ret = Image.fromstring('L',srcLimg.size,r)
    return(ret)

def setbit(src,pos,v):
    if v:
        return src | (0x01 << pos)
    else:
        return src & (0xFF ^ (0x01 << pos))

def embed(cover,data,layer=0):
#   print(data + '.')
    cdata = list(cover.getdata())
    print data[0:5]
    exit()
    
    maxlen = len(data)
    r = [0] * maxlen

    for i in xrange(0, maxlen):
        h = cdata[i]
        if data:
            r[i] = setbit(h, layer, data[i] == '1')
        else:
            r[i] = h
    r = ''.join([chr(i) for i in r])

    return(Image.fromstring('L',cover.size,r))

def write(rgbimg,datastr):
    fullsize = rgbimg.size[0] * rgbimg.size[1] 
    usesize = fullsize * 3
    datasize = len(datastr)
    if datasize>usesize-20:
        print('Cover Picture Can save only %d bits. Data exceeded.' % (datasize))
        return False
    sizestr = bin(datasize)[2:].zfill(20)
    datastr = sizestr + datastr

    r,g,b = rgbimg.split()[0:3]
    r = embed(r,datastr[0:fullsize-1],0)
    g = embed(g,datastr[fullsize:fullsize + fullsize - 1],0)
    b = embed(b,datastr[2*fullsize:],0)

    return(Image.merge('RGB',(r,g,b)))

def extract(rgbimg):
#    usesize = rgbimg.size[0] * rgbimg.size[1] * 3 / 8
    r,g,b = rgbimg.split()
    datastr = getlayer(r,0).tostring() + getlayer(g,0).tostring() + getlayer(b,0).tostring()
    datastr = datastr.replace(chr(0),'0')
    datastr = datastr.replace(chr(255),'1')
    datasize = int('0b' + datastr[0:20],2)
    if datasize > len(datastr) - 20:
        return False
    datastr = datastr[20:20 + datasize]
#   print('Extracted: ' + datastr)
    return(datastr)

def str2binstr(s):
    return ''.join([bin(ord(x))[2:].zfill(8) for x in s])

def readfile(filename):
    fs = open(filename,'r').read()
    return(str2binstr(fs))

def readstr(binstr):
    r = ''
    while binstr != '':
        r += chr(int('0b' + binstr[0:8],2))
	binstr = binstr[8:]
    return r
"""
edata = 'a' * 200

srcimg = Image.open('emotion.png')#'lena_std.tif')
srcdat = str2binstr(edata)
#print srcdat
#srcdat = readfile('')
outimg = write(srcimg,srcdat)
outimg.show()

fetch = extract(outimg)
#print fetch
fetch = readstr(fetch)
if not fetch == edata:
    print fetch
"""
