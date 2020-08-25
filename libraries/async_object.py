class AsyncObject(object):
    '''
    Inheriting this class allows you to define
    async __init__
    '''
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass
