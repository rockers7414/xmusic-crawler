from database import Session


class unique(object):
    """The utility of unique constraint decorator for entity class"""

    def __init__(self, hashfunc, queryfunc):
        """Constructor

        :hashfunc: define the function return unique value for hash with the given parameters from constructor
        :queryfunc: define the function return result from database with given query and parameters from constructor

        """

        self.hashfunc = hashfunc
        self.queryfunc = queryfunc

    def __call__(self, cls):
        def _null_init(self, *args, **kwargs):
            pass

        def __new__(cls, bases, *args, **kwargs):
            if not args and not kwargs:
                return object.__new__(cls)

            session = Session()

            def _unique(session, cls, hashfunc, queryfunc, constructor, args, kwargs):
                cache = getattr(session, '_unique_cache', None)
                if cache is None:
                    session._unique_cache = cache = {}

                key = (cls, hashfunc(*args, **kwargs))

                if key not in cache:
                    with session.no_autoflush:
                        q = session.query(cls)
                        obj = queryfunc(q, *args, **kwargs).one_or_none()

                        if not obj:
                            obj = constructor(*args, **kwargs)
                            session.add(obj)

                    cache[key] = obj

                return cache[key]

            def constructor(*args, **kwargs):
                obj = object.__new__(cls)
                obj._init(*args, **kwargs)
                return obj

            return _unique(
                session,
                cls,
                self.hashfunc,
                self.queryfunc,
                constructor,
                args,
                kwargs
            )

        cls._init = cls.__init__
        cls.__init__ = _null_init
        cls.__new__ = classmethod(__new__)

        return cls

