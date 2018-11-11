""" Orlov adb module : adb profile. """
from orlov.libs.adb.profile import android_base


class _8ABX0PUP1(android_base.Android):
    SERIAL = '8ABX0PUP1'
    TMP_PICTURE = '%s_TMP.png' % SERIAL
    IP = ''
    PORT = ''

    NAME = 'Pixel 3'
    WIDTH = '1080'
    HEIGHT = '2160'
    MINICAP_WIDTH = '720'
    MINICAP_HEIGHT = '1440'
    LOCATE = 'H'
    ROTATE = '90'


if __name__ == '__main__':
    print(eval('_8ABX0PUP1.%s' % 'TMP_PICTURE'))