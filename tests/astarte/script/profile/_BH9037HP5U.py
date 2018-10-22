""" Orlov adb module : adb profile. """
from orlov.libs.adb.profile import android_base


class _BH9037HP5U(android_base.Android):
    SERIAL = 'BH9037HP5U'
    TMP_PICTURE = '%s_TMP.png' % SERIAL
    IP = ''
    PORT = ''

    NAME = 'Xperia X Compact'
    WIDTH = '720'
    HEIGHT = '1280'
    MINICAP_WIDTH = '720'
    MINICAP_HEIGHT = '1280'
    LOCATE = 'H'
    ROTATE = '90'


if __name__ == '__main__':
    print(eval('_BH9037HP5U.%s' % 'TMP_PICTURE'))
