import ipywidgets as widgets
from traitlets import Unicode, default, Float, Dict
import requests
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

#New stuff
import time
import logging
import sys
import asyncio
from tornado.queues import PriorityQueue, QueueEmpty
from tornado import gen
from zmq import POLLIN
from itertools import count

__all__ = ['ESASkyWidget']
    
class ESASkyWidget(widgets.DOMWidget):

    _view_name = Unicode('ESASkyJSView').tag(sync=True)
    _model_name = Unicode('ESASkyJSModel').tag(sync=True)
    _view_module = Unicode('pyesasky').tag(sync=True)
    _model_module = Unicode('pyesasky').tag(sync=True)
    _view_module_version = Unicode('1.0.1').tag(sync=True)
    _model_module_version = Unicode('1.0.1').tag(sync=True)
    
    def __init__(self):
        super().__init__()
        self.messageTimeOut=10.0 #s
        self.msgId = 0
        self.guiReady = False
        self.guiReadyCallSent = False
        
    def waitGuiReady(self):
        self.guiReadyCallSent = True
        while True:
                content = dict(event='initTest')
                self.send(content)
                time.sleep(1)
                val = self.loopMessageQueue()
                print(val)
                if val is not None:
                    self.guiReady = True
                    return val

    @default('layout')
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    def send(self,content):
        if not (self.guiReady or self.guiReadyCallSent):
            self.waitGuiReady()
        content['origin'] = 'pyesasky'
        self.msgId += 1
        content['msgId'] = self.msgId
        super().send(content)

    def _sendAvaitCallback(self,content):
        self.send(content)
        startTime = time.time()
        while time.time()-startTime<self.messageTimeOut:
            val = self.loopMessageQueue()
            if val is not None:
                return val
            time.sleep(0.1)
        print("Request timed out")
        return None

    def loopMessageQueue(self):
        for stream in self.comm.kernel.shell_streams:
            stream.flush()
        for item in self.comm.kernel.msg_queue._queue:
            try:
                msg = item[3][1][6]
                msg = json.loads(str(msg))
                if int(msg['data']['content']['msgId']) == self.msgId:
                    self.comm.kernel.msg_queue._queue.remove(item)
                    self.comm.kernel.msg_queue.task_done()
                    return msg['data']['content']['values']
            except:
                    pass

    def getCenter(self,cooFrame = 'J2000'):
        if cooFrame not in ['J2000','GALACTIC']:
            print('Coordinate frame must be J2000 or GALACTIC')
            return
        content = dict(
                        event='getCenter',
                        cooFrame=cooFrame
        )
        return self._sendAvaitCallback(content)

    def getAvailableHiPSAPI(self, wavelength=""):
        content = dict(
                        event='getAvailableHiPS',
                        wavelength=wavelength
        )
        return self._sendAvaitCallback(content)

    def plotObservations(self, missionId):
        content = dict(
                event = 'plotObservations',
                missionId=missionId
        )
        return self._sendAvaitCallback(content)

    def plotCatalogues(self, missionId):
        content = dict(
                event = 'plotCatalogues',
                missionId=missionId
        )
        return self._sendAvaitCallback(content)

    def plotSpectra(self, missionId):
        content = dict(
                event = 'plotSpectra',
                missionId=missionId
        )
        return self._sendAvaitCallback(content)
    
    def getObservationsCount(self):
        content = dict(
                event = 'getObservationsCount'
        )
        return self._sendAvaitCallback(content)

    def getCataloguesCount(self):
        content = dict(
                event = 'getCataloguesCount'
        )
        return self._sendAvaitCallback(content)

    def getSpectraCount(self):
        content = dict(
                event = 'getSpectraCount'
        )
        return self._sendAvaitCallback(content)

    def getPublicationsCount(self):
        content = dict(
                event = 'getPublicationsCount'
        )
        return self._sendAvaitCallback(content)


    def getResultPanelData(self):
        content = dict(
                event = 'getResultPanelData'
        )
        return self._sendAvaitCallback(content)
        
    def getAvailableHiPS(self, wavelength=""):
        response = requests.get('http://sky.esa.int/esasky-tap/hips-sources')  
        response.raise_for_status()
        HiPSMap = self.parseHiPSJSON(response.text)
        if len(wavelength) > 0:
            if wavelength.upper() in HiPSMap.keys():
                return HiPSMap[wavelength.upper()]
            else:
                print("No wavelength: " + wavelength + " in ESASky")
                print("Available wavelengths are: ")
                print(HiPSMap.keys())
        else:
            return HiPSMap

    def parseHiPSJSON(self,HiPSJson):
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


    def setGoToRADec(self, ra, dec):
        content = dict(
                       event='goToRADec',
                       ra=ra,
                       dec=dec
                )
        self.send(content)

    def goToTargetName(self, targetname):
        self._targetname = targetname 
        content = dict(
                        event='goToTargetName',
                        targetname=targetname
        )
        self.send(content)
        
    def setFoV(self, fovDeg):
        self._fovDeg = fovDeg
        content = dict(
                        event='setFoV',
                        fovDeg=fovDeg
        )
        self.send(content)
        
    def setHiPSColorPalette(self, colorPalette):
        self._colorPalette = colorPalette
        content = dict(
                        event='setHiPSColorPalette',
                        colorPalette=colorPalette
        )
        self.send(content)
        
    def closeJwstPanel(self):
        content = dict(
                        event='closeJwstPanel'
        )
        self.send(content)
    
    def openJwstPanel(self):
        content = dict(
                        event='openJwstPanel'
        )
        self.send(content)

    def addJwst(self, instrument, detector, showAllInstruments):
        content = dict(
                        event='addJwst',
                        instrument=instrument,
                        detector=detector,
                        showAllInstruments=showAllInstruments
                        )
        self.send(content)

    def clearJwstAll(self):
        content = dict(
                        event='clearJwstAll'
        )
        self.send(content)

    def addJwstWithCoordinates(self, instrument, detector, showAllInstruments, ra, dec, rotation):
        
        content = dict(
                       event='addJwstWithCoordinates',
                       instrument=instrument,
                       detector=detector,
                       showAllInstruments=showAllInstruments,
                       ra=ra,
                       dec=dec,
                       rotation=rotation
                       )
        self.send(content)

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
    
    # def getAvailableHiPS(self, wavelength):
    #     content = dict(
    #                     event='getAvailableHiPS',
    #                     )
    #     print(self.send(content))
        
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

    def addLocalHiPS(self, hipsURL):
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
        if hipsURL != 'default':
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
            print('hipsURL '+hipsURL)
            print('imgFormat '+imgFormat[0])
            content = dict(
                        event='changeHiPSWithParams',
                        content=userHiPS.toDict()
                        )
            self.send(content)
        else:
            content = dict(
                        event='changeHiPS',
                        content=hipsName
                        )
            return self._sendAvaitCallback(content)

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
