import os
import unittest

location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if location not in os.sys.path:
    os.sys.path.append(location)



class FileComparisonTest(unittest.TestCase):
    def test__MayaMelExport__exports_same_mel(self):
        with open('test_fixtures/JTJ_0010_v009.mel') as original:
            original_export = original.read()

        with open('test_fixtures/exports/JTJ_0010_v009.mel') as original:
            new_export = original.read()

        self.assertEqual(new_export, original_export)



if __name__ == '__main__':
    unittest.main(module=__name__)