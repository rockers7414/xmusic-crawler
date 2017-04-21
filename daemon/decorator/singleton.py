import functools


class singleton(object):

    def __call__(self, cls):

        @functools.wraps(cls.__new__)
        def get_instance(cls, *args, **kwargs):
            it = cls.__dict__.get('__it__')
            if it is not None:
                return it

            cls.__it__ = it = cls.__new_instance__(cls)
            it.__new_init__(*args, **kwargs)
            return it

        cls.__new_instance__ = cls.__new__
        cls.__new__ = get_instance
        cls.__new_init__ = cls.__init__
        cls.__init__ = object.__init__

        return cls
