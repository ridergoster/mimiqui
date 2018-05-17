import sys
from PIL import Image

class Steganography:
    def __init__(self,  url):
        self.url = url
        self.image = Image.open(self.url)
        self.width, self.height = self.image.size
        self.encoded = self.image.copy()

    @staticmethod
    def _add_padding(data, size):
        '''
        add byte padding to data depending on size

        @param data: byteArray
        @param size: int for padding size
        @return: byteArray with padding
        '''
        if (len(data) % size != 0):
            paddingSize = size - (len(data) % size)
            data += b'\x00' * paddingSize
        return data

    def encrypt(self, data):
        '''
        Hide data in the image

        @param data: data to hide in the image
        '''
        lengthData = len(data)
        print('lengthData', lengthData)

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

        for x in range(self.height):
            for y in range(self.width):
                if index + 3 <= lengthBits:
                    pixel = self.image.getpixel((y, x))
                    print('old r', pixel[0])
                    r = pixel[0] & ~1 | int(data[index])
                    print('new r', r)
                    g = pixel[1] & ~1 | int(data[index+1])
                    b = pixel[2] & ~1 | int(data[index+2])

                    if self.image.mode == 'RGBA':
                        self.encoded.putpixel((y, x), (r, g, b, pixel[3]))
                    else:
                        self.encoded.putpixel((y, x), (r, g, b))
                index += 3

        return self.encoded

    def decrypt(self):
        """
            Find a message in an image
        """
        flag, limit, count, buff, result = False, 0, 0, 0, []
        for x in range(self.height):
            for y in range(self.width):
                pixel = self.image.getpixel((y, x))[:3]
                print('pixel', pixel)
                for color in pixel:
                    buffing = color & 1
                    print('buffing', buffing)
                    buff += (buffing << (8 - 1 - count))
                    print('buff', buff)

                    print('count', count)
                    count += 1
                    if count == 8:
                        print('buff-res', buff)
                        print('buff-res', chr(buff))
                        result.append(buff)
                        buff, count = 0, 0
                        if chr(result[-1]) == "@" and flag == False:
                            flag = True
                            limit = int("".join([chr(c) for c in result[:len(result)-1]]))
                            result = []
                if len(result) == limit and flag == True:
                    return result
