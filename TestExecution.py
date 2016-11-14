# import TestExecution
import unittest
import RequestSaveResponce

class TestStringMethods(unittest.TestCase):

    def test_status_code(self):
        r = "200"
        self.assertEquals(r, "200")

if __name__ == '__main__':
    unittest.main()

