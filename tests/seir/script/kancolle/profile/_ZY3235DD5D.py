""" Orlov adb module : adb profile. """
from orlov.libs.adb.profile import android_base


class _ZY3235DD5D(android_base.Android):
    SERIAL = 'ZY3235DD5D'
    TMP_PICTURE = '%s_TMP.png' % SERIAL
    IP = ''
    PORT = ''

    NAME = 'Moto G 5S Plus'
    WIDTH = '1080'
    HEIGHT = '1920'
    MINICAP_WIDTH = '720'
    MINICAP_HEIGHT = '1280'
    LOCATE = 'H'
    ROTATE = '90'


if __name__ == '__main__':
    print(eval('_ZY3235DD5D.%s' % 'TMP_PICTURE'))
