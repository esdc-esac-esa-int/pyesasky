
__all__ = ['HiPS']


class HiPS:
    
    _name = ''
    _id = ''
    _url = ''
    _cooFrame = 'J2000'
    _maxNorder = '3'
    _imgFormat = 'png'


    def __init__(self, name, url, cooframe, maxNorder, imgFormat):
        self._name = name
        self._id = name
        self._url = url
        self._cooframe = cooframe
        self._maxNorder = maxNorder
        self._imgFormat = imgFormat

    def toDict(self):
        
        content = dict(
            HiPS=dict(
                name=self._name,
                id=self._id,
                url=self._url,
                cooframe=self._cooframe,
                maxnorder=self._maxNorder,
                imgformat=self._imgFormat
            )
        )
        return content
    
        
