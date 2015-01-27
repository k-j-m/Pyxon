from .. import subtyped, extending, transforming, classify, decode_list

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
