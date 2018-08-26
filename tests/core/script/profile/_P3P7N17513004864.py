""" Orlov adb module : adb profile. """
from orlov.libs.adb.profile import android_base


class _P3P7N17513004864(android_base.Android):
    SERIAL = 'P3P7N17513004864'
    TMP_PICTURE = '%s_TMP.png' % SERIAL
    IP = ''
    PORT = ''

    NAME = 'Huawei P10 lite'
    WIDTH = '1080'
    HEIGHT = '1920'
    MINICAP_WIDTH = '720'
    MINICAP_HEIGHT = '1280'
    LOCATE = 'H'
    ROTATE = '90'


if __name__ == '__main__':
    print(eval('_P3P7N17513004864.%s' % 'TMP_PICTURE'))