import inspect
import pyxon.decode2 as pd

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

    
    #([prop_name] {prop_name: (fn, inv_fn)}
    prop_names, prop_funs = _get_init_args(cls)

    # Create empty data
    data = {}
    for prop_name in prop_names:
        if prop_name in prop_funs:
            serialiser = props_funs[prop_name][1]
            data[prop_name]=serialiser(getattr(obj,prop_name))
        else:
            data[prop_name]=getattr(obj,prop_name)
            
    return data

def _get_registered_props(cls):
    """
    Returns all of the registered properties for a given class.
    Recursively calls up to parent classes that are inherited from.

    {propname: (fn, inv_fn)}
    """
    props = pd.class_props.get(cls,{}) # [name]

    parent_cls = _get_parent_class(cls) # parent class OR None
    if parent_cls is not None: 
        parent_props = _get_registered_props(parent_cls)
        props2 = parent_cprops.copy()
        props2.update(cprops)
        props = cprops2

    return props

def _get_parent_class(cls):
    """
    Returns the parent inherited class if possible, otherwise
    returns None.
    """
    if cls in pd.conc_to_abstract:
        return pd.conc_to_abstract[cls][0]
    else:
        return None

def _get_init_args(cls):
    """
    Returns a tuple of the form
    ([argname], {argname:(deserialiser, serialiser)})

    The first item is just a list of all arguments listed in
    the class __init__ method, along with all arguments for any
    inherited classes.

    The second item is a dict giving the functions needed to deserialise
    and serialise an argument when it does not correspond to a native
    JSON data type.
    """

    # Do we inherit?
    parent_cls = _get_parent_class(cls)
    if parent_cls is not None:
        args, arg_funs = _get_init_args(parent_cls)
    else:
        args, arg_funs = [], {}

    myargs = inspect.getargspec(cls.__init__).args[1:]
    # Make sure there are no duplicate arguments: this is forbidden
    assert set(myargs) & set(args) == set()

    
    # The parent args aren't needed during deserialisation (**kwargs
    # in the __init__ mean we can just pass leftovers on up the inheritance
    # tree. They ARE however needed during serialisation.
    
    myprops = _get_class_props(cls)
    arg_funs.update(myprops)

    myargs.extend(args)

    return (myargs, arg_funs)
        
    
    

def _get_class_props(cls):
    """
    Returns a dict containing the deserialise/serialise functions for
    all class properties that need transformations applied to them.

    {propname: (deserialiser, serialiser)}

    We give this a protective copy because it would be a BAD thing for
    this to get changed in the field.
    """
    return pd.class_props.get(cls,{}).copy()
    
def asobj(cls):
    """
    Returns a tuple pair of functions. The first for deserialising,
    the second for serialising.
    """
    return (lambda d: objectify(d, cls), unobjectify)

def aslist((f,inv_f)):
    """
    Returns a tuple pair of functions that are used to deserialise/serialise
    a list containing non-native json types.
    """
    def deserialise(lst):
        return map(f, lst)

    def serialise(lst):
        return map(inv_f, lst)

    return (deserialise, serialise)

def asmap((kf, inv_kf), (vf, inv_vf)):
    """
    Returns a tuple pair of functions that are used to deserialise/serialise
    a map containing non-native json datatypes (or non-string keys).
    """
    def deserialise(some_dict):
        return dict([(kf(k), vf(v)) for k,v in some_dict.iteritems()])

    def serialise(some_dict):
        return dict([(inv_kf(k), inv_vf(v)) for k,v in some_dict.iteritems()])

    return (deserialise, serialise)

def objectify(data, cls):
    """
    Function takes JSON data and a target class as arguments
    and returns an instance of the class created using the
    JSON data.

    I'm not sure whether it is a great idea to keep (un)objectify
    separate from the decode module, since they need to access
    some of the module-level parameters.
    """
    # protective copy - we will be mutating this
    data2 = data.copy()
    
    # Create empty class
    concrete_cls = pd.conc2(data, cls)

    prop_names, prop_funs = _get_init_args(cls)

    # TODO: knock out loop and replace with set comparison
    for prop_name in prop_names:
        assert prop_name in data

    # Transform the data that needs transformed
    for prop_name, (deserialiser, _) in prop_funs.iteritems():
        data2[prop_name]=deserialiser(data2[prop_name])
        
    # create our object from the concrete class
    # and pass in the data as kwargs
    print concrete_cls
    obj = concrete_cls(**data2)
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
