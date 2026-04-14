import unittest
from food import Food

class TestFood(unittest.TestCase):
    """ class test food"""
    
    def test_get_name(self):
        """ test_get_name """
        print('\ntest_get_name')
        food_one = Food()
        food_two = Food()

        food_two.set_name('coconut')

        self.assertEqual(food_one.get_name() , None)
        self.assertEqual(food_two.get_name() , 'coconut')

    def test_is_fat(self):
        """ test_is_fat 
        Testing 3 different levels of fat
        """
        print('test_is_fat')
        
        # Test 1 : Aliment très gras (ex: beurre)
        f1 = Food()
        f1.set_fat(50.0)
        self.assertTrue(f1.is_fat())

        # Test 2 : Aliment léger (ex: pomme)
        f2 = Food()
        f2.set_fat(0.3)
        self.assertFalse(f2.is_fat())

        # Test 3 : Pile à la limite (20.0)
        f3 = Food()
        f3.set_fat(20.0)
        self.assertFalse(f3.is_fat()) # Car le test est > 20

if __name__ == '__main__':
    unittest.main()