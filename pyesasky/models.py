from pyesasky.legacy.legacy_models import LCatalogue, LFootprintSet, LHiPS


class CooFrame:

    FRAME_J2000 = "J2000"

    FRAME_GALACTIC = "Galactic"

    @classmethod
    def all(cls):
        return {cls.FRAME_J2000, cls.FRAME_GALACTIC}


class ImgFormat:

    JPEG = "jpeg"
    PNG = "png"

    @classmethod
    def all(cls):
        return {cls.JPEG, cls.PNG}


class MetadataType:

    STRING = "STRING"
    DOUBLE = "DOUBLE"
    RA_DEG = "RA"
    DEC_DEG = "DEC"

    @classmethod
    def all(cls):
        return {cls.STRING, cls.DOUBLE, cls.RA_DEG, cls.DEC_DEG}


class Catalogue(LCatalogue):

    def __init__(self, catalogue_name, cooframe, color, line_width):

        self._catalogue_name = ""
        self._cooframe = CooFrame.FRAME_J2000
        self._color = color if color else "#aa2345"
        self._line_width = line_width if line_width else 10
        self._sources = []

        self._catalogue_name = catalogue_name

        if cooframe in CooFrame.all():
            self._cooframe = cooframe
        else:
            print(
                f"""coordinates frame {cooframe} not recognized.
                Possible options are J2000 and Galactic.Applied J2000 by default"""
            )

    def add_source(self, name, ra, dec, id=None, *details):
        source = {}
        source["name"] = name
        if not id:
            source["id"] = len(self._sources)
        else:
            source["id"] = int(id)

        source["ra"] = ra
        source["dec"] = dec

        source["data"] = []

        if details and len(details[0]) > 0:
            i = 0
            while i < len(details[0]):
                source["data"].append(details[0][i])
                i += 1
        self._sources.append(source)

    def to_dict(self):

        content = dict(
            overlaySet=dict(
                type="SourceListOverlay",
                overlayName=self._catalogue_name,
                cooframe=self._cooframe,
                color=self._color,
                lineWidth=self._line_width,
                skyObjectList=self._sources,
            )
        )
        return content


class FootprintSet(LFootprintSet):

    def __init__(self, name, cooframe, color, line_width):
        self._name = ""
        self._cooframe = "J2000"
        self._color = color if color else "#aa2345"
        self._line_width = line_width if line_width else 10
        self._footprints = []

        self._name = name

        if cooframe in CooFrame.all():
            self._cooframe = cooframe
        else:
            print(
                f"""Coordinates frame {cooframe} is not recognized.
                Possible options are J2000 and Galactic. Applied J2000 by default"""
            )

    # details is a dictionary d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
    def add_footprint(self, name, stcs, id, ra_col, dec_col, *details):
        footprint = {}

        footprint["name"] = name
        if not id:
            footprint["id"] = len(self._footprints)
        else:
            footprint["id"] = int(id)

        stcs = stcs.upper()
        stcs = stcs.replace("ICRS", "")
        stcs = stcs.replace("J2000", "")
        stcs = stcs.replace("FK5", "")
        stcs = stcs.replace("POLYGON", "POLYGON J2000")
        stcs = stcs.replace("CIRCLE", "CIRCLE J2000")
        footprint["stcs"] = stcs

        if not ra_col:
            # we take the first ra coord in the stcs, just after POLYGON J2000
            footprint["ra_deg"] = stcs.split()[2]
        else:
            footprint["ra_deg"] = ra_col

        if not dec_col:
            # we take the first dec coord in the stcs, just after POLYGON J2000
            footprint["dec_deg"] = stcs.split()[3]
        else:
            footprint["dec_deg"] = dec_col

        footprint["data"] = []
        if len(details[0]) > 0:
            i = 0
            while i < len(details[0]):
                footprint["data"].append(details[0][i])
                i += 1

        self._footprints.append(footprint)

    def to_dict(self):

        content = dict(
            overlaySet=dict(
                type="FootprintListOverlay",
                overlayName=self._name,
                cooframe=self._cooframe,
                color=self._color,
                lineWidth=self._line_width,
                skyObjectList=self._footprints,
            )
        )
        return content


class HiPS(LHiPS):

    def __init__(self, name, url, cooframe, max_order, img_format):
        self._name = name
        self._url = url
        self._cooframe = cooframe
        self._max_order = max_order
        self._img_format = img_format

        if cooframe in CooFrame.all():
            self._cooframe = cooframe
        else:
            print(
                f"""Coordinates frame {cooframe} is not recognized.
                Possible options are J2000 and Galactic. Applied J2000 by default"""
            )
            self._cooframe = CooFrame.FRAME_J2000

        if img_format in ImgFormat.all():
            self._img_format = img_format
        else:
            print(
                f"""Image format {img_format} is not recognized.
                Possible options are {', '.join(ImgFormat.all())}"""
            )

            self._img_format = ImgFormat.PNG

    def to_dict(self):
        content = dict(
            hips=dict(
                name=self._name,
                url=self._url,
                cooframe=self._cooframe,
                maxnorder=self._max_order,
                imgformat=self._img_format,
            )
        )
        return content
