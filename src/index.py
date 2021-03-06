import argparse

from Cypher import Cypher
from Steganography import Steganography

'''
    Mimiqui
    - Encrypt data from a file then encode it inside a picture
    - Decode data from a picture then decrypt it in a file
    - CBC mode encryption
    - LSB encoding in the picture
'''

def handleArgs():
    '''
    Handle argument from main call

    @return : None
    '''
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

    parser.add_argument('-c', '--compression',
                        dest='compression',
                        type=int,
                        default=4,
                        help='compression value [1-8] (default: 4)')

    parser.add_argument('-e', '--encrypt',
                        dest='decrypt',
                        action='store_false',
                        help='select encrypt mode (default: true)')

    parser.add_argument('-d', '--decrypt',
                        dest='decrypt',
                        action='store_true',
                        help='select decrypt mode (default: false)')

    parser.set_defaults(decrypt=False)
    parser.set_defaults(key='maison')
    return parser.parse_args()

def main():
    '''
    Main function to handle the script

    @return : None
    '''
    args = handleArgs()
    cypher = Cypher(args.key, args.size)  # create the Cypher obj from our Cypher class
    steganography = Steganography(args.imageInput, args.compression)  # create the Steganography obj from our Steganography class

    if args.decrypt:  # if decrypt option is used
        encoded = steganography.decode()  # decode the message hidden into image
        result = cypher.decrypt(encoded)  # decrypt the message found

        # Write the decrypted message in the output file
        with open(args.dataOutput, 'wb') as writeFile:
            byteArray = bytearray(result)
            writeFile.write(byteArray)
    else:  # if encrypt option is used
        # Read bytes of input file
        with open(args.dataInput, 'rb') as readFile:
            data = [i for i in readFile.read()]
            encoded = cypher.encrypt(data)  # encrypt the message
            image = steganography.encode(encoded)  # encode the message into image

            '''
            Copy the encoded image to a new file in best quality
            to ensure that image's bits are not corrupted by compression
            '''
            image.save(args.imageOutput, quality=100)

if __name__ == "__main__":
    main()
