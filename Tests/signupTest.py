import unittest
import main

class MyTestCase(unittest.TestCase):
    def test_something(self):
        main.save_new_user()



if __name__ == '__main__':
    unittest.main()
