# 3DE4.script.name: mel export tests...
#
# 3DE4.script.version:  v0.1
#
# 3DE4.script.gui:  Main Window::ford
#
# 3DE4.script.comment:  tests

import os
import unittest
import shutil
from test import test_support
import MayaMelExport
import tde4

reload(MayaMelExport)


class FileComparisonTest(unittest.TestCase):
    def test__MayaMelExport__exports_same_mel(self):
        with open('test_fixtures/JTJ_0010_v009.mel') as original:
            original_export = original.read()

        with open('test_fixtures/exports/JTJ_0010_v009.mel') as original:
            new_export = original.read()

        self.assertEqual(new_export, original_export)


class MayaMelExportFuncTest(unittest.TestCase):
    def setUp(self):
        try:
            self.tde_file = tde4.getProjectPath()
        except:
            print '--> No 3De project is opne...'
            raise Exception

        self.tde_path = os.path.dirname(self.tde_file)
        self.tde_filename = os.path.basename(self.tde_file)
        self.mel_filename = self.tde_filename.replace('3de', 'mel')
        self.mel_file = os.path.join(self.tde_path, 'exports', self.mel_filename)
        self.camera_id = tde4.getCurrentCamera()
        self.footage = tde4.getCameraPath(self.camera_id)
        self.footage_name = os.path.basename(self.footage).split('.')[0]
        self.exportfolder = os.path.join(self.tde_path, 'exports')

        if os.path.exists(self.exportfolder):
            shutil.rmtree(self.exportfolder)

        assert os.path.exists(self.exportfolder) == False, '--> Export exists'

        MayaMelExport.main()

        with open(self.mel_file, 'r') as f:
            self.melscript = f.read()

    def tearDown(self):
        if os.path.exists(self.exportfolder):
            shutil.rmtree(self.exportfolder)

        assert os.path.exists(self.exportfolder) == False, '--> Export exists'

    def test__are_running(self):
        self.assertTrue(True)

    def test__are_running_B(self):
        self.assertTrue(True)

    def test__exporter_creates_mel_file_in_export_folder(self):
        pass
    #     # exportfolder = os.path.join(self.tde_path, 'exports')

    # #     if os.path.exists(exportfolder):
    # #         shutil.rmtree(exportfolder)

    # #     MayaMelExport.main()
    # #     self.assertTrue(os.path.exists(exportfolder))
    # #     self.assertTrue(os.path.isfile(self.mel_file))

    def test__mm_group_name_in_may_is_mm_plus_footage(self):
        pass
        # group_name = 'mm_' + self.footage_name
    #     # self.assertTrue(group_name in self.melscript)







def test_main():
    test_support.run_unittest(MayaMelExportFuncTest)

if __name__ == "__main__":
    test_main()
