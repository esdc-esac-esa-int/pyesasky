class CooFrame:

    FRAME_J2000 = "J2000"

    FRAME_GALACTIC = "Galactic"


class ImgFormat:

    JPEG = "jpeg"

    PNG = "png"


class MetadataType:

    STRING = "STRING"
    DOUBLE = "DOUBLE"
    RA_DEG = "RA"
    DEC_DEG = "DEC"


class Catalogue:

    def __init__(self, catalogue_name, cooframe, color, line_width):

        self._catalogue_name = ""
        self._cooframe = CooFrame.FRAME_J2000
        self._color = "#aa2345"
        self._line_width = 10
        self._sources = []

        self._catalogue_name = catalogue_name

        if cooframe == CooFrame.FRAME_J2000 or cooframe == CooFrame.FRAME_GALACTIC:
            self._cooframe = cooframe
        else:
            print(
                "coordinates frame "
                + cooframe
                + " not recognized. Possible options are J2000 and Galactic. Applied J2000 by default."
            )

        if color:
            self._color = color

        self._line_width = line_width

    def addSource(self, name, ra, dec, id=None, *details):
        currSource = {}
        currSource["name"] = name
        if not id:
            currSource["id"] = len(self._sources)
        else:
            currSource["id"] = int(id)

        currSource["ra"] = ra
        currSource["dec"] = dec

        currSource["data"] = []

        if len(details[0]) > 0:
            i = 0
            while i < len(details[0]):
                currSource["data"].append(details[0][i])
                i += 1
        self._sources.append(currSource)

    def toDict(self):

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


class FootprintSet:

    def __init__(self, footprintSetName, cooframe, color, lineWidth):
        self._footprintSetName = ""
        self._cooframe = "J2000"
        self._color = "#aa2345"
        self._lineWidth = 10
        self._footprints = []

        self._footprintSetName = footprintSetName

        if cooframe == "J2000" or cooframe == "Galactic":
            self._cooframe = cooframe
        else:
            print(
                "coordinates frame "
                + cooframe
                + " not recognized. Possible options are J2000 and Galactic. Applied J2000 by default."
            )

        if color:
            self._color = color

        self._lineWidth = lineWidth

    # details is a dictionary d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
    def addFootprint(self, name, stcs, id, centralRADeg=[], centralDecDeg=[], *details):
        currFootprint = {}

        currFootprint["name"] = name
        if not id:
            currFootprint["id"] = len(self._footprints)
        else:
            currFootprint["id"] = int(id)

        stcs = stcs.upper()
        stcs = stcs.replace("ICRS", "")
        stcs = stcs.replace("J2000", "")
        stcs = stcs.replace("FK5", "")
        stcs = stcs.replace("POLYGON", "POLYGON J2000")
        stcs = stcs.replace("CIRCLE", "CIRCLE J2000")
        currFootprint["stcs"] = stcs

        if not centralRADeg:
            # we take the first ra coord in the stcs, just after POLYGON J2000
            currFootprint["ra_deg"] = stcs.split()[2]
        else:
            currFootprint["ra_deg"] = centralRADeg

        if not centralDecDeg:
            # we take the first dec coord in the stcs, just after POLYGON J2000
            currFootprint["dec_deg"] = stcs.split()[3]
        else:
            currFootprint["dec_deg"] = centralDecDeg

        currFootprint["data"] = []
        if len(details[0]) > 0:
            i = 0
            while i < len(details[0]):
                currFootprint["data"].append(details[0][i])
                i += 1

        self._footprints.append(currFootprint)

    def toDict(self):

        content = dict(
            overlaySet=dict(
                type="FootprintListOverlay",
                overlayName=self._footprintSetName,
                cooframe=self._cooframe,
                color=self._color,
                lineWidth=self._lineWidth,
                skyObjectList=self._footprints,
            )
        )
        return content


class HiPS:

    def __init__(self, name, url, cooframe, maxNorder, imgFormat):
        self._name = name
        self._url = url
        self._cooframe = cooframe
        self._maxNorder = maxNorder
        self._imgFormat = imgFormat

        if (
            cooframe.lower() == CooFrame.FRAME_J2000.lower()
            or cooframe.lower() == CooFrame.FRAME_GALACTIC.lower()
        ):
            self._cooframe = cooframe
        else:
            print(
                "coordinates frame "
                + cooframe
                + " not recognized. Possible options are "
                + CooFrame.FRAME_J2000
                + " and "
                + CooFrame.FRAME_GALACTIC
                + ". Applied "
                + CooFrame.FRAME_J2000
                + " by default."
            )
            self._cooframe = CooFrame.FRAME_J2000

        if imgFormat == ImgFormat.PNG or imgFormat == ImgFormat.JPEG:
            self._imgFormat = imgFormat
        else:
            print(
                "image format "
                + imgFormat
                + " not recognized. Possible options are "
                + ImgFormat.PNG
                + " and "
                + ImgFormat.JPEG
                + ". Applied "
                + ImgFormat.PNG
                + " by default."
            )
            self._imgFormat = ImgFormat.PNG

    def toDict(self):
        content = dict(
            hips=dict(
                name=self._name,
                url=self._url,
                cooframe=self._cooframe,
                maxnorder=self._maxNorder,
                imgformat=self._imgFormat,
            )
        )
        return content
