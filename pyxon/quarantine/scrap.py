class MetaCProp(type):
    def __getattr__(prop_cls,key):
        print 'cprop getter'
        def cprop2(f1, f2):
            def cprop3(cls):
                cprops = class_cprops.get(cls,{})
                cprops[key]=(f1,f2)
                class_cprops[cls]=cprops
                return cls
            return cprop3
        return cprop2
    
class cprop:
    __metaclass__ = MetaCProp

    def __getattr__(prop_cls,key):
        print 'getter of name:',key
        def sprop2(cls):
            simple_props = class_sprops.get(cls,[])
            simple_props.append(key)
            class_sprops[cls]=simple_props
            return cls
        return sprop2



def add_type_property_orig(data, cls):
    """
    Fairly nasty reverse lookups going on in here.
    Rework to just store a reversed version of the map.
    This involves the duplication of some data, but keeps things
    much simpler - worth it!
    """
    for abstract_cls, specifiers in class_specifiers.items():
        # for most abstract clases this will return an empty list
        labels = [l for l,c in specifiers.items() if c == cls]

        # if it doesn't return an empty list then we're in business!
        if len(labels) > 0:
            label = labels[0]
            # find the property name
            prop_name = specifier_properties[abstract_cls]
            # add the specifier property to the data
            data[prop_name]=label
            return data

    # If we've made it this far then we haven't found anything
    # so just return the original data!
    return data


def concretise(cls):
    """
    Takes an instance of a subtyped class and returns a function
    that returns the appropriate concrete class based on some
    JSON data.
    """
    assert set(specifier_properties.keys())==set(class_specifiers.keys()), "You need to use @subtypes and @using as a pair!"

    if not cls in specifier_properties:
        return lambda x: cls
            
    def concretise2(d):
        prop_name = specifier_properties[cls]
        cls_label = d[prop_name]
        concrete_cls = class_specifiers[cls][cls_label]
        return concrete_cls
    
    return concretise2

