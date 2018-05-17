import sys

class Cypher:
    '''
        Cypher
        - encrypt or decrypt data
        - Encryption enable with a XOR method using a string key
        - CBC mode enable
    '''

    def __init__(self, key, size):
        '''
        Constructor for Cypher class

        @param self : Cypher
        @param key  : String
        @param size : Number
        @return     : None
        '''
        self.size = size
        self.key = bytearray()
        self.key.extend(key.encode('utf-8')) # key must be byteArray
        self.key = Cypher._add_padding(self.key, self.size) # we add padding to the key so it match data size

    def cypher(self, data):
        '''
        Encrypt data with a key using XOR

        @param self : Cypher
        @param data : byteArray
        @return     : byteArray
        '''
        return [ (p ^ l) for (p, l) in zip(data, self.key) ]

    @staticmethod
    def _remove_padding(data):
        '''
        Remove byte padding to data

        @param data : byteArray
        @return     : byteArray
        '''
        pad_len = 0
        for byte in data[::-1]:
            if byte == 0:
                pad_len += 1
            else:
                break
        return data[:-pad_len]

    @staticmethod
    def _add_padding(data, size):
        '''
        Add byte padding to data depending on size

        @param data : byteArray
        @param size : Number
        @return     : byteArray
        '''
        if (len(data) % size != 0):
            paddingSize = size - (len(data) % size)
            data += b'\x00' * paddingSize
        return data

    def encrypt(self, data):
        '''
        Encrypt data with CBC mode

        @param self : Cypher
        @param data : byteArray
        @return     : byteArray
        '''
        data = Cypher._add_padding(data, self.size)
        result, i, IV = [], 0, range(self.size)
        while i <= len(data):
            segment = data[i: i + self.size]
            cypherData = [ (p ^ l) for (p, l) in zip(segment, IV) ]
            IV = self.cypher(cypherData)
            result = result + IV
            i += self.size
        return result

    def decrypt(self, data):
        '''
        Decrypt data with CBC mode

        @param self : Cypher
        @param data : byteArray
        @return     : byteArray
        '''
        result, i, IV = [], 0, range(self.size)
        while i <= len(data):
            segment = data[i: i + self.size]
            cypherData = self.cypher(segment)
            result += [ (p ^ l) for (p, l) in zip(cypherData, IV) ]
            IV = segment
            i += self.size
        return Cypher._remove_padding(result)
