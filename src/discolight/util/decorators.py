"""Some useful decorators."""


# yapf: disable
# We have to do this becuase yapf doesn't play nice with pep257.
def singleton(klas):
    """Make a class a singleton."""
    class Singleton:

        class __Singleton:

            def __init__(self):

                self.__name__ = klas.__name__
                self.klas = klas()

            def __getattr__(self, name):

                return getattr(self.klas, name)

        instance = None

        def __init__(self):
            if not Singleton.instance:
                Singleton.instance = Singleton.__Singleton()

        def __getattr__(self, name):

            return getattr(self.instance, name)

    Singleton.__name__ = klas.__name__

    return Singleton
# yapf: enable
