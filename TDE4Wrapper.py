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
        }

    def __getattr__(self, attr):
        if len(self.linker[attr]) == 1:
            return getattr(tde4, self.linker[attr][0])()
        else:
            return getattr(tde4, self.linker[attr][0])(self.cam_id)




def main():
    k = TDE4Wrapper()
    print k.frange
    print type(k.frange)


if __name__ == '__main__':
    main()