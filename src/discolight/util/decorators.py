def singleton(klas):
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
