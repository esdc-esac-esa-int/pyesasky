from .cooFrame import CooFrame
from .imgFormat import ImgFormat

__all__ = ['HiPS']


class HiPS:

    def __init__(self, name, url, cooframe, maxNorder, imgFormat):
        self._name = name
        self._url = url
        self._cooframe = cooframe
        self._maxNorder = maxNorder
        self._imgFormat = imgFormat
        
        if (cooframe.lower() == CooFrame.FRAME_J2000.lower() or cooframe.lower() == CooFrame.FRAME_GALACTIC.lower()): 
            self._cooframe = cooframe
        else:
            print('coordinates frame ' + cooframe + ' not recognized. Possible options are ' + CooFrame.FRAME_J2000 + ' and ' + CooFrame.FRAME_GALACTIC + '. Applied ' + CooFrame.FRAME_J2000 + ' by default.')
            self._cooframe = CooFrame.FRAME_J2000
        
        if (imgFormat == ImgFormat.PNG or imgFormat == ImgFormat.JPEG): 
            self._imgFormat = imgFormat
        else:
            print('image format ' + imgFormat + ' not recognized. Possible options are ' + ImgFormat.PNG + ' and ' + ImgFormat.JPEG + '. Applied ' + ImgFormat.PNG + ' by default.')
            self._imgFormat = ImgFormat.PNG


    def toDict(self):
        content = dict(
            hips = dict(
                name=self._name,
                url=self._url,
                cooframe=self._cooframe,
                maxnorder=self._maxNorder,
                imgformat=self._imgFormat
            )
        )
        return content
    
        
