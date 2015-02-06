# Dict of the form:
#    {cls: {name:(fn, inv_fn)}}
# cls: class that has been written with @cprop annotations
# name: class attribute name
# fn: function to turn json data into the corresponding attribute type
# inv_fn: inverse of fn
class_props = {}

# Dict of the form:
#     {AbstractClass:specifier_property}
# AbstractClass: the class that we're trying to (de)serialize
# specifier_property: the name of the json property that
#                     will indicate the concrete class name
specifier_properties = {}

# Dict of the form {AbstractClass: {label: ConcreteClass}}
# Used to retrieve the concrete implementation of an
# abstract class based on a string label.
class_specifiers = {}

# {ConcreteClass: (AbstractClass, concrete_label)}
conc_to_abstract = {}

def add_type_property(data,cls):
    """
    Given some JSON data and the class from which it was produced,
    this function returns the JSON data with any required type
    annotations added to it.
    """    
    if not cls in conc_to_abstract:
        return data

    abstract_cls, concrete_label = conc_to_abstract[cls]
    prop_name = specifier_properties[abstract_cls]
    data[prop_name] = concrete_label
    return data

class MetaProp(type):
    """
    Metaclass for the prop calculated property decorator.

    This class contains all of the decorator logic. The reason
    for using a metaclass rather than something simpler is
    to allow us to use dot notation when adding calculated
    properties.
    """
    def __getattr__(prop_cls,key):

        def prop2((f1, f2)):
            def prop3(cls):
                props = class_props.get(cls,{})
                props[key]=(f1,f2)
                class_props[cls]=props
                return cls
            return prop3
        return prop2
    
class prop:
    """
    Decorator for adding calculated properties to a class.
    A calculated property is needed when the json data can't
    be added to the class directly, for example when creating
    some other user classes from the data before adding as
    properties.

    The decorator needs to be given 2 functions as arguments:
    fun1: a function that takes JSON data and converts to some
    other data type
    fun2: the inverse of fun1, which takes some data type and
    converts it into JSON data

    Note: ideally the following will hold for any value of x
    >>> fun2(fun1(x)) == x
    
    Example:
    class Foo(object): pass
    
    @prop.y(obj(Foo))
    class Bar(object):
        def __init__(self, y):
            self.y = y
    """
    __metaclass__ = MetaProp

# Decorator annotations
def subtyped(using):
    """
    Decorator used to indicate that a class will be subtyped.
    The using= parameter is used to indicate which JSON
    property will contain the name of the subclass. A sensible
    value for thsi will be @type, but this wil all depend on
    how you have set up the rest of the system.

    Example:
    @subtyped(using='@type')
    class Foo(object): pass
    """

    # Because this is a parameterised decorator that we call, we
    # now need to create and return the decorator proper.
    def subtyped2(cls):
        specifier_properties[cls]=using
        return cls
    
    return subtyped2

def extending(super_cls, named):
    """
    This decorator is used to indicate which superclass a class
    extends. This could potentially be interpreted from the classes
    mro, but that starts to get tricky and we would still need to
    add extra info to say what the class will be named in the data.
    This label is needed because we can't necessarily rely on the
    class name and the class label in the data being the same.

    Example:
    @extending(Foo, named='Bar')
    class Baz(Foo): pass
    """
    def extending2(cls):
        conc_to_abstract[cls]=super_cls,named
        
        clsmap = class_specifiers.get(super_cls,{})
        clsmap[named]=cls
        class_specifiers[super_cls]=clsmap
        return cls
    return extending2

def conc2(data, cls):
    """
    Returns the appropriate concrete class of a subtyped class
    based on the content of some JSON data.

    If the class is not subtyped then it gets returned.
    """
    s1 = set(specifier_properties.keys())
    s2 = set(class_specifiers.keys())
    assert s1==s2, "You need to use @subtyped and @extending as a pair!:\n%s\n%s" % (str(s1), str(s2))

    if not cls in specifier_properties:
        return cls

    prop_name = specifier_properties[cls]
    cls_label = data[prop_name]
    concrete_cls = class_specifiers[cls][cls_label]
    return concrete_cls

    
