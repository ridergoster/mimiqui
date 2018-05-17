# CBC ECB cryptography
import argparse
import string
from cypher import Cypher
from steganography import Steganography

def handleArgs():
    parser = argparse.ArgumentParser(description='mimiqui create image with secret message')
    parser.add_argument('-if', '--image-file',
                        dest='imageInput',
                        default='index.png',
                        help='input image file path (default: index.png)')
    parser.add_argument('-io', '--image-output',
                        dest='imageOutput',
                        default='output.png',
                        help='output image file path (default: output.png)')

    parser.add_argument('-df', '--data-file',
                        dest='dataInput',
                        default='index.txt',
                        help='input data file path (default: index.txt)')
    parser.add_argument('-do', '--data-output',
                        dest='dataOutput',
                        default='output.txt',
                        help='output data file path (default: output.txt)')

    parser.add_argument('-k', '--key',
                        dest='key',
                        help='key to unlock file')

    parser.add_argument('-s', '--size',
                        dest='size',
                        type=int,
                        default=16,
                        help='size for each block in cypher (default: 16)')

    parser.add_argument('-e', '--encrypt',
                        dest='decrypt',
                        action='store_false',
                        help='select encrypt mode (default: false)')

    parser.add_argument('-d', '--decrypt',
                        dest='decrypt',
                        action='store_true',
                        help='select decrypt mode (default: true)')

    parser.set_defaults(decrypt=False)
    parser.set_defaults(key='maison')
    return parser.parse_args()

def main():
    args = handleArgs()
    cypher = Cypher(args.key, args.size)
    steganography = Steganography(args.imageInput)
    print('cypher', cypher)

    with open(args.dataInput, 'rb')  as readFile: # we read as byte with 'rb'
        data = [i for i in readFile.read()]
        if (args.decrypt == True):
            encoded = steganography.decrypt()
            print('encoded', encoded)
            result = cypher.decrypt(encoded)
            print('result', result)
        else:
            result = cypher.encrypt(data)
            print('result', result)
            encoded = steganography.encrypt(result)
            encoded.save(args.imageOutput, quality=100)

    with open(args.dataOutput, 'wb') as writeFile:
        byteArray = bytearray(result)
        writeFile.write(byteArray)

    print('done !')
main()
