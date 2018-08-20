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
import fasteners

PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not PATH in sys.path:
    sys.path.insert(0, PATH)

MAX_SIZE = 5
L = logging.getLogger(__name__)


class SearchObject(object):
    """ Search Object.

    Attributes:
        function(str): target get function.
        target(str): target image filepath.
        box(tuple): target position(x, y)

    """

    def __init__(self, _function, _target, _box):
        self.func = _function
        self.target = _target
        self.box = _box

    def __repr__(self):
        return 'SearchObject()'

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
        self.module = {}
        self.module['stream'] = _stream
        self.module['service'] = _service

        self.space = {}

        self.output = Queue()
        self._loop_flag = True
        self._debug = debug

        self._search = None
        self.search_result = Queue()
        self.counter = 0
        self.lock = fasteners.InterProcessLock('.lockfile')

    def start(self, _adb, _workspace, _picture, _ocr=None):
        """ Minicap Process Start.

        Arguments:
            _adb(Android): android adaptor object.
            _workspace(Workspace): workspace adaptor object.
                - log : workspace.log
                - tmp : workspace.tmp
                - evidence : workspace.tmp.evidence
                - reference : workspace.tmp.reference
            _picture(Picture): picture module adaptor object.
            _ocr(Ocr): ocr module adaptor object.

        """
        self.module['adb'] = _adb
        self.module['workspace'] = _workspace
        self.module['picture'] = _picture
        self.module['ocr'] = _ocr

        self.space['tmp'] = self.module['workspace'].mkdir('tmp')
        self.space['log'] = self.module['workspace'].mkdir('log')
        self.space['tmp.evidence'] = self.module['workspace'].mkdir('tmp\\evidence')
        self.space['tmp.reference'] = self.module['workspace'].mkdir('tmp\\reference')

        self.module['service'].start(self.module['adb'], self.space['log'])
        time.sleep(2)
        self.module['adb'].forward('tcp:%s localabstract:minicap' % str(self.module['stream'].get_port()))
        self.module['stream'].start()
        time.sleep(1)
        self.module['loop'] = threading.Thread(target=self.main_loop).start()

    def finish(self):
        """ Minicap Process Finish.
        """
        self._loop_flag = False
        time.sleep(2)
        self.module['stream'].finish()
        time.sleep(2)
        if 'service' in self.module and self.module['service'] != None:
            self.module['service'].stop()

    def get_d(self) -> int:
        """ Get output queue size.
        """
        return self.output.qsize()

    def get_frame(self) -> object:
        """ Get frame image in output.
        """
        return self.output.get()

    def __save(self, filename, data):
        """ Save framedata in files.

        Arguments:
            filename(str): saved filename.
            data(object): save framedata.
        
        """
        with open(filename, 'wb') as f:
            f.write(data)
            f.flush()

    def __save_cv(self, filename, img_cv):
        """ Save framedata in files. (opencv)

        Arguments:
            filename(str): saved filename.
            img_cv(numpy.ndarray): framedata(opencv).
        
        Returns:
            filepath(str): filepath

        """
        return cv2.imwrite(filename, img_cv)

    def __save_evidence(self, number, data):
        """ Save Evidence Data.

        Arguments:
            number(int): counter number.
            data(object): save framedata.

        """
        zpnum = '{:0:08d}'.format(number)
        if 'tmp.evidence' in self.space:
            self.__save_cv(os.path.join(self.space['tmp.evidence'], "image_%s.png" % str(zpnum)), data)

    def __search(self, func, target, box=None, _timeout=5):
        """ Search Object.
        """
        self._search = SearchObject(func, target, box)
        with self.lock:
            result = self.search_result.get(timeout=_timeout)

        self._search = None
        return result

    def capture_image(self, filename, _timeout=5):
        result = self.__search('capture', filename, None)
        L.info(result)
        return result

    def main_loop(self):
        if self._debug:
            cv2.namedWindow("debug")
        while self._loop_flag:
            data = self.stream.picture.get()
            save_flag = False

            image_pil = Image.open(io.BytesIO(data))
            image_cv = cv2.cvtColor(np.asarray(image_pil), cv2.COLOR_RGB2BGR)

            if self._search is not None:
                if self._search.func == 'capture':
                    outputfile = os.path.join(self.space['tmp'], self._search.target)
                    result = self.__save_cv(outputfile, image_cv)
                    self.search_result.put(result)
                """
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
                """
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
