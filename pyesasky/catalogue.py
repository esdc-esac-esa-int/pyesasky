from .cooFrame import CooFrame

__all__ = ['Catalogue']


class Catalogue:
    
    def __init__(self, catalogueName, cooframe, color, lineWidth):
        
        self._catalogueName = ''
        self._cooframe = CooFrame.FRAME_J2000
        self._color = '#aa2345'
        self._lineWidth = 10
        self._sources = []
        
        self._catalogueName = catalogueName
        
        if (cooframe == CooFrame.FRAME_J2000 or cooframe == CooFrame.FRAME_GALACTIC): 
            self._cooframe = cooframe
        else:
            print('coordinates frame ' + cooframe + ' not recognized. Possible options are J2000 and Galactic. Applied J2000 by default.')

        if color:
            self._color = color
        
        self._lineWidth = lineWidth
   
    def addSource(self, name, ra, dec, id=None, *details):
        currSource = {}
        currSource['name'] = name
        if not id:
            currSource['id'] = len(self._sources)
        else:
            currSource['id'] = int(id)
            
        currSource['ra'] = ra
        currSource['dec'] = dec
        
        currSource['data'] = []
        
        if len(details[0]) > 0:
            i = 0
            while i < len(details[0]):
                currSource['data'].append(details[0][i]) 
                i += 1
        self._sources.append(currSource)
        
    def toDict(self):
        
        content = dict(
            overlaySet=dict(
                type='SourceListOverlay',
                overlayName=self._catalogueName,
                cooframe=self._cooframe,
                color=self._color,
                lineWidth=self._lineWidth,
                skyObjectList=self._sources
            )
        )
        return content
    
        
