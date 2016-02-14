# 3DE4.script.name: mel export tests...
#
# 3DE4.script.version:  v0.1
#
# 3DE4.script.gui:  Main Window::ford
#
# 3DE4.script.comment:  tests

import os
import unittest
from test import test_support
import MayaMelExport


# location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# if location not in os.sys.path:
#     os.sys.path.append(location)



class FileComparisonTest(unittest.TestCase):
    def test__MayaMelExport__exports_same_mel(self):
        with open('test_fixtures/JTJ_0010_v009.mel') as original:
            original_export = original.read()

        with open('test_fixtures/exports/JTJ_0010_v009.mel') as original:
            new_export = original.read()

        self.assertEqual(new_export, original_export)


class MayaMelExportFuncTest(unittest.TestCase):
	def test__are_running(self):
		self.assertTrue(True)

	def test__exporter_creates_mel_file_in_export_folder(self):
		MayaMelExport.main()


def test_main():
    test_support.run_unittest(MayaMelExportFuncTest)

if __name__ == "__main__":
    test_main()
