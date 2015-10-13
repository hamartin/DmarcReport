''' Module to handle exceptions for the XmlDmarcParser. '''

class XmlDmarcParserException(Exception):
    ''' Generic XmlDmarcParser exception. '''

    def __init__(self, message):
        super(XmlDmarcParserException, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return repr("XmlDmarcParserException: {0}".format(self.message))

class XmlDmarcParserFileException(XmlDmarcParserException):
    ''' XmlDmarcParser exception to handle file problems. '''

    def __init__(self, message):
        super(XmlDmarcParserFileException, self).__init__(message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return repr("XmlDmarcParserFileException: {0}".format(self.message))
