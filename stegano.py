from PIL import Image

def set_LSB(value, bit):
    if bit == '0':
        value = value & 254  # Clear LSB
    else:
        value = value | 1  # Set LSB
    return value

def get_LSB(value):
    return '1' if value & 1 else '0'

def get_pixxelpairs(pixlist):
    a = iter(pixlist)
    return zip(a, a)

def extract_message(image):
    im = Image.open(image)
    pixlist = list(im.getdata())
    message = ""
    for p1, p2 in get_pixxelpairs(pixlist):
        message_byte = "0b"
        for p in p1:
            message_byte += get_LSB(p)
        for p in p2:
            message_byte += get_LSB(p)
        if message_byte == "0b00000000":
            break
        message += chr(int(message_byte, 2))
    return message

def hide_message(image, message, outfile):
    message += chr(0)  # Null terminator
    im = Image.open(image)
    im = im.convert('RGBA')
    out = Image.new(im.mode, im.size)
    pixlist = list(im.getdata())
    newArray = []
    
    for i in range(len(message)):
        charInt = ord(message[i])
        cb = bin(charInt)[2:].zfill(8)  # Get 8-bit binary
        p1 = pixlist[i * 2]
        p2 = pixlist[i * 2 + 1]
        newp1 = []
        newp2 = []
        
        for j in range(4):  # First 4 bits in p1, last 4 in p2
            newp1.append(set_LSB(p1[j], cb[j]))
            newp2.append(set_LSB(p2[j], cb[j + 4]))

        newArray.append(tuple(newp1))
        newArray.append(tuple(newp2))

    newArray.extend(pixlist[len(message) * 2:])  # Keep rest unchanged
    out.putdata(newArray)
    out.save(outfile)
    return out

if __name__ == "__main__":
    hide_message('test.png', 'glen', 'stageno.png')
    print(extract_message('stageno.png'))
