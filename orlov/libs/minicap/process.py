"""  Orlov Plugins : Minicap Process Utility. """
import os
import io
import sys
import time
import logging
import threading
from queue import Queue

import cv2
from PIL import Image
import numpy as np

from orlov.exception import *
from orlov.cmd import run

PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not PATH in sys.path:
    sys.path.insert(0, PATH)

MAX_SIZE = 5
L = logging.getLogger(__name__)


class PatternMatchObject(object):
    """ Pattern Match Object.

    Attributes:
        target(str): target image filepath.
        box(tuple): target position(x, y)

    """

    def __init__(self, _target, _box):
        self.target = _target
        self.box = _box

    def __repr__(self):
        return 'PatternMatchObject()'

    def __str__(self):
        return 'Target, Box : %s, %s' % (os.path.basename(self.target), self.box)


# pylint: disable=E1101
class MinicapProc(object):
    """ Minicap Process

    Attributes:
        stream(MinicapStream): Minicap Stream Object.
        service(MinicapService): Minicap Service Object.
        debug(bool): Debug flag.

    """

    def __init__(self, _stream, _service, debug=False):
        self.stream = _stream
        self.service = _service
        self.output = Queue()
        self._loop_flag = True
        self._debug = debug

        self._pattern_match = None
        self.patternmatch_result = Queue()

        self._ocr = None
        self.ocr_result = Queue()

        self._capture = None
        self.capture_result = Queue()

        self.counter = 0

    def start(self, _adb, _pic, _ocr=None):
        """ Minicap Process Start.
        
        """
        self.adb = _adb
        self.pic = _pic
        self.ocr = _ocr
        self.service.start(self.adb)
        time.sleep(2)
        self.adb.forward("tcp:%s localabstract:minicap" % str(self.stream.get_port()))
        self.stream.start()
        time.sleep(1)
        self.loop = threading.Thread(target=self.main_loop).start()

    def finish(self):
        self._loop_flag = False
        time.sleep(2)
        self.stream.finish()
        time.sleep(2)
        if self.service != None:
            self.service.stop()

    def get_d(self):
        return self.output.qsize()

    def get_frame(self):
        return self.output.get()

    def __save(self, filename, data):
        with open(filename, "wb") as f:
            f.write(data)
            f.flush()

    def __save_cv(self, filename, img_cv):
        return cv2.imwrite(filename, img_cv)

    def __save_evidence(self, number, data):
        number = int(number)
        if number < 10: number = "0000%s" % str(number)
        elif number < 100: number = "000%s" % str(number)
        elif number < 1000: number = "00%s" % str(number)
        elif number < 10000: number = "0%s" % str(number)
        else: number = str(number)
        self.__save_cv(os.path.join(TMP_EVIDENCE_DIR, "image_%s.png" % number), data)

    def search_pattern(self, target, box=None, _timeout=5):
        self._pattern_match = PatternMatchObject(target, box)
        result = self.patternmatch_result.get(timeout=_timeout)
        self._pattern_match = None
        return result

    def search_ocr(self, box=None, _timeout=5):
        self._ocr = PatternMatchObject("dummy", box)
        result = self.ocr_result.get(timeout=_timeout)
        self._ocr = None
        return result

    def capture_image(self, filename, _timeout=5):
        self._capture = filename
        self.capture_result.get(timeout=_timeout)
        abspath = os.path.join(TMP_DIR, filename)
        self._capture = None
        return abspath

    def create_video(self, src, dst, filename="output.mp4"):
        output = os.path.join(dst, filename)
        if os.path.exists(output):
            os.remove(output)
        cmd = r'%s -r 3 -i %s -an -vcodec libx264 -pix_fmt yuv420p %s' % (FFMPEG_BIN, os.path.join(
            src, "image_%05d.png"), os.path.join(dst, filename))
        L.debug(cmd)
        return run(cmd)

    def main_loop(self):
        if self._debug:
            cv2.namedWindow("debug")
        while self._loop_flag:
            data = self.stream.picture.get()
            save_flag = False

            image_pil = Image.open(io.BytesIO(data))
            image_cv = cv2.cvtColor(np.asarray(image_pil), cv2.COLOR_RGB2BGR)

            if self._capture != None:
                outputfile = os.path.join(TMP_DIR, self._capture)
                result = self.__save_cv(outputfile, image_cv)
                self.capture_result.put(result)

            if self._pattern_match != None:
                if self.pic != None:
                    result, image_cv = self.pic.search_pattern(image_cv, self._pattern_match.target,
                                                               self._pattern_match.box, TMP_DIR)
                    self.patternmatch_result.put(result)
                    save_flag = True

            if self._ocr != None:
                if self.ocr != None:
                    result, image_cv = self.ocr.img_to_string(image_cv, self._ocr.box, TMP_DIR)
                    self.ocr_result.put(result)
                    save_flag = True

            if self.counter % 5 == 0 or save_flag:
                self.__save_evidence(self.counter / 5, image_cv)

            if self._debug:
                if self.adb is None:
                    resize_image_cv = cv2.resize(image_cv, (640, 360))
                else:
                    w = int(int(self.adb.get().MINICAP_WIDTH) / 2)
                    h = int(int(self.adb.get().MINICAP_HEIGHT) / 2)
                    if int(self.adb.get().ROTATE) == 0:
                        resize_image_cv = cv2.resize(image_cv, (h, w))
                    else:
                        resize_image_cv = cv2.resize(image_cv, (w, h))
                cv2.imshow('debug', resize_image_cv)
                key = cv2.waitKey(5)
                if key == 27:
                    break
            self.counter += 1
            """
            ret, jpeg = cv2.imencode('.jpg', image_cv)
            self.output.put(jpeg.tobytes())
            if self.get_d() > MAX_SIZE: self.output.get()
            """
        if self._debug:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    service = library.register(library.register(), LIB_DIR)
    L.info(service)
    adb = service["stve.android"].get("BH9037HP5U")

    stream = service["aliez.stve.minicap"].get_stream("localhost", 1919)
    proc = service["aliez.stve.minicap"].get_process(LOG_DIR)

    main = MinicapProc(stream, proc, debug=True)
    main.start(adb)
    time.sleep(20)
    main.finish()
    main.create_video(TMP_EVIDENCE_DIR, TMP_VIDEO_DIR)