import ipywidgets as widgets
from traitlets import Unicode, default, Float, Dict, List
import requests
import warnings
import re
import configparser
from urllib3.exceptions import HTTPError

from traitlets import observe
from .catalogue import Catalogue
from .footprintSet import FootprintSet
from .footprintSetDescriptor import FootprintSetDescriptor
from .catalogueDescriptor import CatalogueDescriptor
from .metadataDescriptor import MetadataDescriptor
from .metadataType import MetadataType
from .HiPS import HiPS
import csv
import json
import os.path
import tornado.web
import tornado.httpserver
import time

__all__ = ['ESASkyWidget']
    
class ESASkyWidget(widgets.DOMWidget):

    _view_name = Unicode('ESASkyJSView').tag(sync=True)
    _model_name = Unicode('ESASkyJSModel').tag(sync=True)
    _view_module = Unicode('pyesasky').tag(sync=True)
    _model_module = Unicode('pyesasky').tag(sync=True)
    _view_module_version = Unicode('1.7.1').tag(sync=True)
    _model_module_version = Unicode('1.7.1').tag(sync=True)
    _intended_server_version = "3.7.1"
    _view_language = Unicode('En').tag(sync=True)
    _view_module_ids = List().tag(sync=True)
    view_height = Unicode('800px').tag(sync=True)
    
    def __init__(self, lang = 'en'):
        super().__init__()
        self.messageTimeOut=20.0 #s
        self.initTimeOut=30.0
        self.msgId = 0
        self.guiReady = False
        self.guiReadyCallSent = False
        availableLanguages = ['en', 'es', 'zh']
        
        serverVersionResponse = requests.get("https://sky.esa.int/esasky-tap/version")
        if(serverVersionResponse.status_code == 200):
            serverVersion = re.match('\"(\d+\.?\d*\.?\d*).*',serverVersionResponse.text).group(1)
            if(serverVersion > self._intended_server_version):
                warnings.warn("The ESASky server has been updated since your installation of pyESASky.\n\n"\
                            + "Some commands might malfunction. Please upgrade your installation if you experience any issue.\n\n" \
                            + "$pip install --upgrade pyesasky \n\nand if you're using Jupyter Lab: \n\n$jupyter labextension install pyesasky@latest")

        if lang.lower() in availableLanguages:
           self._view_language = lang
        else:
            raise EnvironmentError("Wrong language code used. Available are " + str(availableLanguages).strip('[]'))
        for stream in self.comm.kernel.shell_streams:
            stream.flush()
        for item in self.comm.kernel.msg_queue._queue:
            if "comm_close" in str(item[3][1][3]) and self.comm.comm_id in str(item[3][1][6]):
                raise ConnectionError("Communication could not be established with widget. \n" \
                + "Possible errors could be that installed version of PyESASky differs in python " \
                + "and Jupyter lab. \nMake sure to upgrade to the latest version of both \n" \
                + "pip install --upgrade pyesasky \njupyter labextension install pyesasky@latest\n\n"\
                + "Also make sure that jupyter lab manager is up to date with your current jupyter lab version\n"\
                + "jupyter labextension install @jupyter-widgets/jupyterlab-manager\n\n"\
                + "It could also be another labextension that is not compatible with the current Jupyter lab version\n"\
                + "A more drastic way is to run $jupyter labextension clean --extensions \n"\
                + "CAUTION!! This will remove all your extensions and you will need to reinstall them "\
                + "one by one and check that it works.")
        
    def _waitGuiReady(self):
        self.guiReadyCallSent = True
        startTime = time.time()
        while time.time()-startTime<self.initTimeOut:
                content = dict(event='initTest')
                self._sendToFrontEnd(content)
                time.sleep(1)
                val = self._loopMessageQueue()
                if val is not None:
                    self.guiReady = True
                    return val
        raise(TimeoutError("Widget doesn't seem to have initialised properly"))

    @default('layout')
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    def _sendToFrontEnd(self,content):
        if not (self.guiReady or self.guiReadyCallSent):
            self._waitGuiReady()
        content['origin'] = 'pyesasky'
        self.msgId += 1
        content['msgId'] = self.msgId
        super().send(content)

    def _sendAvaitCallback(self,content):
        self._sendToFrontEnd(content)
        startTime = time.time()
        while time.time()-startTime<self.messageTimeOut:
            val = self._loopMessageQueue()
            if val is not None:
                if val == "No return value":
                    return None
                else:
                    return val
            time.sleep(0.1)
        raise(TimeoutError("Request timed out"))


    def _loopMessageQueue(self):
        for stream in self.comm.kernel.shell_streams:
            stream.flush()
        for item in self.comm.kernel.msg_queue._queue:
            try:
                msg = item[3][1][6]
                msg = json.loads(str(msg))
                if int(msg['data']['content']['msgId']) == self.msgId:
                    self.comm.kernel.msg_queue._queue.remove(item)
                    self.comm.kernel.msg_queue.task_done()
                    if 'extras' in msg['data']['content'].keys():
                        if 'message' in msg['data']['content']['extras'].keys():
                            print(msg['data']['content']['extras']['message'])

                    if 'values' in msg['data']['content'].keys():
                        data = msg['data']['content']['values']
                        if len(data.values()) == 1:
                            return list(data.values())[0]
                        else:
                            return msg['data']['content']['values']
                    else:
                        return "No return value"
            except:
                pass

    def setViewHeight(self, height):
        """Sets the widget view height in pixels """
        
        height = str(height)
        if not height.endswith('px'):
            height = height + 'px'
        self.view_height = height

    def showCoordinateGrid(self,show = True):
        """Overlays a coordinate grid on the sky"""
        
        content = dict( 
                        event='showCoordinateGrid',
                        content = dict(show=show)
        )
        self._sendToFrontEnd(content)

    def getCenter(self,cooFrame = 'J2000'):
        """Returns the coordinate of the center of the screen in specified coordinate Frame."""
       
        if cooFrame not in ['J2000','GALACTIC']:
            print('Coordinate frame must be J2000 or GALACTIC')
            return
        content = dict(
                        event='getCenter',
                        content = dict(cooFrame=cooFrame)
        )
        return self._sendAvaitCallback(content)


    def plotObservations(self, missionId):
        """Overlays availabe observations for the specified mission on the sky"""

        content = dict(
                event = 'plotObservations',
                content = dict(missionId=missionId)
        )
        return self._sendAvaitCallback(content)

    def plotCatalogues(self, missionId):
        """Overlays availabe catalogues for the specified mission on the sky"""
        
        content = dict(
                event = 'plotCatalogues',
                content = dict(missionId=missionId)
        )
        return self._sendAvaitCallback(content)

    def plotSpectra(self, missionId):
        """Overlays availabe spectra for the specified mission on the sky"""

        content = dict(
                event = 'plotSpectra',
                content = dict(missionId=missionId)
        )
        return self._sendAvaitCallback(content)
    
    def coneSearchObservations(self, missionId, ra, dec, radius):
        """Overlays availabe observations within the specified cone for the specified mission on the sky
         
         Arguments:
        ra -- float or string in decimal format
        dec -- float or string in decimal format
        radius -- float or string in decimal degrees
        """

        content = dict(
                event = 'plotObservations',
                content = dict(
                    missionId=missionId,
                    ra = ra,
                    dec = dec,
                    radius = radius
                )
        )
        return self._sendAvaitCallback(content)

    def coneSearchCatalogues(self, missionId, ra, dec, radius):
        """Overlays availabe catalogues within the specified cone for the specified mission on the sky
         
         Arguments:
        ra -- float or string in decimal format
        dec -- float or string in decimal format
        radius -- float or string in decimal degrees
        """
        content = dict(
                event = 'plotCatalogues',
                content = dict(
                    missionId=missionId,
                    ra = ra,
                    dec = dec,
                    radius = radius
                )
        )
        return self._sendAvaitCallback(content)

    def coneSearchSpectra(self, missionId, ra, dec, radius):
        """Overlays availabe spectra within the specified cone for the specified mission on the sky
         
         Arguments:
        ra -- float or string in decimal format
        dec -- float or string in decimal format
        radius -- float or string in decimal degrees
        """

        content = dict(
                event = 'plotSpectra',
                content = dict(
                    missionId=missionId,
                    ra = ra,
                    dec = dec,
                    radius = radius
                )
        )
        return self._sendAvaitCallback(content)
    
    def getObservationsCount(self):
        """Returns the number of observations per mission in the current view of the sky"""
        
        content = dict(
                event = 'getObservationsCount'
        )
        return self._sendAvaitCallback(content)

    def getCataloguesCount(self):
        """Returns the number of catalogs per mission in the current view of the sky"""
        
        content = dict(
                event = 'getCataloguesCount'
        )
        return self._sendAvaitCallback(content)
    
    def getPublicationsCount(self):
        """Returns the number of publications in the current view of the sky"""

        content = dict(
                event = 'getPublicationsCount'
        )
        return self._sendAvaitCallback(content)

    def getSpectraCount(self):
        """Returns the number of spectra per mission in the current view of the sky"""

        content = dict(
                event = 'getSpectraCount'
        )
        return self._sendAvaitCallback(content)

    def getResultPanelData(self):
        """Returns the content of the currently active datapanel as a dictionary"""
        content = dict(
                event = 'getResultPanelData'
        )
        return self._sendAvaitCallback(content)

    def closeResultPanelTab(self, index = -1):
        """Close the tab on index or current open if no argument"""
        content = dict(
                event = 'closeResultPanelTab',
                content = dict(index=index)
        )
        return self._sendToFrontEnd(content)

    def closeAllResultPanelTabs(self):
        """Close all open result panel tabs"""
        content = dict(
                event = 'closeAllResultPanelTabs'
        )
        return self._sendToFrontEnd(content)
        
    def getAvailableHiPS(self, wavelength=""):
        """Returns available HiPS in ESASky
        No argument for all available HiPS.
        Specify wavelength for those available in that specific wavelength """

        response = requests.get('http://sky.esa.int/esasky-tap/hips-sources')  
        response.raise_for_status()
        HiPSMap = self._parseHiPSJSON(response.text)
        if len(wavelength) > 0:
            if wavelength.upper() in HiPSMap.keys():
                return HiPSMap[wavelength.upper()]
            else:
                print("No wavelength: " + wavelength + " in ESASky")
                print("Available wavelengths are: ")
                print(HiPSMap.keys())
        else:
            return HiPSMap

    def getAvailableHiPSAPI(self, wavelength=""):
        """Returns available HiPS in ESASky
        No argument for all available HiPS.
        Specify wavelength for those available in that specific wavelength """

        content = dict(
                        event='getAvailableHiPS',
                        content = dict(wavelength=wavelength)
        )
        return self._sendAvaitCallback(content)

    def _parseHiPSJSON(self,HiPSJson):
        HiPSJson = json.loads(HiPSJson)
        if 'total' in HiPSJson.keys():
            HiPSMap = dict()
            for i in range(HiPSJson['total']):
                wavelength = HiPSJson['menuEntries'][i]
                wavelengthMap = dict()
                for j in range(wavelength['total']):
                    hips = wavelength['hips'][j]
                    wavelengthMap[hips['surveyName']]=hips
                HiPSMap[wavelength['wavelength']] = wavelengthMap
            return HiPSMap


    def goToRADec(self, ra, dec):
        """Moves the center of the view to the specified coordinate 
        in current coordinate system
        
        Arguments:
        ra -- float or string in sexagesimal or decimal format
        dec -- float or string in sexagesimal or decimal format
        """

        content = dict(
                       event='goToRaDec',
                       content = dict(
                            ra=ra,
                            dec=dec
                       )
                    )
        self._sendToFrontEnd(content)

    def setGoToRADec(self, ra, dec):
        self.goToRADec(ra, dec)

    def goToTargetName(self, targetName):
        """Moves to targetName resolved by SIMBAD"""

        content = dict(
                        event='goToTargetName',
                        content = dict(targetName=targetName)
        )
        self._sendToFrontEnd(content)
        #Add small sleeper to wait for simbad to react
        time.sleep(1)
        
    def setFoV(self, fovDeg):
        """Sets the views Field of View in degrees"""

        content = dict(
                        event='setFov',
                        content = dict(fov=fovDeg)
        )
        self._sendToFrontEnd(content)
        
    def setHiPSColorPalette(self, colorPalette):
        """Sets the colorpalette of the currently active sky to spcified value"""

        content = dict(
                        event='setHipsColorPalette',
                        content = dict(colorPalette=colorPalette)
        )
        self._sendToFrontEnd(content)
        
    def closeJwstPanel(self):
        """Closes the JWST observation planning tool panel"""

        content = dict(
                        event='closeJwstPanel'
        )
        self._sendToFrontEnd(content)
    
    def openJwstPanel(self):
        """Opens the JWST observation planning tool panel"""

        content = dict(
                        event='openJwstPanel'
        )
        self._sendToFrontEnd(content)

    def clearJwstAll(self):
        """Removes all rows in the JWST observation planning tool panel"""
        content = dict(
                        event='clearJwstAll'
        )
        self._sendToFrontEnd(content)

    def addJwst(self, instrument, detector, showAllInstruments):
        """Adds specified instrument and detector to the center of the screen
         for the JWST observation planning tool panel"""

        content = dict(
                        event='addJwst',
                        content = dict(
                            instrument=instrument,
                            detector=detector,
                            showAllInstruments=showAllInstruments
                        )
                        )
        self._sendAvaitCallback(content)

    def addJwstWithCoordinates(self, instrument, detector, showAllInstruments, ra, dec, rotation):
        """Adds specified instrument and detector to the specified coordinate
         for the JWST observation planning tool panel"""
        
        content = dict(
                       event='addJwstWithCoordinates',
                       content = dict(
                            instrument=instrument,
                            detector=detector,
                            showAllInstruments=showAllInstruments,
                            ra=ra,
                            dec=dec,
                            rotation=rotation)
                       )
        self._sendAvaitCallback(content)

    def overlayCatalogue(self, catalogue):
        """Overlays a catalogue created by pyesasky.catalogue in the sky"""

        content = dict(
                       event='overlayCatalogue',
                       content=catalogue.toDict()
                       )
        self._sendToFrontEnd(content)

    def overlayCatalogueWithDetails(self, userCatalogue):
        """Overlays a catalogue created by pyesasky.catalogue
        in the sky and opens a datapanel showing the data"""

        content = dict(
                        event='overlayCatalogueWithDetails',
                        content = dict(userCatalogue.toDict())
                        )
        self._sendToFrontEnd(content)
        
    def clearCatalogue(self, catalogueName):
        """Clears all objects in named visualised catalogue"""

        content = dict(
                        event='clearCatalogue',
                        content = dict(overlayName=catalogueName)
                        )
        self._sendToFrontEnd(content)

    def deleteCatalogue(self, catalogueName):
        """Deletes named visualised cataloge"""

        content = dict(
                        event='deleteCatalogue',
                        content = dict(overlayName=catalogueName)
                        )
        self._sendToFrontEnd(content)
    
    def overlayFootprints(self, footprintSet):
        """Overlays footprints created by pyesasky.footprint in the sky"""

        content = dict(
                        event='overlayFootprints',
                        content = dict(footprintSet.toDict())
                        )
        self._sendToFrontEnd(content)

    def overlayFootprintsWithDetails(self, footprintSet):
        """Overlays footprints created by pyesasky.Footprint in the sky
        and opens a datapanel showing the data"""

        content = dict(
                        event='overlayFootprintsWithDetails',
                        content = dict(footprintSet.toDict())
                        )
        self._sendToFrontEnd(content)

    def clearFootprintsOverlay(self, overlayName):
        """Clears all objects in named visualised footprint table"""
        content = dict(
                        event='clearFootprintsOverlay',
                        content = dict(overlayName=overlayName)
                        )
        self._sendToFrontEnd(content)

    def deleteFootprintsOverlay(self, overlayName):
        """Deletes named visualised footprint table"""

        content = dict(
                        event='deleteFootprintsOverlay',
                        content = dict(overlayName=overlayName)
                        )
        self._sendToFrontEnd(content)

    def overlayFootprintsFromCSV(self, pathToFile, csvDelimiter, footprintSetDescriptor):
        """Overlays footprints read from a csv file"""

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

    def overlayFootprintsFromAstropyTable(self,footprintSetDescriptor, table):
        i = 0

        astropyFootprintSet = FootprintSet(footprintSetDescriptor.getDatasetName(), 'J2000', footprintSetDescriptor.getHistoColor(), footprintSetDescriptor.getLineWidth())
             
        while i < len(table.colnames):
            
            if table.colnames[i] == footprintSetDescriptor.getIdColumnName():
                columnId = table.colnames[i]
                print('{id} mapped to '+columnId)
                if footprintSetDescriptor.getIdColumnName() == footprintSetDescriptor.getNameColumnName():
                    columnName = columnId
                    print('{name} mapped to '+columnName)
            elif table.colnames[i] == footprintSetDescriptor.getNameColumnName():
                columnName = table.colnames[i]
                print('{name} mapped to '+columnName)
            elif table.colnames[i] == footprintSetDescriptor.getStcsColumnName():
                columnStcs = table.colnames[i]
                print('{stcs} mapped to '+columnStcs)
            elif table.colnames[i] == footprintSetDescriptor.getCentralRADegColumnName():
                columnRaDeg = table.colnames[i]
                print('{centerRaDeg} mapped to '+columnRaDeg)
            elif table.colnames[i] == footprintSetDescriptor.getCentralDecDegColumnName():
                columnDecDeg = table.colnames[i]
                print('{centerDecDeg} mapped to '+columnDecDeg)
            i += 1
        
        j = 0
        currId = j
        
        while j < len(table):
            currDetails = []
            k = 0
            while k < len(table.colnames):
                currMetadata = {}
                colName = table.colnames[k]
                if type(table[j][k]) == bytes:
                    currValue = str(table[j][k].decode("utf-8"))
                else:
                    currValue = str(table[j][k])
                currRaDeg = []
                currDecDeg = []

                if colName == footprintSetDescriptor.getNameColumnName():
                    currName = currValue
                elif colName == footprintSetDescriptor.getStcsColumnName():
                    currStcs = currValue
                elif colName == footprintSetDescriptor.getCentralRADegColumnName():
                    currRaDeg = currValue
                elif colName == footprintSetDescriptor.getCentralDecDegColumnName():
                    currDecDeg = currValue
                else:
                    currMetadata = {}
                    found = False
                    if len(footprintSetDescriptor.getMetadata()) > 0:
                        l = 0
                        while l < len(footprintSetDescriptor.getMetadata()):
                            if footprintSetDescriptor.getMetadata()[j].getLabel() == colName:
                                found = True
                                currMetadata['name'] = footprintSetDescriptor.getMetadata()[j].getLabel()
                                currMetadata['value'] = currValue
                                currMetadata['type'] = footprintSetDescriptor.getMetadata()[j].getType()

                                break
                            l += 1
                    elif not found:
                        currMetadata['name'] = colName
                        currMetadata['value'] = currValue
                        currMetadata['type'] = MetadataType.STRING

                    currDetails.append(currMetadata)
                k += 1

            j += 1
            astropyFootprintSet.addFootprint(currName, currStcs, currId, currRaDeg, currDecDeg, currDetails)
                    
        print(f'Processed {j} lines.')
        self.overlayFootprintsWithDetails(astropyFootprintSet)

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
                if type(table[j][k]) == bytes:
                    currValue = str(table[j][k].decode("utf-8"))
                else:
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
        """Overlays catalogue read from a csv file"""

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

    def overlayMOC(self, mocObject, name ='MOC', color = '', opacity = 0.2 ):
        """Overlay HealPix Multi-Order Coverage map"""
        mocString = '{'
        if isinstance(mocObject, dict):
            for order in mocObject.keys():
                mocString += '\"' + order + '\":['
                for val in mocObject[order]:
                    if '-' in str(val):
                        start = int(val.split('-')[0])
                        end = int(val.split('-')[1])
                        for i in range(start,end+1):
                            mocString += str(i) + ","
                    else:
                        mocString += str(val) + ","
                mocString = mocString[:-1] + "],"

            mocString = mocString[:-1] + "}"
        elif '/' in mocObject:
            currOrder = ''
            for currVal in mocObject.split(' '):
                if '/' in currVal:
                    if currOrder != '':
                        mocString = mocString[:-1] + "],"
                    currOrder = currVal.split('/')[0]
                    mocString += '\"' + currOrder + '\":['
                    currVal = currVal.split('/')[1] 
                
                if '-' in str(currVal):
                    start = int(currVal.split('-')[0])
                    end = int(currVal.split('-')[1])
                    for i in range(start,end+1):
                        mocString += str(i) + ","
                else:
                    mocString += str(currVal) + ","
            mocString = mocString[:-1] + "]}"
        else:
            mocString = mocObject
        content = dict(
                event = 'addMOC',
                content = dict(
                    options="{\"color\":\"" + color + "\","
                                + "\"opacity\":\"" + str(opacity) + "\"}",
                    mocData = mocString,
                    name = name
                )
        )
        self._sendToFrontEnd(content)

    def removeMOC(self, name ='MOC'):
        content = dict(
                event = 'removeMOC',
                content = dict(name=name)
        )
        return self._sendToFrontEnd(content)

    def checkExtTapAvailability(self, tapService):
        """Returns the 1 if any data is availabe otherwise 0"""

        content = dict(
                event = 'extTapCount',
                content = dict(tapService=tapService)
        )
        return self._sendAvaitCallback(content)

    def getExtTapData(self, tapService):
        """Calls the external tap and try to recieve data in the current view"""

        content = dict(
                event = 'extTap',
                content = dict(tapService=tapService)
        )
        return self._sendAvaitCallback(content)
   
    def getExtTapDataWithDetails(self, tapServiceName, tapUrl, tapTable, adql):
        """Calls the external tap and try to recieve data in the current view"""

        content = dict(
                event = 'newExtTapService',
                content = dict(
                    name = tapServiceName,
                    tapUrl = tapUrl,
                    tapTable = tapTable,
                    adql = adql
                    )
        )
        return self._sendAvaitCallback(content)

    def _readProperties(self, url):
        config = configparser.RawConfigParser(strict=False)
        if not url.startswith('http'):
            text = "[Dummy section]\n"
            try:
                with open(url+"properties", 'r') as f:
                    text += f.read() + "\n"
                config.read_string(text)
                return config
            except FileNotFoundError as fnf_error:
                print(url + " not found or missing properties file.\n Did you mean http://" + url)
                raise(fnf_error)
        else:   
            response = requests.get(url+"properties")
            response.raise_for_status()
            text = "[Dummy section]\n"+response.text
            config.read_string(text)
            return config

    def openSkyPanel(self):
        """Opens the sky selector panel"""
        content = dict(
                    event = 'openSkyPanel'
                    )
        self._sendToFrontEnd(content)   

    def closeSkyPanel(self):
        """Closes the sky selector panel"""
        content = dict(
                    event = 'closeSkyPanel'
                    )
        self._sendToFrontEnd(content)     

    def getNumberOfSkyRows(self):
        """Returns the number of rows in the sky panel """
        content = dict(
                    event = 'getNumberOfSkyRows'
                    )
        return self._sendAvaitCallback(content)   

    def removeHiPS(self, index = -1):
        """Removes HiPS row in the skypanel either at "index"
        or no argument for all except the first"""
        content = dict(
                    event = 'removeHips',
                    content = dict(index = index)
                    )
        self._sendAvaitCallback(content)   
    
    def setHiPSSliderValue(self, value):
        """Sets the value of the HiPS slider to fade between
        the HiPS in the skypanel.
        Valid values are 0 to nSkyRows - 1 """
        content = dict(
                    event = 'setHipsSliderValue',
                    content = dict(value = value)
                    )
        self._sendToFrontEnd(content)    

    def addLocalHiPS(self, hipsURL):
        """Starts a tornado server which will supply the widget with
        HiPS from a local source on client machine"""
        if not hasattr(self, 'tornadoServer'):
            self.startTornado()
        drive, tail = os.path.splitdrive(hipsURL)
        if drive:
            #Windows
            url = tail.replace("\\","/") 
        else:
            url = hipsURL
        patternUrl = url + "(.*)"
        self.tornadoServer.add_handlers(r"localhost",[(str(patternUrl),self.FileHandler,dict(baseUrl=hipsURL))])
        return url

    def setHiPS(self, hipsName, hipsURL='default'):
        """Sets the currently active row in the skypanel to either
        hipsName already existing in ESASky or adds a new name from specified URL         
         """
        if hipsURL != 'default':
            userHiPS = self.parseHiPSURL(hipsName, hipsURL)
            content = dict(
                        event='changeHipsWithParams',
                        content = dict(userHiPS.toDict())
                        )
            self._sendToFrontEnd(content)
        else:
            content = dict(
                        event='changeHips',
                        content = dict(hipsName=hipsName)
                        )
            return self._sendAvaitCallback(content)
    
    def addHiPS(self, hipsName, hipsURL='default'):
        """Adds a new row win the skypanel witheither
        hipsName already existing in ESASky or adds a new name from specified URL  """
        if hipsURL != 'default':
            userHiPS = self.parseHiPSURL(hipsName, hipsURL)
            content = dict(
                        event='addHipsWithParams',
                        content = dict(userHiPS.toDict())
                        )
            self._sendToFrontEnd(content)
        else:
            content = dict(
                        event='addHips',
                        content = dict(hipsName = hipsName)
                        )
            return self._sendAvaitCallback(content)

    def parseHiPSURL(self, hipsName, hipsURL):
        if not hipsURL.endswith("/"):
            hipsURL += '/'
        config = self._readProperties(hipsURL)
        if not hipsURL.startswith('http'):
            url = self.addLocalHiPS(hipsURL)
            port= self.httpServerPort
            hipsURL = 'http://localhost:' + str(port) + url 

        maxNorder = config.get('Dummy section','hips_order')
        imgFormat = config.get('Dummy section','hips_tile_format').split()
        cooFrame = config.get('Dummy section','hips_frame')
        if cooFrame == 'equatorial':
            cooFrame = 'J2000'
        else:
            cooFrame = 'Galactic'
        userHiPS = HiPS(hipsName, hipsURL, cooFrame, maxNorder, imgFormat[0])
        print('hipsURL '+ hipsURL)
        print('imgFormat '+imgFormat[0])
        return userHiPS

    def startTornado(self):
        class DummyHandler(tornado.web.RequestHandler):
            pass

        app = tornado.web.Application([
            tornado.web.url(r"dummy", DummyHandler),
        ])
        #pool = ThreadPoolExecutor(max_workers=2)
        #loop = tornado.ioloop.IOLoop()
        server = tornado.httpserver.HTTPServer(app)
        portStart = 8900
        portEnd = 8910
        for port in range(portStart,portEnd+1):
            try:
                server.listen(port)
            except OSError as os_error:
                if port is portEnd:
                    raise(os_error)
            else:
                break
        #fut = pool.submit(loop.start)

        self.httpserver = server
        self.tornadoServer = app
        self.httpServerPort = port

    class FileHandler(tornado.web.RequestHandler):
        def initialize(self, baseUrl):
            self.baseUrl = baseUrl
        
        def set_default_headers(self):
            self.set_header("Access-Control-Allow-Origin", "*")
        
        def get(self, path):
            host=self.request.host
            origin = host.split(':')[0]
            if not origin == 'localhost':
                raise tornado.web.HTTPError(status_code=403)
            file_location = os.path.abspath(os.path.join(self.baseUrl, path))
            if not os.path.isfile(file_location):
                raise tornado.web.HTTPError(status_code=404)
            with open(file_location, "rb") as source_file:
                self.write(source_file.read())


    """ External TAP Services"""

    def getAvailableTapServices(self):
        """Returns the available predefined External TAP Services in ESASky"""

        content = dict(
                        event='getAvailableTapServices'
                        )
        return self._sendAvaitCallback(content)
    
    def getAllAvailableTapMissions(self):
        """Returns all the missions and dataproducts from the available predefined
         External TAP Services in ESASky"""

        content = dict(
                        event='getAllAvailableTapMissions'
                        )
        return self._sendAvaitCallback(content)
   
    def getTapADQL(self, tapServiceName):
        """Returns the adql that will be run on this tapService"""

        content = dict(
                        event='getTapADQL',
                        content = dict(
                            tapService = tapServiceName
                        ))
        return self._sendAvaitCallback(content)

    def getTapServiceCount(self, tapServiceName= ''):
        """Returns the available data in the current sky for the named tapService"""

        content = dict(
                        event='getTapServiceCount',
                        content = dict(
                            tapService = tapServiceName
                        ))
        return self._sendAvaitCallback(content)
    
    def plotTapService(self, tapServiceName):
        """Plots data from selected mission in the an external TAP service"""

        content = dict(
                        event='plotTapService',
                        content = dict(
                            tapService = tapServiceName
                        ))
        return self._sendAvaitCallback(content)

    def plotTapServiceWithDetails(self, name, tapUrl, ADQL, dataOnlyInView = True, color = "", limit = -1, ):
        """Searches and plots data from specified TAP service
       
        Arguments:
        name -- (String) Name that will be shown on the screen 
        tapUrl -- (String) URL to the tap service
        ADQL -- (String) The ADQL that will be used for retrieving the data
        dataOnlyInView -- (Boolean, default:True) Adds a WHERE statement to only retrieve data in the current view
        color -- (String, default: preset list) Color for display in RGB format (e.g. #FF0000 for red)
        limit -- (Int, default: 3000) Limit for amount of results to display        
        """

        content = dict(
                        event='plotTapServiceWithDetails',
                        content = dict(
                            name = name,
                            tapUrl = tapUrl,
                            dataOnlyInView = dataOnlyInView,
                            adql = ADQL,
                            color = color,
                            limit = limit
                        ))
        self._sendToFrontEnd(content)
