from pyxon.decode import subtyped, extending, sprop, cprop
from pyxon.utils import transform_list, transform_map, identity, objectify, unobjectify, obj

@subtyped(using='@type')
class AbstractClass(object):
    pass

@extending(AbstractClass, named='SomeClass2')
@sprop.a
@sprop.b
class SomeClass2(AbstractClass):
    pass

@sprop.x
@sprop.y
@sprop.z
@cprop.xx(transform_list(lambda x: x*10),
          transform_list(lambda y: y/10))
@cprop.yy(transform_map(lambda k: int(k), lambda v: v+1),
          transform_map(lambda k: str(k), lambda v: v-1))
@cprop.zz(lambda d: objectify(d, AbstractClass),
          lambda o: unobjectify(o))
class SomeClass(object):
    pass


data = {'x':'hello_x','y':'hello_y','z':'ZZZZ',
        'xx':[10,20],'yy':{'1':100,'2':200},
        'zz':{'a':'hello','b':'world','@type':'SomeClass2'}}
#o = objectify(data, SomeClass)

# QUESTION: Can I represent data structures such as...
# Map<String,Map<String,SomeClass>> using my notation?

data2 = {'a':{'k1':{'k1A':{'a':'hello','b':'world','@type':'SomeClass2'},
                    'k1B':{'a':'HELLO','b':'WORLD','@type':'SomeClass2'}},
              'k2':{'k2A':{'a':'olleh','b':'dlrow','@type':'SomeClass2'},
                    'k2B':{'a':'OLLEH','b':'DLROW','@type':'SomeClass2'}}}}

@cprop.a(transform_map(identity, transform_map(identity, obj(AbstractClass))),
         transform_map(identity, transform_map(identity, unobjectify)))
class FunnyHolder(object): pass

print 'buuuh'
#fh = objectify(data2, FunnyHolder)
print 'bzaaat'

@sprop.a
@sprop.b
@subtyped(using='@type')
class Abstract(object):
    pass

@sprop.x
@sprop.y
@extending(Abstract, named='Concrete')
class Concrete(Abstract):
    pass

data2 = {'a':1, 'b':2, 'x':3, 'y':4, '@type':'Concrete'}
conc_obj = objectify(data2, Concrete)
print conc_obj
