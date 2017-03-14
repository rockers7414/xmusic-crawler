from database.providerrepo import ProviderRepo

dic_curr_providers = {}


class provider(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def _null_init(self, *args, **kwargs):
            pass

        def fetch(self):
            if '_process' not in dir(self):
                raise NotImplementedError(
                    'the provider of "' + self._provider_name + '" ' +
                    'method: _process(self, provider, tracks) is required')

            provider = self.provider_repo.get_provider(self._provider_name)
            tracks = self.provider_repo.get_unfetched_tracks_by_provider(
                provider)

            # TODO: temporarily limit fetching times
            self._process(provider, tracks[:10])

            self.provider_repo.save(provider)

        def __new__(cls, bases, *args, **kwargs):
            obj = object.__new__(cls)
            obj._provider_name = self.name
            obj.provider_repo = ProviderRepo()
            obj._init(*args, **kwargs)

            return obj

        cls._init = cls.__init__
        cls.__init__ = _null_init
        cls.__new__ = classmethod(__new__)
        cls.fetch = fetch

        dic_curr_providers[self.name] = cls

        return cls
