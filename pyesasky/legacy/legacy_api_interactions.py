from pyesasky.legacy.legacy_utils import deprecated


class LApiInteractionsMixin:

    @deprecated("show_coo_grid")
    def showCoordinateGrid(self, show=True):
        pass

    @deprecated("get_center")
    def getCenter(self, cooFrame="J2000"):
        pass

    @deprecated("plot_obs")
    def plotObservations(self, missionId):
        pass

    @deprecated("plot_cat")
    def plotCatalogues(self, missionId):
        pass

    @deprecated("plot_spec")
    def plotSpectra(self, missionId):
        pass

    @deprecated("cs_obs")
    def coneSearchObservations(self, missionId, ra, dec, radius):
        pass

    @deprecated("cs_cat")
    def coneSearchCatalogues(self, missionId, ra, dec, radius):
        pass

    @deprecated("cs_spec")
    def coneSearchSpectra(self, missionId, ra, dec, radius):
        pass

    @deprecated("get_obs_count")
    def getObservationsCount(self):
        pass

    @deprecated("get_cat_count")
    def getCataloguesCount(self):
        pass

    @deprecated("get_pub_count")
    def getPublicationsCount(self):
        pass

    @deprecated("get_spec_count")
    def getSpectraCount(self):
        pass

    @deprecated("get_result_data")
    def getResultPanelData(self):
        pass

    @deprecated("close_result_tab")
    def closeResultPanelTab(self, index=-1):
        pass

    @deprecated("close_result")
    def closeAllResultPanelTabs(self):
        pass

    @deprecated("get_available_public_hips")
    def getAvailableHiPS(self, wavelength=""):
        pass

    @deprecated("get_available_hips")
    def getAvailableHiPSAPI(self, wavelength=""):
        pass

    @deprecated("go_to")
    def goToRADec(self, ra, dec):
        pass

    @deprecated("go_to")
    def setGoToRADec(self, ra, dec):
        pass

    @deprecated("go_to_target")
    def goToTargetName(self, targetName):
        pass

    @deprecated("set_fov")
    def setFoV(self, fovDeg):
        pass

    @deprecated("set_hips_color")
    def setHiPSColorPalette(self, colorPalette):
        pass

    @deprecated("close_jwst")
    def closeJwstPanel(self):
        pass

    @deprecated("open_jwst")
    def openJwstPanel(self):
        pass

    @deprecated("clear_jwst")
    def clearJwstAll(self):
        pass

    @deprecated("add_jwst")
    def addJwst(self, instrument, detector, showAllInstruments):
        pass

    @deprecated("add_jwst")
    def addJwstWithCoordinates(
        self, instrument, detector, showAllInstruments, ra, dec, rotation
    ):
        pass

    @deprecated("overlay_cat")
    def overlayCatalogue(self, catalogue):
        pass

    @deprecated("overlay_cat")
    def overlayCatalogueWithDetails(self, userCatalogue):
        pass

    @deprecated("clear_cat")
    def clearCatalogue(self, catalogueName):
        pass

    @deprecated("delete_cat")
    def deleteCatalogue(self, catalogueName):
        pass

    @deprecated("overlay_footprints")
    def overlayFootprints(self, footprintSet):
        pass

    @deprecated("overlay_footprints")
    def overlayFootprintsWithDetails(self, footprintSet):
        pass

    @deprecated("clear_footprints")
    def clearFootprintsOverlay(self, overlayName):
        pass

    @deprecated("delete_footprints")
    def deleteFootprintsOverlay(self, overlayName):
        pass

    @deprecated("overlay_footprints_csv")
    def overlayFootprintsFromCSV(
        self, pathToFile, csvDelimiter, footprintSetDescriptor
    ):
        pass

    @deprecated("overlay_footprints_astropy")
    def overlayFootprintsFromAstropyTable(self, footprintSetDescriptor, table):
        pass

    @deprecated("overlay_cat_astropy")
    def overlayCatalogueFromAstropyTable(
        self,
        catalogueName,
        cooFrame,
        color,
        lineWidth,
        table,
        raColName,
        decColName,
        mainIdColName,
    ):
        pass

    @deprecated("overlay_cat_csv")
    def overlayCatalogueFromCSV(
        self, pathToFile, csvDelimiter, catalogueDescriptor, cooFrame
    ):
        pass

    @deprecated("overlay_moc")
    def overlayMOC(self, mocObject, name="MOC", color="", opacity=0.2, mode="healpix"):
        pass

    @deprecated("remove_moc")
    def removeMOC(self, name="MOC"):
        pass

    @deprecated("open_sky_panel")
    def openSkyPanel(self):
        pass

    @deprecated("close_sky_panel")
    def closeSkyPanel(self):
        pass

    @deprecated("get_sky_row_count")
    def getNumberOfSkyRows(self):
        pass

    @deprecated("remove_hips")
    def removeHiPS(self, index=-1):
        pass

    @deprecated("set_hips_slider")
    def setHiPSSliderValue(self, value):
        pass

    @deprecated("add_hips_local")
    def addLocalHiPS(self, hipsURL):
        pass

    @deprecated("select_hips")
    def setHiPS(self, hipsName, hipsURL="default"):
        pass

    @deprecated("add_hips")
    def addHiPS(self, hipsName, hipsURL="default"):
        pass

    @deprecated("browse_hips")
    def browseHips(self):
        pass

    @deprecated("get_tap_services")
    def getAvailableTapServices(self):
        pass

    @deprecated("get_tap_missions")
    def getAllAvailableTapMissions(self):
        pass

    @deprecated("get_tap_query")
    def getTapADQL(self, tapServiceName):
        pass

    @deprecated("get_tap_count")
    def getTapServiceCount(self, tapServiceName=""):
        pass

    @deprecated("plot_tap")
    def plotTapService(self, tapServiceName):
        pass

    @deprecated("plot_custom_tap")
    def plotTapServiceWithDetails(
        self,
        name,
        tapUrl,
        ADQL,
        dataOnlyInView=True,
        color="",
        limit=-1,
    ):
        pass

    @deprecated("save_session")
    def saveSession(self, fileName=None):
        pass

    @deprecated("restore_session_file")
    def restoreSessionFromFile(self, fileName):
        pass

    @deprecated("restore_session_obj")
    def restoreSessionFromDict(self, session):
        pass

    @deprecated("get_gw_ids")
    def getGWIds(self):
        pass

    @deprecated("get_gw_data")
    def getGWData(self):
        pass

    @deprecated("get_neutorino_data")
    def getNeutrinoEventData(self):
        pass

    @deprecated("show_gw_event")
    def showGWEvent(self, id: str):
        pass

    @deprecated("open_neutorino_panel")
    def openNeutrinoPanel(self):
        pass

    @deprecated("open_gw_panel")
    def openGWPanel(self):
        pass

    @deprecated("close_event_panel")
    def closeAlertPanel(self):
        pass

    @deprecated("open_search_panel")
    def showSearchToolPanel(self):
        pass

    @deprecated("close_search_panel")
    def closeSearchToolPanel(self):
        pass

    @deprecated("cone_search")
    def setConeSearchArea(self, ra, dec, radius):
        pass

    @deprecated("poly_search")
    def setPolygonSearchArea(self, stcs):
        pass

    @deprecated("clear_search")
    def clearSearchArea(self):
        pass
