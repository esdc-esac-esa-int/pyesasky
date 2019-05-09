import ipywidgets as widgets
from traitlets import Unicode, default, Float
import requests
import configparser

from .catalogue import Catalogue
from .footprintSet import FootprintSet
from .footprintSetDescriptor import FootprintSetDescriptor
from .catalogueDescriptor import CatalogueDescriptor
from .metadataDescriptor import MetadataDescriptor
from .metadataType import MetadataType
from .HiPS import HiPS
import csv


__all__ = ['ESASkyWidget']


    
class ESASkyWidget(widgets.DOMWidget):

    _view_name = Unicode('ESASkyJSView').tag(sync=True)
    _model_name = Unicode('ESASkyJSModel').tag(sync=True)
    _view_module = Unicode('pyesasky').tag(sync=True)
    _model_module = Unicode('pyesasky').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)
    _model_module_version = Unicode('0.1.0').tag(sync=True)
    
    _targetname = Unicode('Mkr432').tag(sync=True)
    _fovDeg = Float(60).tag(sync=True)
    _colorPalette = Unicode('NATIVE').tag(sync=True)
    
    
    @default('layout')
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    def setGoToRADec(self, ra, dec):
        content = dict(
                       event='goToRADec',
                       ra=ra,
                       dec=dec
                )
        self.send(content)

    def goToTargetName(self, targetname):
        self._targetname = targetname 
        
    def setFoV(self, fovDeg):
        self._fovDeg = fovDeg
        
    def setHiPSColorPalette(self, colorPalette):
        self._colorPalette = colorPalette
        
    def overlayCatalogue(self, catalogue):
        
        content = dict(
                       event='overlayCatalogue',
                       content=catalogue.toDict()
                       )
        self.send(content)
        
    def clearCatalogue(self, catalogueName):
        content = dict(
                        event='clearCatalogue',
                       content=catalogueName
                        )
        self.send(content)

    def removeCatalogue(self, catalogueName):
        content = dict(
                        event='removeCatalogue',
                       content=catalogueName
                        )
        self.send(content)
    
    def getAvailableHiPS(self, wavelength):
        content = dict(
                        event='getAvailableHiPS',
                        )
        print(self.send(content))
        
    def clearFootprintsOverlay(self, overlayName):
        content = dict(
                        event='clearFootprintsOverlay',
                       content=overlayName
                        )
        self.send(content)

    def removeFootprintsOverlay(self, overlayName):
        content = dict(
                        event='removeFootprintsOverlay',
                       content=overlayName
                        )
        self.send(content)

    def _readProperties(self, url):
        config = configparser.RawConfigParser()
        response = requests.get(url+"properties")
        text = "[Dummy section]\n"+response.text
        config.read_string(text)
        return config
        
    def setHiPS(self, hipsName, hipsURL):
        config = self._readProperties(hipsURL)
        maxNorder = config.get('Dummy section','hips_order')
        imgFormat = config.get('Dummy section','hips_tile_format')
        cooFrame = config.get('Dummy section','hips_frame')
        if cooFrame == 'equatorial':
            cooFrame = 'J2000'
        userHiPS = HiPS(hipsName, hipsURL, cooFrame, maxNorder, imgFormat)
        print('hipsURL '+hipsURL)
        print('imgFormat '+imgFormat)
        content = dict(
                       event='changeHiPS',
                       content=userHiPS.toDict()
                       )
        self.send(content)

    def overlayFootprints(self, footprintSet):
        content = dict(
                        event='overlayFootprints',
                       content=footprintSet.toDict()
                        )
        self.send(content)

    def overlayFootprintsWithDetails(self, footprintSet):
        content = dict(
                        event='overlayFootprintsWithDetails',
                       content=footprintSet.toDict()
                        )
        self.send(content)

    def overlayCatalogueWithDetails(self, userCatalogue):
        content = dict(
                        event='overlayCatalogueWithDetails',
                       content=userCatalogue.toDict()
                        )
        self.send(content)

    def overlayFootprintsFromCSV(self, pathToFile, csvDelimiter, footprintSetDescriptor):

        footprintSet = FootprintSet(footprintSetDescriptor.getDatasetName(), 'J2000', footprintSetDescriptor.getHistoColor(), footprintSetDescriptor.getLineWidth())

        #read colums
        with open(pathToFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=csvDelimiter)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    columns = row
                    print(f'Columns identified: {", ".join(row)}')
                    line_count += 1
                    i = 0
                    while i < len(columns):
                        if columns[i] == footprintSetDescriptor.getIdColumnName():
                            columnId = columns[i]
                            print('{id} mapped to '+columnId)
                            if footprintSetDescriptor.getIdColumnName() == footprintSetDescriptor.getNameColumnName():
                                columnName = columnId
                                print('{name} mapped to '+columnName)
                        elif columns[i] == footprintSetDescriptor.getNameColumnName():
                            columnName = columns[i]
                            print('{name} mapped to '+columnName)
                        elif columns[i] == footprintSetDescriptor.getStcsColumnName():
                            columnStcs = columns[i]
                            print('{stcs} mapped to '+columnStcs)
                        elif columns[i] == footprintSetDescriptor.getCentralRADegColumnName():
                            columnRaDeg = columns[i]
                            print('{centerRaDeg} mapped to '+columnRaDeg)
                        elif columns[i] == footprintSetDescriptor.getCentralDecDegColumnName():
                            columnDecDeg = columns[i]
                            print('{centerDecDeg} mapped to '+columnDecDeg)
                        i += 1
                else:
                    i = 0
                    currDetails = []
                    currId = ''
                    currName = ''
                    currStcs = ''
                    currRaDeg = ''
                    currDecDeg = ''

                    while i < len(row):
                        if columns[i] == footprintSetDescriptor.getIdColumnName():
                            currId = row[i]
                            if footprintSetDescriptor.getIdColumnName() == footprintSetDescriptor.getNameColumnName():
                                currName = currId
                        elif columns[i] == footprintSetDescriptor.getNameColumnName():
                            currName = row[i]
                        elif columns[i] == footprintSetDescriptor.getStcsColumnName():
                            currStcs = row[i]
                        elif columns[i] == footprintSetDescriptor.getCentralRADegColumnName():
                            currRaDeg = row[i]
                        elif columns[i] == footprintSetDescriptor.getCentralDecDegColumnName():
                            currDecDeg = row[i]
                        else:
                            currMetadata = {}
                            found = False
                            if len(footprintSetDescriptor.getMetadata()) > 0:
                                j = 0
                                while j < len(footprintSetDescriptor.getMetadata()):
                                    if footprintSetDescriptor.getMetadata()[j].getLabel() == columns[i]:
                                        found = True
                                        currMetadata['name'] = footprintSetDescriptor.getMetadata()[j].getLabel()
                                        currMetadata['value'] = row[i]
                                        currMetadata['type'] = footprintSetDescriptor.getMetadata()[j].getType()

                                        break
                                    j += 1
                            elif not found:
                                currMetadata['name'] = columns[i]
                                currMetadata['value'] = row[i]
                                currMetadata['type'] = MetadataType.STRING

                            currDetails.append(currMetadata)

                        i += 1

                    
                    footprintSet.addFootprint(currName, currStcs, currId, currRaDeg, currDecDeg, currDetails)
                    
                    line_count += 1
            print(f'Processed {line_count} lines.')
            self.overlayFootprintsWithDetails(footprintSet)


    def overlayCatalogueFromAstropyTable(self, catalogueName, cooFrame, color, lineWidth, table, raColName, decColName, mainIdColName):
        
        raColNameUserInput = True
        decColNameUserInput = True
        mainIdColNameUserInput = True
        
        if not raColName:
            raColName = ''
            raColNameUserInput = False
        
        if not decColName:
            decColName = ''
            decColNameUserInput = False
            
        if not mainIdColName:
            mainIdColName = ''
            mainIdColNameUserInput = False
        
        i = 0


        if (not raColNameUserInput and not decColNameUserInput and not mainIdColNameUserInput):
             
            while i < len(table.colnames):
                
                colName = table.colnames[i]

                if len(table[colName].meta) > 0:
                    metaType = table[colName].meta['ucd']
                    if ('pos.eq.ra;meta.main' in metaType and not raColNameUserInput):
                        raColName = colName
                    elif ('pos.eq.dec;meta.main' in metaType and not decColNameUserInput):
                        decColName = colName
                    elif ('meta.id;meta.main' in metaType and not mainIdColNameUserInput):
                        mainIdColName = colName 
                i += 1
        
        if not lineWidth:
            lineWidth = 5
            
        astropyCatalogue = Catalogue(catalogueName, cooFrame, color, lineWidth)
        
        j = 0
        currId = j
        
        while j < len(table):
            currDetails = []
            k = 0
            while k < len(table.colnames):
                currMetadata = {}
                colName = table.colnames[k]
                currValue = str(table[j][k])
                                
                if colName == raColName:
                    currRaDeg = currValue
                    
                elif colName == decColName:
                    currDecDeg = currValue
                    
                elif colName == mainIdColName:
                    currName = currValue
                    
                else:
                    currMetadata['name'] = colName
                    currMetadata['value'] = currValue
                    if 'ucd' in table[colName].meta:
                        currMetadata['type'] = self.convertTapType2ESASky(table[colName].meta['ucd'])
                    else:
                        currMetadata['type'] = 'STRING'
                    currDetails.append(currMetadata)
                        
                k += 1
                
            currId = j
            
            astropyCatalogue.addSource(currName, currRaDeg, currDecDeg, currId, currDetails)
            j += 1
            
        self.overlayCatalogueWithDetails(astropyCatalogue)




    def convertTapType2ESASky(self, tapType):
        if tapType == 'meta.number':
            return 'DOUBLE'
        else:
            return 'STRING'
        
    def parseValue(self, valueObj, colName):
        if type(valueObj) == '<class \'bytes\'>':
            return valueObj.decode('utf-8')
        else:
            return valueObj
        
    
    def overlayCatalogueFromCSV(self, pathToFile, csvDelimiter, catalogueDescriptor, cooFrame):
        
        catalogue = Catalogue(catalogueDescriptor.getDatasetName(), cooFrame, catalogueDescriptor.getHistoColor(), catalogueDescriptor.getLineWidth())
        
        #read colums
        with open(pathToFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=csvDelimiter)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    columns = row
                    print(f'Column identified: {", ".join(row)}')
                    line_count += 1
                    i = 0
                    while i < len(columns):
                        if columns[i] == catalogueDescriptor.getIdColumnName():
                            columnId = columns[i]
                            print('{id} column identified: '+columnId)
                            if catalogueDescriptor.getIdColumnName() == catalogueDescriptor.getNameColumnName():
                                columnName = columnId
                                print('{name} column identified: '+columnName)
                        elif columns[i] == catalogueDescriptor.getNameColumnName():
                            columnName = columns[i]
                            print('{name} column identified: '+columnName)
                        elif columns[i] == catalogueDescriptor.getRADegColumnName():
                            columnRaDeg = columns[i]
                            print('{centerRaDeg} column identified: '+columnRaDeg)
                        elif columns[i] == catalogueDescriptor.getDecDegColumnName():
                            columnDecDeg = columns[i]
                            print('{currDecDeg} column identified: '+columnDecDeg)
                        i += 1
                else:
                    i = 0
                    currDetails = []
                    currId = ''
                    currName = ''
                    currRaDeg = ''
                    currDecDeg = ''

                    while i < len(row):
                        if columns[i] == catalogueDescriptor.getIdColumnName():
                            currId = row[i]
                            if catalogueDescriptor.getIdColumnName() == catalogueDescriptor.getNameColumnName():
                                currName = currId
                        elif columns[i] == catalogueDescriptor.getNameColumnName():
                            currName = row[i]
                        elif columns[i] == catalogueDescriptor.getRADegColumnName():
                            currRaDeg = row[i]
                        elif columns[i] == catalogueDescriptor.getDecDegColumnName():
                            currDecDeg = row[i]
                        else:
                            currMetadata = {}
                            found = False
                            if len(catalogueDescriptor.getMetadata()) > 0:
                                j = 0
                                while j < len(catalogueDescriptor.getMetadata()):
                                    if catalogueDescriptor.getMetadata()[j].getLabel() == columns[i]:
                                        found = True
                                        currMetadata['name'] = catalogueDescriptor.getMetadata()[j].getLabel()
                                        currMetadata['value'] = row[i]
                                        currMetadata['type'] = catalogueDescriptor.getMetadata()[j].getType()
                                        break
                                    j += 1
                            elif not found:
                                currMetadata['name'] = columns[i]
                                currMetadata['value'] = row[i]
                                currMetadata['type'] = MetadataType.STRING

                            currDetails.append(currMetadata)

                        i += 1
                    
                    catalogue.addSource(currName, currRaDeg, currDecDeg, currId, currDetails)
                    line_count += 1
            print(f'Processed {line_count} lines.')
            self.overlayCatalogueWithDetails(catalogue)

