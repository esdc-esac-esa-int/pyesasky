__all__ = ['CatalogueDescriptor']

class CatalogueDescriptor:
    
    _idColumnName = ''
    _nameColumnName = ''
    #_stcsColumnName  = ''
    _centralRADegColumnName = ''
    _centralDecDegColumnName = ''
    _datasetName = ''
    _lineWidth  = 5
    _histoColor = 'green'
    _metadata = []


    def __init__(self, datasetName, color, lineWidth, idColumnName, nameColumnName, RADegColumnName, decDegColumnName, metadata):
        self._datasetName = datasetName
        self._histoColor = color
        self._lineWidth = lineWidth
        
        self._idColumnName = idColumnName
        self._nameColumnName = nameColumnName
        self._RADegColumnName = RADegColumnName
        self._decDegColumnName = decDegColumnName

        self._metadata = metadata

    def getDatasetName(self):
        return self._datasetName
    
    def getHistoColor(self):
        return self._histoColor
    
    def getLineWidth(self):
        return self._lineWidth
    
    def getIdColumnName(self):
        return self._idColumnName
    
    def getNameColumnName(self):
        return self._nameColumnName
        
    def getRADegColumnName(self):
        return self._RADegColumnName
    
    def getDecDegColumnName(self):
        return self._decDegColumnName
    
    def getMetadata(self):
        return self._metadata

    def addMetadataDefinition(self, metadataDescriptor):
        self._metadata.append(metadataDescriptor)

    def toDict(self):
        
        content = dict(
            mission=self._datasetName,
            tapTable='',
            countColumn='',
            guiShortName=self._guiShortName,
            guiLongName=self._guiLongName,
            histoColor=self._histoColor,
            countFovLimit=360,
            fovLimit=90.0,
            archiveURL='',
            archiveProductURI='',
            adsPublicationsMaxRows=0,
            tabCount=0,
            sourceLimit=100000,
            sourceLimitDescription='',
            posTapColumn='pos',
            polygonRaTapColumn=self._polygonRaTapColumn,
            polygonDecTapColumn=self._polygonDecTapColumn,
            polygonNameTapColumn=self._polygonNameTapColumn,
            orderBy='',
            metadata=self._metadata
        )
        return content
        


