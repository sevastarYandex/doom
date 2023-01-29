from PIL import Image


f = open("data/level/1.txt", 'w')
im = Image.open("арта.png")
pixels = im.load()
x, y = im.size
ans = []
for j in range(0, y):
    s = ''
    for i in range(0, x):
        if pixels[i, j][0] == 255 and pixels[i, j][1] == 255 and pixels[i, j][2] == 255:
            s += '1'
        elif pixels[i, j][0] == 0 and pixels[i, j][1] == 0 and pixels[i, j][2] == 0:
            s += '2'
        elif pixels[i, j][0] == 255 and pixels[i, j][1] == 0 and pixels[i, j][2] == 0:
            s += '3'
        elif pixels[i, j][0] == 0 and pixels[i, j][1] == 0 and pixels[i, j][2] == 255:
            s += '4'
        elif pixels[i, j][0] == 0 and pixels[i, j][1] == 255 and pixels[i, j][2] == 0:
            s += '@'
        elif pixels[i, j][0] == 255 and pixels[i, j][1] == 255 and pixels[i, j][2] == 0:
            s += 'w'
        elif pixels[i, j][0] == 255 and pixels[i, j][1] == 0 and pixels[i, j][2] == 255:
            s += 'x'
        elif pixels[i, j][0] == 0 and pixels[i, j][1] == 255 and pixels[i, j][2] == 255:
            s += 'y'
        elif pixels[i, j][0] == 0 and pixels[i, j][1] == 0 and pixels[i, j][2] == 128:
            s += 'z'
        elif pixels[i, j][0] == 0 and pixels[i, j][1] == 128 and pixels[i, j][2] == 0:
            s += 'a'
        elif pixels[i, j][0] == 128 and pixels[i, j][1] == 0 and pixels[i, j][2] == 0:
            s += 'b'
        elif pixels[i, j][0] == 128 and pixels[i, j][1] == 128 and pixels[i, j][2] == 0:
            s += 'c'
        elif pixels[i, j][0] == 128 and pixels[i, j][1] == 0 and pixels[i, j][2] == 128:
            s += 'd'
        elif pixels[i, j][0] == 0 and pixels[i, j][1] == 128 and pixels[i, j][2] == 128:
            s += '+'
        elif pixels[i, j][0] == 128 and pixels[i, j][1] == 128 and pixels[i, j][2] == 128:
            s += '*'
        elif pixels[i, j][0] == 128 and pixels[i, j][1] == 64 and pixels[i, j][2] == 0:
            s += '}'
        elif pixels[i, j][0] == 64 and pixels[i, j][1] == 128 and pixels[i, j][2] == 0:
            s += '{'
        else:
            s += '4'
    ans.append(s)
text = '\n'.join(ans)
f.write(text)
