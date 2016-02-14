from test import test_support
import unittest

class SiT(unittest.TestCase):
    def test_exceptions(self):
        self.assertTrue(True)

def test_main():
    test_support.run_unittest(SiT)

if __name__ == "__main__":
    print 'TEEEEEESt'
    test_main()
