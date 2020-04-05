# generated from rosidl_generator_py/resource/_idl.py.em
# with input from custom_msgs:msg/RadarScan.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_RadarScan(type):
    """Metaclass of message 'RadarScan'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_msgs.msg.RadarScan')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__radar_scan
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__radar_scan
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__radar_scan
            cls._TYPE_SUPPORT = module.type_support_msg__msg__radar_scan
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__radar_scan

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RadarScan(metaclass=Metaclass_RadarScan):
    """Message class 'RadarScan'."""

    __slots__ = [
        '_header',
        '_point_id',
        '_x',
        '_y',
        '_z',
        '_range',
        '_velocity',
        '_doppler_bin',
        '_bearing',
        '_intensity',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'point_id': 'uint16',
        'x': 'float',
        'y': 'float',
        'z': 'float',
        'range': 'float',
        'velocity': 'float',
        'doppler_bin': 'uint16',
        'bearing': 'float',
        'intensity': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.point_id = kwargs.get('point_id', int())
        self.x = kwargs.get('x', float())
        self.y = kwargs.get('y', float())
        self.z = kwargs.get('z', float())
        self.range = kwargs.get('range', float())
        self.velocity = kwargs.get('velocity', float())
        self.doppler_bin = kwargs.get('doppler_bin', int())
        self.bearing = kwargs.get('bearing', float())
        self.intensity = kwargs.get('intensity', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.point_id != other.point_id:
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.z != other.z:
            return False
        if self.range != other.range:
            return False
        if self.velocity != other.velocity:
            return False
        if self.doppler_bin != other.doppler_bin:
            return False
        if self.bearing != other.bearing:
            return False
        if self.intensity != other.intensity:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @property
    def point_id(self):
        """Message field 'point_id'."""
        return self._point_id

    @point_id.setter
    def point_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'point_id' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'point_id' field must be an unsigned integer in [0, 65535]"
        self._point_id = value

    @property
    def x(self):
        """Message field 'x'."""
        return self._x

    @x.setter
    def x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'x' field must be of type 'float'"
        self._x = value

    @property
    def y(self):
        """Message field 'y'."""
        return self._y

    @y.setter
    def y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'y' field must be of type 'float'"
        self._y = value

    @property
    def z(self):
        """Message field 'z'."""
        return self._z

    @z.setter
    def z(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'z' field must be of type 'float'"
        self._z = value

    @property  # noqa: A003
    def range(self):
        """Message field 'range'."""
        return self._range

    @range.setter  # noqa: A003
    def range(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'range' field must be of type 'float'"
        self._range = value

    @property
    def velocity(self):
        """Message field 'velocity'."""
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'velocity' field must be of type 'float'"
        self._velocity = value

    @property
    def doppler_bin(self):
        """Message field 'doppler_bin'."""
        return self._doppler_bin

    @doppler_bin.setter
    def doppler_bin(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'doppler_bin' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'doppler_bin' field must be an unsigned integer in [0, 65535]"
        self._doppler_bin = value

    @property
    def bearing(self):
        """Message field 'bearing'."""
        return self._bearing

    @bearing.setter
    def bearing(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'bearing' field must be of type 'float'"
        self._bearing = value

    @property
    def intensity(self):
        """Message field 'intensity'."""
        return self._intensity

    @intensity.setter
    def intensity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'intensity' field must be of type 'float'"
        self._intensity = value
