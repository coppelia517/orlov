""" Orlov Plugins : Picture Utility. """
import os
import logging

try:
    import cv2
    import numpy as np
    import pyocr
    import pyocr.builders
    from PIL import Image
except ModuleNotFoundError as e:
    print(str(e))

from orlov.exception import PictureError, OcrError

PMC_THRESHOLD = 0.96
L = logging.getLogger(__name__)


class POINT(object):
    """ PatternMatch Point Object.

    Attributes:
        x(int): Start Point X position.
        y(int): Start Point Y position.
        width(int): Target Image Width.
        height(int): Target Image Height.

    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return 'POINT()'

    def __str__(self) -> str:
        return '(X, Y) = (%s, %s), Width = %s, Height = %s' \
            % (self.x, self.y, self.width, self.height)


# pylint: disable=E1101
class Picture(object):
    """ Picture Module.
    """

    @classmethod
    def exists(cls, filename):
        """ picture file exists.

        Arguments:
            filename(str): picture filename.

        Raises:
            PictureError: file not founds.

        Returns:
            exists(bool): file exist or not.

        """
        if os.path.exists(filename):
            return True
        else:
            L.warning('%s is not exists.', filename)
            raise PictureError('%s is not exists.' % filename)

    @classmethod
    def open(cls, filename):
        """ picture file open.

        Arguments:
            filename(str): picture filename.

        Raises:
            PictureError: 1). file not founds.
                          2). file not opens.

        Returns:
            image(PIL.Image): opened PIL Image Object.

        """
        if cls.exists(filename):
            try:
                return Image.open(filename, 'r')
            except IOError as e:
                L.warning('I/O Error %s', str(e))
                raise PictureError('it is not success of loading picture %s' % filename)

    @classmethod
    def save(cls, pic, filepath, q=100, opt=True):
        """ picture file save.

        Arguments:
            pic(PIL.Image): PIL Image Object.
            filepath(str): Save Target Path.
            q(int): Save Quality.
            opt(bool): Save Optimized.

        Raises:
            PictureError: Could not find target parent directory.

        Returns:
            filepath(str): Save Target FilePath.

        """
        #cls.exists(filepath)
        if not os.path.exists(os.path.dirname(filepath)):
            raise PictureError('it is not exists parents directory. : %s' % os.path.dirname(filepath))
        pic.save(filepath, quality=q, optimize=opt)
        return filepath

    @classmethod
    def to_opencv(cls, pic):
        """ Exchanged PIL.Image to OpenCV Image.

        Arguments:
            pic(PIL.Image): PIL Image Object.

        Raises:
            PictureError: PIL.Images is None.

        Returns:
            data(numpy.ndarray): OpenCV Image Data.

        """
        if pic is None:
            raise PictureError('it is not create opencv_pic.')
        return np.asarray(pic)

    @classmethod
    def to_pil(cls, opencv_pic):
        """ Exchanged OpenCV Image to PIL.Image.

        Arguments:
            opencv_pic(numpy.ndarray): OpenCV Image Data.

        Raises:
            PictureError: Not Excnahged Picture.

        Returns:
            data(PIL.Image): PIL.Images.

        """
        try:
            return Image.fromarray(opencv_pic)
        except Exception as e:
            L.warning(str(e))
            raise PictureError('it is not exchange pic.')

    @classmethod
    def resize(cls, pic, size):
        """ Resized Picture.

        Arguments:
            pic(PIL.Image): PIL.Image.
            size(str): resize resolution. only 240P, 360P, 480P, 720P, 1080P.

        Returns:
            image(PIL.Image): opened PIL Image Object.

        """
        sz = 240
        if size == '240P':
            sz = 240
        elif size == '360P':
            sz = 360
        elif size == '480P':
            sz = 480
        elif size == '720P':
            sz = 720
        elif size == '1080P':
            sz = 1080
        else:
            return None
        #L.info("Base : %s" % str(pic.size))
        width = float((float(pic.size[0]) * sz)) / float(pic.size[1])
        res = (int(width), sz)
        #L.info("Resize : %s" % str(res))
        return pic.resize(res)

    @classmethod
    def _patternmatch(cls, reference, target, box=None):
        """ PatternMatch Base Method.

        Arguments:
            reference(str): Reference Picture FilePath.
            target(str): Target Picture FilePath.
            box(tuple): restrict target box.

        Raises:
            PictureError: 1). Could not find reference file.
                          2). Could not find target file.

        Returns:
            result(box): Pattern Match Result.
            reference(str): reference filepath.

        """
        if not os.path.exists(reference):
            raise PictureError('it is not exists reference file. : %s' % reference)
        if not os.path.exists(target):
            raise PictureError('it is not exists target file. : %s' % target)
        reference_cv = cv2.imread(reference)
        target_cv = cv2.imread(target, 0)
        return cls.__patternmatch(reference_cv, target_cv, box)

    @classmethod
    def __patternmatch(cls, reference, target, box=None, tmp=None):
        """ PatternMatch Base Method.

        Arguments:
            reference(str): Reference Picture FilePath.
            target(str): Target Picture FilePath.
            box(tuple): restrict target box.
            tmp(str): temporary folder path.

        Raises:
            PictureError: 1). Could not find reference file.
                          2). Could not find target file.

        Returns:
            result(box): Pattern Match Result.
            reference(str): reference filepath.

        """
        if len(reference.shape) == 3:
            height, width, _ = reference.shape[:3]
        else:
            height, width = reference.shape[:2]

        if box is None:
            box = POINT(0, 0, width, height)
        cv2.rectangle(reference, (box.x, box.y), (box.x + box.width, box.y + box.height), (0, 255, 0), 5)

        img_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
        img_gray = img_gray[box.y:(box.y + box.height), box.x:(box.x + box.width)]

        if tmp:
            cv2.imwrite(os.path.join(tmp, 'crop.png'), img_gray)

        template = target
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= PMC_THRESHOLD)
        result = None
        for pt in zip(*loc[::-1]):
            x = pt[0] + box.x
            y = pt[1] + box.y
            result = POINT(x, y, w, h)
            cv2.rectangle(reference, (x, y), (x + w, y + h), (0, 0, 255), 5)
        return result, reference

    @classmethod
    def search_pattern(cls, reference, target, box=None, tmp=None):
        """ PatternMatch Method.

        Arguments:
            reference(str): Reference Picture FilePath.
            target(str): Target Picture FilePath.
            box(tuple): restrict target box.
            tmp(str): temporary folder path.

        Raises:
            PictureError: 1). Could not find reference file.
                          2). Could not find target file.

        Returns:
            result(box): Pattern Match Result.
            reference(str): reference filepath.

        """
        if not os.path.exists(target):
            raise PictureError('it is not exists target file. : %s' % target)
        target_cv = cv2.imread(target, 0)
        return cls.__patternmatch(reference, target_cv, box, tmp)


class Singleton(type):
    """ Singleton meta-class
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# pylint: disable=E1101
class Ocr(object):
    """ OCR Module
    """

    TOOL = __tool_initialize()
    LANGUAGE = __language_initialize(TOOL)

    @classmethod
    def __tool_initialize(cls):
        tools = pyocr.get_available_tools()
        if not tools:
            raise OcrError('No OCR tool found.')
        return tools[0]

    @classmethod
    def __language_initialize(cls, tool):
        L.info('Will use tool "%s"', (tool.get_name()))
        langs = tool.get_available_languages()
        L.info('Available languages: %s', ', '.join(langs))
        lang = langs[0]
        L.info('Will use lang "%s"', lang)
        return lang

    @classmethod
    def __img_to_string(cls, reference, box=None, tmp=None, _lang='eng'):
        """ OCR Image to String Method.

        Arguments:
            reference(str): Reference Picture FilePath.
            box(tuple): restrict target box.
            tmp(str): temporary folder path.
            _lang(str): ocr base languages.

        Raises:
            PictureError: 1). Could not find reference file.
                          2). Could not find target file.

        Returns:
            txt(str): Search Text.
            reference(str): reference filepath.

        """
        if len(reference.shape) == 3:
            height, width, _ = reference.shape[:3]
        else:
            height, width = reference.shape[:2]

        if not box:
            box = POINT(0, 0, width, height)
        cv2.rectangle(reference, (box.x, box.y), (box.x + box.width, box.y + box.height), (255, 0, 0), 5)

        img_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
        img_gray = img_gray[box.y:(box.y + box.height), box.x:(box.x + box.width)]
        if tmp:
            cv2.imwrite(os.path.join(tmp, 'crop_ocr.png'), img_gray)
        txt = cls.TOOL.image_to_string(
            Picture.to_pil(img_gray), lang=_lang, builder=pyocr.builders.TextBuilder(tesseract_layout=6))
        return txt, reference

    @classmethod
    def img_to_string(cls, reference, box=None, tmp=None, _lang='eng'):
        """ OCR Image to String Method.

        Arguments:
            reference(str): Reference Picture FilePath.
            box(tuple): restrict target box.
            tmp(str): temporary folder path.
            _lang(str): ocr base languages.

        Raises:
            PictureError: 1). Could not find reference file.
                          2). Could not find target file.

        Returns:
            txt(str): Search Text.
            reference(str): reference filepath.

        """
        txt, _ = cls.__img_to_string(reference, box, tmp, _lang)
        L.debug('Get Text -> %s', txt)
        return txt, reference

    @classmethod
    def file_to_string(cls, filename, box=None, tmp=None, _lang='eng'):
        """ OCR File to String Method.

        Arguments:
            filename(str): Reference Picture FilePath.
            box(tuple): restrict target box.
            tmp(str): temporary folder path.
            _lang(str): ocr base languages.

        Raises:
            PictureError: 1). Could not find reference file.
                          2). Could not find target file.

        Returns:
            txt(str): Search Text.

        """
        if not os.path.exists(filename):
            raise PictureError('it is not exists reference file. : %s' % filename)
        ref_cv = cv2.imread(filename)
        txt, _ = cls.__img_to_string(ref_cv, box, tmp, _lang)
        L.info('%s -> %s', filename, txt)
        return txt
