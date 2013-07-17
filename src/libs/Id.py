class Id(object):

    __ID = 0
    INSTANCE = None
    
    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("already instantiated")
    
    @classmethod
    def getInstance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Id()
        return cls.INSTANCE

    @classmethod
    def getId(cls):
        cls.__ID += 1
        return cls.__ID