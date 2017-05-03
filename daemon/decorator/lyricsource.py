
class LyricSource():

    __lyrics_source = []

    def __init__(self, source_list):
        self.__lyrics_source = source_list

    def __call__(self, func):
        def wrap_function(*args, **kwargs):
            for source in self.__lyrics_source:
                kwargs[source.__class__.__name__] = source
            return func(*args, **kwargs)
        return wrap_function
