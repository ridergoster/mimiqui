import sys
from PIL import Image

class Steganography:
    '''
    Steganography
    - Encode data inside a picture
    - Decode data from an encoded picture
    '''

    def __init__(self,  url):
        '''
        Constructor for Steganography class

        @param self : Steganography
        @param url  : String
        @return     : None
        '''
        self.url = url
        self.image = Image.open(self.url)
        self.width, self.height = self.image.size

    def encode(self, data):
        '''
        Encode data in a picture

        @param self : Steganography
        @param data : byteArray
        @return     : Image
        '''
        lengthData = len(data)

        data = [ord(c) for c in str(lengthData)] + [ord('@')] + data
        data = ''.join([format(char, 'b').zfill(8) for char in data])
        data += '0' * ((3 - (len(data) % 3)) % 3)

        lengthBits = len(data)
        nbPixel = self.width * self.height
        nbColors = nbPixel * 3
        index = 0

        if (lengthBits > nbColors):
            raise Exception('Data too long.')
        if (self.image.mode not in ['RGB', 'RGBA']):
            raise Exception('Image must be RGB or RGBA.')

        encoded = self.image.copy()

        for x in range(self.height):
            for y in range(self.width):
                if index + 3 <= lengthBits:
                    pixel = self.image.getpixel((y, x))
                    r = pixel[0] & ~1 | int(data[index])
                    g = pixel[1] & ~1 | int(data[index+1])
                    b = pixel[2] & ~1 | int(data[index+2])

                    if self.image.mode == 'RGBA':
                        encoded.putpixel((y, x), (r, g, b, pixel[3]))
                    else:
                        encoded.putpixel((y, x), (r, g, b))
                index += 3

        return encoded

    def decode(self):
        '''
        Decode data from a picture

        @param self : Steganography
        @return     : byteArray
        '''
        flag, limit, count, buff, result = False, 0, 0, 0, []
        for x in range(self.height):
            for y in range(self.width):
                pixel = self.image.getpixel((y, x))[:3]
                for color in pixel:
                    buff += ((color & 1) << (8 - 1 - count))
                    count += 1
                    if count == 8:
                        result.append(buff)
                        buff, count = 0, 0
                        if chr(result[-1]) == "@" and flag == False:
                            flag = True
                            limit = int("".join([chr(c) for c in result[:len(result)-1]]))
                            result = []
                if len(result) == limit and flag == True:
                    return result
