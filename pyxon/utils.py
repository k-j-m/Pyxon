import pyxon.decode as pd

def unobjectify(obj):
    """
    Turns a python object (must be a class instance)
    into the corresponding JSON data.

    Example:

    >>> @sprop.a # sprop annotations are needed to tell the
    >>> @sprop.b # unobjectify function what parameter need
    >>> @sprop.c # to be written out.
    >>> class Baz(object): pass
    >>>     def __init__(self, a, b, c):
    >>>         self.a = a
    >>>         self.b = b
    >>>         self.c = c
    >>>
    >>> baz = Baz(a=1, b=2, c='three')
    >>> unobjectify(baz)
    { 'a':1, 'b':2, 'c':'three' }
    """
    cls = obj.__class__

    # Create empty data
    data = {}

    sprops,cprops = _get_registered_props(cls)
        
    # Add simple properties
    for p in sprops:
        data[p]=getattr(obj,p)

    # Add calculated data
    for p in cprops:
        f2 = cprops[p][1]
        data[p]=f2(getattr(obj,p))

    data = pd.add_type_property(data, cls)
        
    return data

def _get_registered_props(cls):
    """
    Returns all of the registered properties for a given class.
    Recursively calls up to parent classes that are inherited from.
    """
    sprops = pd.class_sprops.get(cls,{}) # [name]
    cprops = pd.class_cprops.get(cls,{}) # {name:(fn, inv_fn)}
    
    if cls in pd.conc_to_abstract: # {ConcreteClass: (AbstractClass, _)}
        parent_cls  = pd.conc_to_abstract[cls][0]
        parent_sprops, parent_cprops = _get_registered_props(parent_cls)

        sprops = list(set(sprops).union(set(parent_sprops)))
        
        cprops2 = parent_cprops.copy()
        cprops2.update(cprops)
        cprops = cprops2

    return sprops,cprops

def obj(cls):
    """
    Helper function returns a closure turning objectify into a
    single argument function. This cuts down the amount of code
    needed in class annotations by removing the need to write
    lambda functions.
    """
    return lambda d: objectify(d, cls)
    
def objectify(data, cls):
    """
    Function takes JSON data and a target class as arguments
    and returns an instance of the class created using the
    JSON data.

    I'm not sure whether it is a great idea to keep (un)objectify
    separate from the decode module, since they need to access
    some of the module-level parameters.
    """
    # Create empty class
    concrete_cls = pd.conc2(data, cls)
    obj = concrete_cls()

    sprops,cprops = _get_registered_props(cls)
    
    # Add simple properties from data
    for p in sprops:
        setattr(obj, p, data[p])

    # Add calculated properties from data
    for p in cprops:
        f1 = cprops[p][0]
        setattr(obj, p, f1(data[p]))

    return obj

def transform_map(kfun=lambda x: x, vfun=lambda x: x):
    """
    Function that takes two functions as arguments and returns
    a function that applies those functions over all of the
    keys and values in a map and returns the transformed version
    of the map.

    kfun: function applied to all keys (default identity)
    vfun: function applied to all values (default identity)

    (k -> k') -> (v -> v') -> ((k, v) -> (k', v'))
    """
    return lambda dct: dict([(kfun(k),vfun(v)) for k,v in dct.items()])

def transform_list(item_decoder=lambda x: x):
    return lambda lst: map(item_decoder, lst)

def identity(x):
    """
    Identity function is needed when performing transformations
    on maps where some operation is needed on either the keys
    or values, but not both.
    """
    return x
