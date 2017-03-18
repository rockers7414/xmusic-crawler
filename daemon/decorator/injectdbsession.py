from database import Session


class inject_db_session(object):

    def __init__(self, attr_name="_session"):
        self.attr_name = attr_name

    def __call__(self, cls):
        def _null_init(self, *args, **kwargs):
            pass

        def __new__(cls, bases, *args, **kwargs):
            obj = object.__new__(cls)
            setattr(obj, self.attr_name, Session())
            obj._init(*args, **kwargs)

            return obj

        cls._init = cls.__init__
        cls.__init__ = _null_init
        cls.__new__ = classmethod(__new__)

        return cls
