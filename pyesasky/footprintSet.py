
__all__ = ['FootprintSet']


class FootprintSet:
    
    def __init__(self, footprintSetName, cooframe, color, lineWidth):
        self._footprintSetName = ''
        self._cooframe = 'J2000'
        self._color = '#aa2345'
        self._lineWidth = 10
        self._footprints = []
        
        self._footprintSetName = footprintSetName        
        
        if (cooframe == 'J2000' or cooframe == 'Galactic'):
            self._cooframe = cooframe
        else:
            print('coordinates frame ' + cooframe + ' not recognized. Possible options are J2000 and Galactic. Applied J2000 by default.')
        
        if color:
            self._color = color
        
        self._lineWidth = lineWidth
    
    # details is a dictionary d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
    def addFootprint(self, name, stcs, id, centralRADeg=[], centralDecDeg=[], *details):
        currFootprint = {}

        currFootprint['name'] = name
        if not id:
            currFootprint['id'] = len(self._footprints)
        else:
            currFootprint['id'] = int(id)
        
        stcs = stcs.upper()
        stcs = stcs.replace('ICRS','')
        stcs = stcs.replace('J2000','')
        stcs = stcs.replace('FK5','')
        stcs = stcs.replace('POLYGON','POLYGON J2000')
        stcs = stcs.replace('CIRCLE','CIRCLE J2000')
        currFootprint['stcs'] = stcs

        if not centralRADeg:
            # we take the first ra coord in the stcs, just after POLYGON J2000
            currFootprint['ra_deg'] = stcs.split()[2]
        else:
            currFootprint['ra_deg'] = centralRADeg

        if not centralDecDeg:
            # we take the first dec coord in the stcs, just after POLYGON J2000
            currFootprint['dec_deg'] = stcs.split()[3]
        else:
            currFootprint['dec_deg'] = centralDecDeg
        
        currFootprint['data'] = []
        if len(details[0]) > 0:
            i = 0
            while i < len(details[0]):
                currFootprint['data'].append(details[0][i]) 
                i += 1

        self._footprints.append(currFootprint)

    def toDict(self):

        content = dict(
            overlaySet=dict(
                type='FootprintListOverlay',
                overlayName=self._footprintSetName,
                cooframe=self._cooframe,
                color=self._color,
                lineWidth=self._lineWidth,
                skyObjectList=self._footprints
            )
        )
        return content
