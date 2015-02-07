import unittest
import pyxon.utils2 as utils

class TestUtils(unittest.TestCase):

    def test_aslist(self):
        """
        Make sure that our list transform function works.
        """
        f1 = lambda x: x*2
        f2 = lambda x: x/2
    
        lst_f1, lst_f2 = utils.aslist((f1,f2))

        start_list = [1,2,3]

        expected = [2,4,6]
        returned = lst_f1(start_list)

        self.assertEquals(expected, returned)
        self.assertEquals(start_list, lst_f2(lst_f1(start_list)))
        
    def test_asmap(self):
        """
        Make sure that out map transform function works.
        """
        f1 = lambda x: x*2
        f2 = lambda x: x/2

        map_f1, map_f2 = utils.asmap((f1,f2),(f1,f2))
        
        start_map = {1:2, 2:3}
        expected = {2:4, 4:6}
        returned = map_f1(start_map)

        self.assertEquals(expected, returned)
        self.assertEquals(start_map, map_f2(map_f1(start_map)))
        

    def test_get_init_args(self):
        class ParentClass(object):
            def __init__(self, b, c): pass

        class ChildClass(ParentClass):
            def __init__(self, a, z): pass

        class ChildClass2(ParentClass):
            def __init__(self, a, z, **kwargs): pass
                
        class_props = {ChildClass: {'a':('fn1','inv_fn1')},
                       ChildClass2: {'a':('fn1','inv_fn1')},
                       ParentClass: {'b':('fn2','inv_fn2')}}

        conc_to_abstract = {ChildClass:ParentClass,
                            ChildClass2:ParentClass}
        
        get_parent_class = lambda cls: conc_to_abstract.get(cls,None)
        get_class_props = lambda cls: class_props[cls]

        get_init_args = utils._get_init_args(get_parent_class, get_class_props)

        expected = (['b','c'],{'b':('fn2','inv_fn2')})
        returned = get_init_args(ParentClass)
        self.assertEquals(expected, returned)

        expected = (['a','z','b','c'],{'a':('fn1','inv_fn1'),'b':('fn2','inv_fn2')})
        returned = get_init_args(ChildClass)
        self.assertEquals(expected, returned)



        returned = get_init_args(ChildClass)
        self.assertEquals(expected, returned)

    def test_init_args_base(self):
        """
        Make sure that we can get a full set of init args for a base class.
        """

        class BaseClass(object):
            def __init__(self, a, b, c): pass

        expected = (['a','b','c'], {})
        returned = utils.get_init_args(BaseClass)
        self.assertEquals(expected, returned)

    def test_objectify(self):

        class SomeClass(object):
            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c

        data = {'a':1, 'b':2, 'c':3}

        sc = utils.objectify(data,SomeClass)

        self.assertEquals(sc.a,1)
        self.assertEquals(sc.b,2)
        self.assertEquals(sc.c,3)

    def test_unobjectify(self):
        class SomeClass(object):
            def __init__(self, a,b,c):
                self.a = a
                self.b = b
                self.c = c

        data = {'a':1, 'b':2, 'c':3}

        sc = SomeClass(**data)

        returned = utils.unobjectify(sc)

        self.assertEquals(data,returned)
    
