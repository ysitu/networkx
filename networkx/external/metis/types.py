from numbers import Number

from .enums import *
try:
    from ._metis import set_default_options
except ImportError:
    pass

__all__ = ['MetisOptions', 'MetisError']


class MetisOptions(object):

    def __init__(self):
        set_default_options(self)

    @property
    def ptype(self):
        return self._ptype

    @ptype.setter
    def ptype(self, value):
        self._ptype = MetisPType(value)

    @property
    def objtype(self):
        return self._objtype

    @objtype.setter
    def objtype(self, value):
        self._objtype = MetisObjType(value)

    @property
    def ctype(self):
        return self._ctype

    @ctype.setter
    def ctype(self, value):
        self._ctype = MetisCType(value)

    @property
    def iptype(self):
        return self._iptype

    @iptype.setter
    def iptype(self, value):
        self._iptype = MetisIPType(value)

    @property
    def rtype(self):
        return self._rtype

    @rtype.setter
    def rtype(self, value):
        self._rtype = MetisRType(value)

    @property
    def ncuts(self):
        return self._ncuts

    @ncuts.setter
    def ncuts(self, value):
        if not isinstance(value, Number) or value != int(value):
            raise ValueError('{0} is not an int'.format(repr(value)))
        self._ncuts = int(value)

    @property
    def nseps(self):
        return self._nseps

    @nseps.setter
    def nseps(self, value):
        if not isinstance(value, Number) or value != int(value):
            raise ValueError('{0} is not an int'.format(repr(value)))
        self._nseps = int(value)

    @property
    def numbering(self):
        return self._numbering

    @numbering.setter
    def numbering(self, value):
        self._numbering = MetisNumbering(value)

    @property
    def niter(self):
        return self._niter

    @niter.setter
    def niter(self, value):
        if not isinstance(value, Number) or value != int(value):
            raise ValueError('{0} is not an int'.format(repr(value)))
        self._niter = value

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        if not isinstance(value, Number) or value != int(value):
            raise ValueError('{0} is not an int'.format(repr(value)))
        self._seed = value

    @property
    def minconn(self):
        return self._minconn

    @minconn.setter
    def minconn(self, value):
        self._minconn = bool(value)

    @property
    def no2hop(self):
        return self._no2hop

    @no2hop.setter
    def no2hop(self, value):
        self._no2hop = bool(value)

    @property
    def contig(self):
        return self._contig

    @contig.setter
    def contig(self, value):
        self._contig = bool(value)

    @property
    def compress(self):
        return self._compress

    @compress.setter
    def compress(self, value):
        self._compress = bool(value)

    @property
    def ccorder(self):
        return self._ccorder

    @ccorder.setter
    def ccorder(self, value):
        self._ccorder = bool(value)

    @property
    def pfactor(self):
        return self._pfactor

    @pfactor.setter
    def pfactor(self, value):
        if not isinstance(value, Number) or value != int(value):
            raise ValueError('{0} is not an int'.format(repr(value)))
        self._pfactor = value

    @property
    def ufactor(self):
        return self._ufactor

    @pfactor.setter
    def ufactor(self, value):
        if not isinstance(value, Number) or value != int(value):
            raise ValueError('{0} is not an int'.format(repr(value)))
        self._ufactor = value

    @property
    def dbglvl(self):
        return self._dbglvl

    @dbglvl.setter
    def dbglvl(self, value):
        if (not isinstance(value, Number) or value != int(value) or
            not (value == -1 or (value >= 0 and value < 512) or
                 (value >= 2048 and value < 2560))):
            raise ValueError('{0} is not a valid dbglvl'.format(repr(value)))
        self._dbglvl = int(value)

    def __repr__(self):
        names = ['ptype', 'objtype', 'ctype', 'iptype', 'rtype', 'ncuts',
                 'nseps', 'numbering', 'niter', 'seed', 'minconn', 'no2hop',
                 'contig', 'compress', 'ccorder', 'pfactor', 'ufactor']
        return '{0}({1})'.format(
            self.__class__.__name__,
            ', '.join('{0}={1}'.format(name, repr(getattr(self, name)))
                      for name in names))


class MetisError(Exception):

    def __init__(self, rstatus):
        super(MetisError, self).__init__(rstatus)
