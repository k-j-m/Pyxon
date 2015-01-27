class_specifiers = {}
class_properties = {}
class_arg_transforms = {}

    
def extending(super_cls, named):
    def extending2(cls):
        #print 'Adding',cls,'to specifier map'
        clsmap = class_specifiers.get(super_cls,{})
        clsmap[named]=cls
        class_specifiers[super_cls]=clsmap
        return cls
    return extending2

def subtyped(using):
    def subtyped2(cls):
        class_properties[cls]=using
        return cls
    return subtyped2

def transforming(transform_map):
    def transforming2(cls):
        class_arg_transforms[cls]=transform_map
        return cls
    return transforming2

def concretise(cls):
    assert set(class_properties.keys())==set(class_specifiers.keys()), "You need to use @subtypes and @using as a pair!"

    if not cls in class_properties:
        return lambda x: cls
            
    def concretise2(d):
        prop_name = class_properties[cls]
        cls_label = d[prop_name]
        concrete_cls = class_specifiers[cls][cls_label]
        return concrete_cls
    
    return concretise2

def decode_map(kfun=lambda x: x, vfun=lambda x: x):
    lambda dct: dict([(kfun(k),vfun(v)) for k,v in dct.items()])

def decode_list(item_decoder=lambda x: x):
    return lambda lst: map(item_decoder, lst)
                    

def classify(cls):
    concretiser = concretise(cls)
    #print 'getting funmap',cls

    #print 'funmap',funmap
    def classify2(dct):
        concrete_cls = concretiser(dct)
        funmap = class_arg_transforms.get(concrete_cls,{})
        dct2 = dct.copy()
        for k,fun in funmap.items():
            dct2[k] = fun(dct2[k])
        return concrete_cls(**dct2)
    
    return classify2

# DANGER! I've split the annotations between the abstract and concrete classes!
# This is needed because of the way that the classes are loaded by the interpreter.
# On the surface it doesn't seem so bad but there is scope for much confusion.
@subtyped(using='@type')
class AbstractChild(object): pass

@extending(AbstractChild, named='Child')
@transforming({'name': lambda n: n+'zzz', 'age': lambda a: a*100})
class Child(AbstractChild):
    def __init__(self, name, age, **kwargs):
        self.name = name
        self.age = age

    def __repr__(self):
        return "Child(name=%s, age=%i)"%(self.name, self.age)

@extending(AbstractChild, named='Child2')
class Child2(AbstractChild):
    def __init__(self, name, age, nickname, **kwargs):
        self.name = name
        self.age = age
        self.nickname = nickname

    def __repr__(self):
        return "Child2(name=%s, age=%i, nickname=%s)"%(self.name, self.age, self.nickname)
        
@transforming({'children':decode_list(classify(AbstractChild))})
class Parent(object):
    def __init__(self,name,age,children):
        self.name = name
        self.age = age
        self.children = children



parent_classifier = classify(Parent)

data = {"children":[{"name":"bruce", "age":5, "@type":"Child"},
                    {"name":"derek", "age":10, "nickname":"DEZ", "@type":"Child2"}],
        "name":"Kenny",
        "age":28}
    
p = parent_classifier(data)

print p.name
print p.age
print p.children



#list_decoder = decode_list(classify(Child))
#print list_decoder(p.children)





