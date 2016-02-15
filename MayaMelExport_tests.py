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
import tde4

import MayaMelExport
reload(MayaMelExport)


class FileComparisonTest(unittest.TestCase):
    def test__MayaMelExport__exports_same_mel(self):
        oldfile = 'c:/_store/dev/3DEtools-env/3DEtools/tests/3de/exports/footage02_v001_old.mel'

        with open(oldfile, 'r') as old:
            original_export = old.read()

        newfile = MayaMelExport.main().replace('\\', '/')
        # print oldfile
        # print newfile

        with open(newfile, 'r') as new:
            new_export = new.read()

        self.assertEqual(new_export, original_export)


class MayaMelExportFuncTest(unittest.TestCase):
    def setUp(self):
        # tde4.loadProject('c:/_store/dev/3DEtools-env/3DEtools/tests/3de/footage02_v001.3de')
        tde4.loadProject('/home/DForgacs/dev/3DEtools/tests/3de/footage02_v001.3de')

        try:
            self.tde_file = tde4.getProjectPath()
        except:
            print '--> No 3De project is opne...'
            raise Exception

        self.tde_path = os.path.dirname(self.tde_file)
        self.tde_filename = os.path.basename(self.tde_file)
        self.project = self.tde_filename.split('.')[0]
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

    def test__exporter_creates_mel_file_and_export_folder(self):
        self.assertTrue(os.path.exists(self.exportfolder))
        self.assertTrue(os.path.isfile(self.mel_file))

    def test__mm_group_name_in_may_is_mm_plus_filename(self):
        # 'group -em -name "mm_footage02_v001"'
        group_name = 'mm_' + self.project
        self.assertTrue(group_name in self.melscript)

        # tde4.loadProject('c:/_store/dev/3DEtools-env/3DEtools/tests/3de/footage02_v001.3de')
        tde4.loadProject('/home/DForgacs/dev/3DEtools/tests/3de/footage02_v001.3de')
        mel_file = MayaMelExport.main()

        with open(mel_file, 'r') as f:
            melscript = f.read()

        self.assertTrue('mm_footage02_v001' in melscript)

        # tde4.loadProject('c:/_store/dev/3DEtools-env/3DEtools/tests/3de/test_name.3de')
        tde4.loadProject('/home/DForgacs/dev/3DEtools/tests/3de/test_name.3de')
        mel_file = MayaMelExport.main()

        with open(mel_file, 'r') as f:
            melscript = f.read()

        self.assertTrue('mm_test_name' in melscript)



def test_main():
    test_support.run_unittest(MayaMelExportFuncTest)
    # test_support.run_unittest(FileComparisonTest)

if __name__ == "__main__":
    test_main()
