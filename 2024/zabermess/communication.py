"""Interface classes for ZaberTech motorized devices."""
import serial
from serial import Serial
from exceptions import DeviceError, IncompleteMessageError


def configure_device(port, baud=115200):
    """Configure new ZaberTech device to work with this package.

    To control Zabertech devices with the package it needs to be configured to
    binary mode and work with baud rate of 9600. Since new devices are setup to
    work in ascii mode and a baud rate of 115200 this function changes those
    settings.

    Args:
        port (str): Serial port device name.
        baud (int): Baud rate to use for initiale connection.
    """
    # initialse dev via serial port (rs232)
    dev = serial.Serial(
        port=port,
        baudrate=baud
    )

    # set baud rate as needed
    dev.reset_input_buffer()
    dev.write(b"/set comm.rs232.baud 9600 \r")

    # close device and reconnect with new baud rate
    dev.close()
    del dev
    dev = serial.Serial(
        port=port,
        baudrate=9600,
    )

    # set device protocol to binary
    dev.reset_input_buffer()
    dev.write(b"/set comm.protocol 1 \r")


class Device:
    """Generic Zaber device interface.

    This class provides access to commands that are supported by most Zaber
    device models. More model-specific functionality may be provided by
    subclasses.

    Attributes:
        interface (Interface): The serial interface interface to use.
        device_no (int): The number identifying this specific device.
        microstep_size (float): Microstep size in m.
    """
    def __init__(self, interface, device_no, microstep_size):
        """Initialize a Zaber device.

        Args:
            interface (Interface): The serial interface to use.
            device_no (int): The number identifying this specific device.
            microstep_size (float): Microstep size in m.
        """
        self.interface = interface
        self.device_no = device_no
        self.microstep_size = microstep_size

        # Required for speed calculations, depends on firmware version.
        # Set on demand. See Device._speed_data() for details.
        self._speed_factor = None

    def home(self):
        """Move the device to the home position."""
        self._send(1)

    def move_by(self, position):
        """Move by the requested offset.

        Args:
            position (float): Position offset in m.
        """
        self._send(21, round(position / self.microstep_size))

    def move_const(self, speed):
        """Start moving at a constant speed.

        Movement direction is indicated by the sign of the speed parameter.
        Using this command, the device will move until it either reaches a
        limit (minimum/maximum position) or another movement command (i.e.
        :func:`move_by`, :func:`move_const`, :func:`move_to` or :func:`stop`) is
        issued.

        .. warning::
            In contrast to the other movement commands, :func:`move_const` does
            *not* block program execution until movement is completed.

        Args:
            speed: Movement speed in m/s.
        """
        self._send(22, self._speed_data(speed))

    def move_to(self, position):
        """Move to the given position (absolute movement).

        Args:
            position (float): Target position in m.
        """
        self._send(20, round(position / self.microstep_size))

    def ping(self):
        """Test communication to the device.

        This uses the "Echo Data" (55) command to check whether the device is
        connected and responds correctly.

        Returns:
            bool: `True` if the device responds correctly, `False` otherwise.
        """
        data = 2342
        try:
            response_data = self._send(55, data)
        except IncompleteMessageError:
            return False
        return response_data == data

    def stop(self):
        """Stop any movement."""
        self._send(23)

    @property
    def device_id(self):
        """Zaber device ID for this device.

        .. warning::
            Not to be confused with the current device number, which
            corresponds to the position of the device in the daisy-chain, the
            device ID is a number assigned to each model by Zaber.

        Returns:
            int: Device ID.
        """
        return self._send(50)

    @property
    def firmware_version(self):
        """Current firmware version for this device.

        .. note::
            The firmware version is represented by a single integer. The last
            two digits represent the minor part of the version number, i.e. a
            value of 502 indicates version 5.02.

        Returns:
            int: Firmware version.
        """
        return self._send(51)

    @property
    def home_speed(self):
        """Movement speed used when calling :func:`home`."""
        return self._speed_data(self._send(53, 41), invert=True)

    @home_speed.setter
    def home_speed(self, home_speed):
        """Set the movement speed used when calling :func:`home`.

        Args:
            home_speed: Home speed in m/s.
        """
        self._send(41, self._speed_data(home_speed))

    @property
    def position(self):
        """Current device position.

        Returns:
            float: Current position in m.
        """
        return self._send(60) * self.microstep_size

    @property
    def target_speed(self):
        """Movement speed used when calling move functions."""
        return self._speed_data(self._send(53, 42), invert=True)

    @target_speed.setter
    def target_speed(self, target_speed):
        """Set the movement speed used when calling move functions.

        Args:
            target_speed: Home speed in m/s.
        """
        self._send(42, self._speed_data(target_speed))

    def _send(self, command_no, data=0):
        """Send a command to this device.

        This is just a shorthand for calling :func:`Interface.send` with the
        appropriate device number.

        Args:
            command_no (int): Number of the command to send.
            data (int): Data to send with the command.
        """
        return self.interface.send(self.device_no, command_no, data)

    def _speed_data(self, speed, invert=False):
        """Convert between physical speed and corresponding command data value.

        Required conversion factors vary with the device firmware version. This
        method automatically detects the correct factor.

        Args:
            speed (float): Physical speed in m/s.
            invert (bool): Invert input and output, i.e. calculate physical
                speed for given command data value, if set to `True`.

        Returns:
            Command data value representing the given speed.
        """
        if not self._speed_factor:
            # Detect speed factors by firmware version
            firmware_version = self.firmware_version
            if firmware_version >= 500 and firmware_version < 600:
                # Firmware version 5.xx --> "old" speed factors
                self._speed_factor = 9.375
            elif firmware_version >= 600 and firmware_version < 800:
                # Firmware version 6.xx --> "old" speed factors
                self._speed_factor = 1 / 1.6384
            else:
                raise RuntimeError('Unexpected firmware version detected: {}'
                                   .format(firmware_version))

        # Formula from Zaber docs: speed = data * speed_factor * num_microsteps
        if invert:
            return speed * self.microstep_size * self._speed_factor
        return round(speed / self.microstep_size / self._speed_factor)


class Interface:
    """Wrapper for :class:`serial.Serial` for I/O with zaber devices.

    This class provides common methods for reading from and writing to the
    serial port with ZaberTech devices connected. It also provides some
    commands that operate on all devices simultaneously.
    All functionality concerning only a single device is implemented in
    :class:`Device` (and possible subclasses), so that device control is
    independent of the serial port. This is relevant in daisy-chain scenarios
    where multiple devices are connected to a single port, but must be operated
    independently.

    .. note::
        Read/write functionality assumes that the device uses Zaber's "binary"
        protocol. Devices using the "ASCII" protocol are not supported. See the
        `Zaber Manuals <https://www.zaber.com/wiki/Manuals>`_ for details.
    """
    def __init__(self, port, timeout=60, baud=9600):
        """Initialize the Zaber serial interface.

        Args:
            port: Serial port device name.
            timeout: Abort read operation after this time (in seconds).
            baud (int): Baud rate to use.

        .. note::
            All arguments are directly passed to :class:`serial.Serial`.
        """
        self._port = serial.Serial(port=port, baudrate=baud, timeout=timeout)

    def broadcast(self, command_no, data=0):
        """Send a command to all connected Zaber devices.

        In contrast to :func:`send`, this returns a list of the responses
        received from the individual devices.

        Args:
            command_no (int): Number of the command to send.
            data (int): Data to send with the command.

        Returns:
            list: List of individual device responses.
        """
        responses = []
        self._write(0, command_no, data)
        while len(responses) == 0 or self._port.in_waiting > 0:
            # Read responses until timeout
            try:
                response = self._read()
            except IncompleteMessageError:
                break

            # Only return the response if it has the same command id, i.e. if
            # it actually is a response to our request.
            if response[1] == command_no:
                responses.append(response)
        return responses

    def close(self):
        """Close the serial device."""
        self._port.close()

    def detect_devices(self):
        """Detect all devices currently connected to the interface.

        Returns:
            tuple: Device numbers of all connected devices.
        """
        responses = self.broadcast(55)
        return tuple(r[0] for r in responses)

    def home_all(self):
        """Move all connected devices to the home position."""
        self.broadcast(1)

    def renumber(self):
        """Trigger device renumbering.

        All connected devices will automatically renumber according to their
        chain distance from the computer, starting with the closest device.
        """
        self.broadcast(2)

    def send(self, device_no, command_no, data=0):
        """Send a command to a specific Zaber device.

        .. note::
            This method cannot be used to send commands to all devices at the
            same time (i.e. to device number 0). Use :func:`broadcast` instead.

        Args:
            device_no (int): Number of the device to send to.
            command_no (int): Number of the command to send.
            data (int): Data to send with the command.
        """
        if device_no == 0:
            raise ValueError('Cannot send() to all devices. Use broadcast().')
        self._write(device_no, command_no, data)
        resp_device_no, resp_command_no, resp_data = self._read()
        if resp_device_no != device_no:
            raise RuntimeError('Invalid response: Device number mismatch.')
        if command_no == 53 and resp_command_no != data:
            raise RuntimeError('Invalid response: Command number mismatch '
                               '(get setting).')
        if command_no != 53 and resp_command_no != command_no:
            raise RuntimeError('Invalid response: Command number mismatch.')
        return resp_data

    def _read(self):
        """Read a 6-byte Zaber message from the serial port.

        Returns:
            tuple: Result tuple containing device_no, command_no and data.

        Raises:
            IncompleteMessageError: Raised if less than 6 bytes were received.
            DeviceError: Raised if the device responded with an error code.
        """
        byte_data = self._port.read(6)
        if len(byte_data) < 6:
            raise IncompleteMessageError(len(byte_data))
        device_no, command_no = byte_data[:2]
        data = int.from_bytes(byte_data[2:], 'little', signed=True)
        if command_no == 255:
            raise DeviceError(data)
        return device_no, command_no, data

    def _write(self, device_no, command_no, data):
        """Write a 6-byte Zaber message to the serial port.

        Args:
            device_no (int): Number of the device to send to.
            command_no (int): Number of the command to send.
            data (int): Data to send (gets converted to 4 bytes).
        """
        byte_data = data.to_bytes(4, 'little', signed=True)

        # Discard previous data in input buffer
        self._port.reset_input_buffer()
        self._port.write([device_no, command_no, *byte_data])


class TLSMA(Device):
    """Model-specific device class for T-LSMxxxA."""
    def __init__(self, interface, device_no):
        """Initialize a Zaber device.

        Args:
            interface (Interface): The serial interface to use.
            device_no (int): The number identifying this specific device.
        """
        super().__init__(interface, device_no, 47.625e-9)


class XLSMB(Device):
    """Model-specific device class for X-LSMxxxB."""
    def __init__(self, interface, device_no):
        """Initialize a Zaber device.
        
        Note:
            Axis must be set to binary mode using 
            'self._interface._port.write(b'/tools setcomm 9600 1 \r\n'.

        Args:
            interface (Interface): The serial interface to use.
            device_no (int): The number identifying this specific device.
        """
        super().__init__(interface, device_no, 0.1905e-6)


class XRSMA(Device):
    """Model-specific device class for X-RSMxxxA."""

    def __init__(self, interface, device_no):
        """Initialize a Zaber device.

        Note:
            Axis must be set to binary mode using
            'self._interface._port.write(b'/tools setcomm 9600 1 \r\n'.

            This device is a rotary stage. Therefore all positions for this
            device have to be interpreted/given in degree instead of meters.

        Args:
            interface (Interface): The serial interface to use.
            device_no (int): The number identifying this specific device.
        """
        super().__init__(interface, device_no, 0.46875e-3)

class XLSMA(Device):
    """Model-specific device class for X-LSMxxxA."""
    def __init__(self, interface, device_no):
        """Initialize a Zaber device.

            Note:
            Axis must be set to binary mode using
            'self._interface._port.write(b'/tools setcomm 9600 1 \r\n'.

        Args:
            interface (Interface): The serial interface to use.
            device_no (int): The number identifying this specific device.
        """
        super().__init__(interface, device_no, 47.625e-9)

