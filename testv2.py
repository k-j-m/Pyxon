from pyxon.utils2 import objectify, unobjectify, asobj, aslist
from pyxon.decode2 import prop

class Foo(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

@prop.a(aslist(asobj(Foo)))
@prop.b(asobj(Foo))
class Bar(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
foo_data = {'a':1, 'b':2}

f = objectify(foo_data, Foo)

bar_data = {'a':[foo_data, foo_data], 'b':foo_data}
b = objectify(bar_data, Bar)
