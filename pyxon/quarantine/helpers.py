def transform_map(kfun=lambda x: x, vfun=lambda x: x):
    return lambda dct: dict([(kfun(k),vfun(v)) for k,v in dct.items()])

def transform_list(item_decoder=lambda x: x):
    return lambda lst: map(item_decoder, lst)


identity = lambda x: x

def obj(cls):
    return lambda d: objectify(d, cls)
