from database import Session

class inject_db_session(object):
    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *args, **kwargs):
        def _null_init(self, *args, **kwargs):
            pass

        def __new__(cls, bases, *args, **kwargs):
            obj = object.__new__(cls)
            obj._session = Session()
            obj._init(*args, **kwargs)

            return obj

        self._cls._init = self._cls.__init__
        self._cls.__init__ = _null_init
        self._cls.__new__ = classmethod(__new__)

        return self._cls(*args, **kwargs)
