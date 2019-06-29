from copy import copy
from enum import Enum
from typing import no_type_check


@no_type_check
def adt(cls):
    try:
        annotations = cls.__annotations__
    except AttributeError:
        # no annotations defined
        return cls

    cls._Key = Enum('_Key',
                    [k for k in annotations.keys() if not k.startswith('__')])

    def _init(self, key, value, orig_init=cls.__init__):
        self._key = key
        self._value = value
        orig_init(self)

    cls.__init__ = _init

    def _repr(self):
        return f'{type(self)}.{self._key.name}({self._value})'

    if '__repr__' not in cls.__dict__:
        cls.__repr__ = _repr

    def _str(self):
        return f'<{type(self)}.{self._key.name}: {self._value}>'

    if '__str__' not in cls.__dict__:
        cls.__str__ = _str

    def _eq(self, other, cls=cls):
        if not isinstance(other, cls):
            return False

        return self._key == other._key and self._value == other._value

    if '__eq__' not in cls.__dict__:
        cls.__eq__ = _eq

    for caseName, key in cls._Key.__members__.items():

        def constructor(cls, value, _key=key):
            return cls(key=_key, value=value)

        if hasattr(cls, caseName):
            raise AttributeError(
                f'{cls} should not have a default value for {caseName}, as this will be a generated constructor'
            )

        setattr(cls, caseName, classmethod(constructor))

        def accessor(self, _key=key):
            if self._key != _key:
                raise AttributeError(
                    f'{self} was constructed as case {self._key.name}, so {_key.name} is not accessible'
                )

            return self._value

        if caseName.lower() not in cls.__dict__:
            setattr(cls, caseName.lower(), accessor)

    def match(self, **kwargs):
        cases = set(type(self)._Key.__members__.keys())
        predicates = {k.upper() for k in kwargs.keys()}

        assert cases == predicates, f'Pattern match on {self} ({predicates}) is over- or under-specified vs. {cases}'

        for key, callback in kwargs.items():
            if self._key == type(self)._Key[key.upper()]:
                return callback(self._value)

        raise ValueError(
            f'{self} failed pattern match against all of: {predicates}')

    if 'match' not in cls.__dict__:
        cls.match = match

    return cls