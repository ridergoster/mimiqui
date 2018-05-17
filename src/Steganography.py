import sys
from PIL import Image

def dataToInput(data, index, compression):
    result = 0
    for i in range(compression)[::-1]:
        result += (int(data[index]) << i)
        index += 1
    return result

class Steganography:
    '''
    Steganography
    - Encode data inside a picture
    - Decode data from an encoded picture
    '''

    def __init__(self,  url, compression=4):
        '''
        Constructor for Steganography class

        @param self : Steganography
        @param url  : String
        @return     : None
        '''
        self.url = url
        self.image = Image.open(self.url)
        self.compression = compression if (compression <= 8 and compression > 0) else 4
        self.width, self.height = self.image.size

    @staticmethod
    def dataToInput(data, index, compression):
        '''
        sum binary with padding for compression

        @param data        : String
        @param index       : Number
        @param compression : Number
        @return            : Number
        '''
        result = 0
        for i in range(compression)[::-1]:
            result += (int(data[index]) << i)
            index += 1
        return result

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
        data += '0' * (((3*self.compression) - (len(data) % (3*self.compression))) % (3*self.compression))

        lengthBits = len(data)
        nbPixel = self.width * self.height
        nbColors = nbPixel * 3
        mask = (2 ** self.compression) - 1
        index = 0

        if (lengthBits > (nbColors * self.compression)):
            raise Exception('Data too long.')
        if (self.image.mode not in ['RGB', 'RGBA']):
            raise Exception('Image must be RGB or RGBA.')

        encoded = self.image.copy()

        for x in range(self.height):
            for y in range(self.width):
                if index + (3 * self.compression) <= lengthBits:
                    pixel = self.image.getpixel((y, x))
                    r = pixel[0] & ~mask | dataToInput(data, index, self.compression)
                    g = pixel[1] & ~mask | dataToInput(data, index + self.compression, self.compression)
                    b = pixel[2] & ~mask | dataToInput(data, index + 2 * self.compression, self.compression)

                    if self.image.mode == 'RGBA':
                        encoded.putpixel((y, x), (r, g, b, pixel[3]))
                    else:
                        encoded.putpixel((y, x), (r, g, b))
                index += 3 * self.compression
        return encoded

    def decode(self):
        '''
        Decode data from a picture

        @param self : Steganography
        @return     : byteArray
        '''
        flag, limit, counter, buffer, data = False, 0, 0, 0, []
        for x in range(self.height):
            for y in range(self.width):
                for color in self.image.getpixel((y, x))[:3]:
                    for i in range(self.compression)[::-1]:
                        buffer += (((color) & (2 ** i)) >> i) << (8 - 1 - counter)
                        counter += 1
                        if counter == 8:
                            data.append(buffer)
                            buffer, counter = 0, 0
                            if chr(data[-1]) == '@' and flag == False:
                                flag = True
                                limit = int("".join([chr(c) for c in data[:len(data)-1]]))
                                data = []
                            if len(data) == limit:
                                return data
