''' Module to handle exceptions for the DmarcParserFront. '''

class DmarcParserFrontException(Exception):
    ''' Generic DmarcParserFront exception. '''

    def __init__(self, message):
        super(DmarcParserFrontException, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return repr(self.message)

class DmarcParserFrontWidgetException(DmarcParserFrontException):
    ''' Exception to raise when widgets has not been initialized. '''

    def __init__(self, message):
        super(DmarcParserFrontWidgetException, self).__init__(message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return repr(self.message)
