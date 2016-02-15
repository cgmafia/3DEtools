#
#
# 3DE4.script.name: tde wrapper
#
# 3DE4.script.version:  v0.1
#
# 3DE4.script.gui:  Main Window::ford
#
# 3DE4.script.comment: sjkghdfjksegf
#
#

#
# import sdv's python vector lib...

import tde4
from vl_sdv import *

class TDE4Wrapper(object):
    linker = {
            'cam_id': 'getCurrentCamera'
        }

    def __getattr__(self, attr):
        return getattr(tde4, self.linker['cam_id'])()



def main():
    k = TDE4Wrapper()
    # print k.getCurrentCamera()
    print k.cam_id
    # print TDE4Wrapper.__dict__


if __name__ == '__main__':
    main()