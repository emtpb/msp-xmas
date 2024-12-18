"""Custom exception classes for use with the zabertech package."""
class DeviceError(RuntimeError):
    """Exception raised when a Zaber device returns an error message.

    Device errors are identified by an error code. See the `Zaber Wiki
    <https://www.zaber.com/wiki/Manuals/Binary_Protocol_Manual#Error_Codes>`_
    for more information.

    Attributes:
        error_code: Error code as reported by the device.
    """
    def __init__(self, error_code):
        self.error_code = error_code
        super().__init__('Device Error (Code {})'.format(error_code))


class IncompleteMessageError(RuntimeError):
    """Exception raised when an incomplete message was received.

    Messages to and from Zaber devices always consist of 6 bytes.

    Attributes:
        num_bytes: Number of bytes that were received.
    """
    def __init__(self, num_bytes):
        self.num_bytes = num_bytes
        super().__init__('Incomplete message received (only {} bytes).'
                         .format(num_bytes))
