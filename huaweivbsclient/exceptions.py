"""Exceptions for the HuaWeiVBSClient"""


class ClientException(Exception):
    """The base exception class for all exceptions this library raises."""
    message = 'Unknown Error'

    def __init__(self, message='Unknown Error'):
        self.message = message

    def __str__(self):
        return self.message


class BadRequest(ClientException):
    """HTTP 400 - Bad request: you sent some malformed data."""
    def __init__(self, *args):
        message = 'HTTP 400 Bad request. Please verify command arguments of '
        for i in args:
            message += '"' + i + '", '
        message = message[:-2] + '.'
        self.message = message


class InvalidFormat(ClientException):
    """Not a valid format."""
    def __init__(self, msg):
        self.message = 'Invalid format. ' + msg


class ServiceError(ClientException):
    """Service has an error."""
    def __init__(self, code, msg):
        self.message = 'Service error ' + code + ': ' + msg


class ResponseFormatError(ClientException):
    """Response is not a valid format."""
    def __init__(self, msg):
        self.message = 'Response format error. Response: ' + msg
