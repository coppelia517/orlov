""" Resource Module """
import os
import json
import logging
from urllib.parse import urlparse

#pylint: disable=E0401
from anat.exception import ResourceError
from anat.utility import TMP_REFERENCE_DIR

L = logging.getLogger(__name__)


class Parser:
    """ Resource Parser Module.
    """

    @classmethod
    def search(cls, target, _id=None):
        """ search resource folder.

        Arguments:
            target(str): target folder path.
            _id(str): resource id path.

        Returns:
            filepath(str): filepath
            name(str): result name.
            bounds(tuple): result bounds. (start x, start y, end x, end y)

        """
        if _id:
            target = '%s/id' % target
        info = urlparse(target)
        base_folder = os.path.join(TMP_REFERENCE_DIR, info.netloc)
        if not os.path.exists(base_folder):
            raise ResourceError('Could not find base directory : %s' % info.netloc)
        for f in os.listdir(base_folder):
            if f.find('%s.json' % info.scheme) != -1:
                with open(os.path.join(base_folder, f), 'r') as jf:
                    data = json.load(jf)
                    result = Parser.query(data, info.path)
                    if not result:
                        ResourceError('Could not find target Infomation : %s' % info.path)
                    return Parser.path(base_folder, info.path, _id), result['name'], result['bounds']
        L.warning('Could not Found Resource.')
        return None, None, None

    @classmethod
    def path(cls, base_folder, path, _id=None):
        """ Search Path.
        """
        for i in path.split('/'):
            base_folder = os.path.join(base_folder, i)
        if _id != None:
            for j in _id.split('/'):
                base_folder = os.path.join(base_folder, j)
        return base_folder

    @classmethod
    def query(cls, d, q):
        """ Search query.
        """
        keys = q.split('/')
        nd = d
        for k in keys:
            if k == '':
                continue
            if k in nd:
                nd = nd[k]
            else:
                return None
        return nd
