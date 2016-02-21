"""
wrapper class for 3DEqualizer tde4 API.

github/danielforgacs
"""

import tde4
from vl_sdv import *

class TDE4Wrapper(object):
    linker = {
            'cam_id': ('getCurrentCamera',),
            'frange': ('getCameraSequenceAttr', 'cam_id'),
            'res_x': ('getCameraImageWidth', 'cam_id'),
            'res_y': ('getCameraImageHeight', 'cam_id'),
            'path': ('getProjectPath',),
            'footage': ('getCameraPath', 'cam_id'),
            'focal': ('getCameraFocalLength', 'cam_id', 'frame'),
            'lens_id': ('getCameraLens', 'cam_id'),
            'filmback_h': ('getLensFBackWidth', 'lens_id'),
            'filmback_v': ('getLensFBackHeight', 'lens_id'),
        }

    def __getattr__(self, attr):
        if len(self.linker[attr]) == 1:
            return getattr(tde4, self.linker[attr][0])()

        elif len(self.linker[attr]) == 2:
            parm = eval('self.' + self.linker[attr][1])
            return getattr(tde4, self.linker[attr][0])(parm)

        elif len(self.linker[attr]) == 3:
            parm = eval('self.' + self.linker[attr][1])
            return getattr(tde4, self.linker[attr][0])(parm, 1)




def main():
    k = TDE4Wrapper()
    print (k.frange)
    print (type(k.frange))


if __name__ == '__main__':
    main()