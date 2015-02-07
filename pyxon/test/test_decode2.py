import unittest
import pyxon.decode2 as decode

class TestUtils(unittest.TestCase):

    def test_add_type_property(self):
        conc_to_abstract = {'conc':('abstract','conc_label')}
        type_props={'abstract':'$type'}
        fn = decode._add_type_property(type_props, conc_to_abstract)

        expected = {'$type':'conc_label'}
        returned = fn({},'conc')
        self.assertEquals(expected, returned)

    def test_prop_annotation(self):
        class_props = {}
        MetaProp = decode._metaprop(class_props)

        class prop(object):
            __metaclass__ = MetaProp

        @prop.x(('deserialiser','serialiser'))
        class SomeClass(object): pass

        print class_props
        self.assertTrue(SomeClass in class_props)
        self.assertTrue('x' in class_props[SomeClass])
        self.assertEquals(class_props[SomeClass]['x'][0], 'deserialiser')
        self.assertEquals(class_props[SomeClass]['x'][1], 'serialiser')
        
    def test_subtyped_annotation(self):
        specifier_properties = {}
        subtyped = decode._subtyped(specifier_properties)

        @subtyped(using='@type')
        class SomeClass(object): pass

        self.assertEquals('@type', specifier_properties[SomeClass])

    def test_extending(self):
        conc_to_abstract = {}
        class_specifiers = {}

        extending = decode._extending(conc_to_abstract, class_specifiers)

        class AbstractClass(object): pass
            
        @extending(AbstractClass, named='somename')
        class ConcreteClass(object): pass

        self.assertEquals(conc_to_abstract[ConcreteClass],(AbstractClass,'somename'))

    def test_get_class_props(self):
        class_props = {'class': {'a':('fn','inv_fn')}}

        get_class_props = decode._get_class_props(class_props)

        props = get_class_props('class')

        self.assertTrue('a' in props)
        self.assertEquals(props['a'],('fn','inv_fn'))

    def test_conc2(self):
        
        class_specifiers = {'AbstractClass': {'conc_label': 'ConcreteClass'}}
        specifier_properties = {'AbstractClass': '$type'}

        data = {'$type':'conc_label'}

        conc2 = decode._conc2(class_specifiers, specifier_properties)

        expected = 'ConcreteClass'
        returned = conc2(data,'AbstractClass')
        self.assertEquals(expected, returned)

    def test_get_parent_class(self):

        conc_to_abstract = {'ConcreteClass': ('AbstractClass','concrete_label')}

        get_parent_class = decode._get_parent_class(conc_to_abstract)

        expected = 'AbstractClass'
        returned = get_parent_class('ConcreteClass')
        self.assertEquals(expected, returned)

        expected = None
        returned = get_parent_class('not there')
        self.assertEquals(expected, returned)
