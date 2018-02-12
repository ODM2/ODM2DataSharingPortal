# coverage.py
from abc import ABCMeta, abstractmethod


class CoverageImplementor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_dict(self):
        pass


class CoverageFactory(object):
    def __init__(self, coverage=None, implementation=None):
        if implementation:
            self.__implementation = implementation
        elif coverage:
            type_ = str(coverage['type'])
            if type_.lower() == 'box':
                self.__implementation = BoxCoverage(**coverage)
            elif type_.lower() == 'point':
                self.__implementation = PointCoverage(**coverage)
            else:
                self.__implementation = Coverage(**coverage)
        else:
            self.__implementation = Coverage()

    @property
    def type(self):
        return self.__implementation.type

    def to_dict(self):
        return self.__implementation.to_dict()


class Coverage(CoverageImplementor):
    def __init__(self, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)

    def to_dict(self):
        value = {}
        for attr in self.__dict__:
            value[attr] = self.__dict__[attr]
        return {
            'type': self.type_,
            'value': value
        }


class BoxCoverage(Coverage):
    type_ = 'box'

    def __init__(self, northlimit=None, eastlimit=None, southlimit=None, westlimit=None, projection=None, units=None,
                 **kwargs):
        super(BoxCoverage, self).__init__(**kwargs)
        self.northlimit = northlimit
        self.eastlimit = eastlimit
        self.southlimit = southlimit
        self.westlimit = westlimit
        self.projection = projection
        self.units = units

    def to_dict(self):
        return {
            'type': self.type_,
            'value': {
                'northlimit': self.northlimit,
                'eastlimit': self.eastlimit,
                'southlimit': self.southlimit,
                'westlimit': self.westlimit,
                'units': self.units,
                'projection': self.projection
            }
        }


class PointCoverage(Coverage):
    type_ = 'point'

    def __init__(self, name=None, latitude=None, longitude=None, projection=None, units=None, **kwargs):
        super(PointCoverage, self).__init__(**kwargs)
        self.name = name
        self.north = latitude
        self.east = longitude
        self.projection = projection
        self.units = units

    def to_dict(self):
        return {
            'type': self.type_,
            'name': self.name,
            'value': {
                'north': self.north,
                'east': self.east,
                'projection': self.projection,
                'units': self.units
            }
        }


class PeriodCoverage(Coverage):
    type_ = 'period'

    def __init__(self, start=None, end=None, **kwargs):
        super(PeriodCoverage, self).__init__(**kwargs)
        self.start = start
        self.end = end

    def to_dict(self):
        return {
            'type': self.type_,
            'value': {
                'start': self.start,
                'end': self.end
            }
        }


__all__ = ["CoverageFactory", "Coverage", "BoxCoverage", "PointCoverage", "PeriodCoverage"]
