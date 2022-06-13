class Namespace:
    """
    A datalass whose values can be accessed directly with the dot notation

    Usage Sample:
    ```py
    config = Namespace(foo="bar", baz=2, dex=Namespace(lmao=1))

    print(config.foo) # "bar"
    print(config.baz) # 2
    print(config.dex) # "Namespace(lmao=1)"
    print(config.null) # None
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, Namespace(**v) if isinstance(v, dict) else v)

    def __repr__(self):
        return "Namespace(%s)" % ", ".join(
            "=".join([k, repr(v)]) for k, v in self.__dict__.items()
        )

    def __getattribute__(self, __name: str):
        if __name not in self.__dict__:
            return
        return self.__dict__.get(__name)
