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
        
