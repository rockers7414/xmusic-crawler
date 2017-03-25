from struct import pack, unpack


class MessageHeader(object):

    HEADER_LENGTH = 4
    HEADER_SEPERATOR = 29

    def __init__(self, data):
        self.data_length = unpack("=BHB", data[:self.HEADER_LENGTH])[1]

    @property
    def length(self):
        return self.data_length

    @staticmethod
    def create(data_length):
        return pack("=BHB",
                    MessageHeader.HEADER_SEPERATOR,
                    data_length,
                    MessageHeader.HEADER_SEPERATOR)
