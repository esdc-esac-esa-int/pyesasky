from pyesasky.legacy.legacy_utils import deprecated


class LCatalogue:

    @deprecated("add_source")
    def addSource(self, name, ra, dec, id=None, *details):
        pass

    @deprecated("to_dict")
    def toDict(self):
        pass


class LFootprintSet:

    @deprecated("add_footprint")
    def addFootprint(self, name, stcs, id, centralRADeg=[], centralDecDeg=[], *details):
        pass

    @deprecated("to_dict")
    def toDict(self):
        pass


class LHiPS:

    @deprecated("to_dict")
    def toDict(self):
        pass
