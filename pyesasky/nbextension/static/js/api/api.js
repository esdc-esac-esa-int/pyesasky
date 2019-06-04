var ESASkyAPI = null;

function ESASkyAPIConstructor() {

	this.goTo = function(ra, dec) {
		//@esac.archive.esasky.cl.web.client.api.Api::goTo(Ljava/lang/String;Ljava/lang/String;)(ra, dec);
		this.goToAPI(ra, dec);
	};

	this.goToWithParams = function(ra, dec, fovDegrees, showTargetPointer, cooFrame) {
        this.goToWithParamsAPI(ra, dec, fovDegrees, showTargetPointer, cooFrame);
    };

	this.goToTargetName = function(targetName) {
        this.goToTargetNameAPI(targetName);
    };

    this.goToTargetNameWithFoV = function(targetName, fovDeg) {
        this.goToTargetNameWithFoVAPI(targetName, fovDeg);
    };

	this.setFoV = function(fovDegrees) {
		this.setFoVAPI(fovDegrees);
	};
	
	this.setHiPS = function(surveyId){
		this.setHiPSAPI(surveyId);
	};

	this.setHiPSWithParams = function(surveyId, surveyName, surveyRootUrl,
			surveyFrame, maximumNorder, imgFormat) {
		this.setHiPSWithParamsAPI(surveyId, surveyName, surveyRootUrl,
				surveyFrame, maximumNorder, imgFormat);
	};

	this.setHiPSColorPalette = function(colorPalette) {
		this.setHiPSColorPaletteAPI(colorPalette);
	};

	this.overlayCatalogue = function(catalogueJSON){
		this.overlayCatalogueAPI(catalogueJSON);
	};

	this.clearCatalogue = function(catalogueName){
		this.clearCatalogueAPI(catalogueName);
	};

	this.removeCatalogue = function(catalogueName){
		this.removeCatalogueAPI(catalogueName);
	};

	this.overlayFootprints = function(footprintsSetJSON){
		this.overlayFootprintsAPI(footprintsSetJSON);
	};
	
	this.overlayFootprintsWithData = function(footprintsSetJSON){
		this.overlayFootprintsWithDataAPI(footprintsSetJSON);
	};
	
	this.overlayCatalogueWithData = function(userCatalogueJSON){
		this.overlayCatalogueWithDataAPI(userCatalogueJSON);
	};
	
	this.getAvailableHiPS = function(wavelength){
		return this.getAvailableHiPSAPI(wavelength);
	};

	this.addJwstWithCoordinates = function(instrument, detector, allInstruments, ra, dec, rotation){
		return this.addJwstWithCoordinatesAPI(instrument, detector, allInstruments, ra, dec, rotation);
	};

	this.addJwst = function(instrument, detector, allInstruments){
		return this.addJwstAPI(instrument, detector, allInstruments);
	};

	this.closeJwstPanel = function(){
		return this.closeJwstPanelAPI();
	};

	this.openJwstPanel = function(){
		return this.openJwstPanelAPI();
	};
	
	this.clearJwst = function(){
		return this.clearJwstAPI();
	};
	
	
}

function JavaApiReady() {
	ESASkyAPI = new ESASkyAPIConstructor();
}

// CALL FROM PYTHON EXAMPLE
// ESASkyAPI.goTo("10","+26");
//
// ESASkyAPI.setFoV(40);
//
// ESASkyAPI.setHiPSWithParams("Planck LFI 030 GHz Pol smoothed", "Planck LFI 030 GHz Pol smoothed", "http://skies.esac.esa.int/pla/LFI_SkyMap_030_1024_R3_00_full_smooth_HiPS/", "Galactic", 3, "png");
//
// ESASkyAPI.setHiPSColorPalette("PLANCK");
//
// ESASkyAPI.goToTargetName("M51");
//
// ESASkyAPI.goToWithParams("10", "-25", 10.3, true, "Equatorial"); // some problem with Galactic
//
// ESASkyAPI.goToTargetNameWithFoV("M1", 10);
//
//
//var catalogueJSON = "{
//	\"catalogue\": {
//		\"catalogueName\": \"bla bla bla\",
//		\"cooframe\": \"equatorial\",
//		\"color\":\"#ee2345\",
//		\"lineWidth\":10,
//		\"coords\": [
//			{
//				\"name\": \"A\",
//				\"ra\": \"105.69239256\",
//				\"dec\": \"-8.45235969\"
//			},{
//				\"name\": \"B\",
//				\"ra\": \"105.70779763\",
//				\"dec\": \"-8.31350997\"
//			},{
//				\"name\": \"C\",
//				\"ra\": \"105.74242906\",
//				\"dec\": \"-8.34776709\"
//			}
//		]
//	}
//}";
//ESASkyAPI.overlayCatalogue("{\"catalogue\":{\"catalogueName\": \"bla bla bla\",\"cooframe\": \"equatorial\",\"color\":\"#ee2345\",\"lineWidth\":10,\"sources\": [{\"name\": \"A\",\"ra\": \"105.69239256\",\"dec\": \"-8.45235969\"},{\"name\": \"B\",\"ra\": \"105.70779763\",\"dec\": \"-8.31350997\"},{\"name\": \"C\",\"ra\": \"105.74242906\",\"dec\": \"-8.34776709\"}]}}");
//ESASkyAPI.overlayFootprints("{\"footprintsSet\":{\"overlayName\":\"test footprint\",\"cooframe\":\"J2000\",\"color\":\"red\",\"lineWidth\":5,\"footprints\":[{\"name\":\"0748010101\",\"id\":1,\"stcs\":\"Polygon J2000 53.426365 -9.619576 53.300158 -9.702947 53.167147 -9.69405 53.08263 -9.650685 53.016188 -9.57398 52.986966 -9.478405 53.00723 -9.495086 52.988101 -9.467295 52.991509 -9.430631 53.038887 -9.315109 53.153757 -9.236272 53.241561 -9.225175 53.327115 -9.244057 53.376637 -9.215155 53.436342 -9.305129 53.425089 -9.317356 53.440849 -9.311793 53.499461 -9.400646 53.470193 -9.423998 53.46799 -9.503998\"},{\"name\":\"0780240101\",\"id\":2,\"stcs\":\"Polygon J2000 53.394905 -9.626175 53.300255 -9.679547 53.221356 -9.690672 53.139074 -9.676222 53.041038 -9.623969 52.978018 -9.487269 52.997232 -9.380614 53.052461 -9.272865 53.193189 -9.20623 53.323768 -9.232877 53.399219 -9.286176 53.453319 -9.368363 53.470293 -9.473906 53.453378 -9.448363 53.46805 -9.486129 53.451193 -9.542808 Polygon J2000  53.350899 -9.499531 53.272006 -9.330667 53.18868 -9.370673 53.17742 -9.352895 53.18305 -9.372895 53.103082 -9.41066 53.180784 -9.579562 Polygon J2000  53.270904 -9.451778 53.204447 -9.481785 53.172911 -9.415117 53.240484 -9.384005 Polygon J2000  53.17742 -9.350673 53.140274 -9.274002 53.138022 -9.274002 53.175168 -9.350673\"}]}}");
//ESASkyAPI.overlayFootprintsWithData("{\"footprintsSet\":{\"overlayName\":\"test footprint\",\"cooframe\":\"J2000\",\"color\":\"red\",\"lineWidth\":5,\"footprints\":[{\"name\":\"0748010101\",\"id\":1,\"stcs\":\"Polygon J2000 53.426365 -9.619576 53.300158 -9.702947 53.167147 -9.69405 53.08263 -9.650685 53.016188 -9.57398 52.986966 -9.478405 53.00723 -9.495086 52.988101 -9.467295 52.991509 -9.430631 53.038887 -9.315109 53.153757 -9.236272 53.241561 -9.225175 53.327115 -9.244057 53.376637 -9.215155 53.436342 -9.305129 53.425089 -9.317356 53.440849 -9.311793 53.499461 -9.400646 53.470193 -9.423998 53.46799 -9.503998\",\"data\":[{\"name\": \"meta1\",\"value\": \"obs 1\",\"type\": \"STRING\"},{\"name\": \"score\",\"value\": \"3\",\"type\": \"STRING\"}]},{\"name\":\"0780240101\",\"id\":2,\"stcs\":\"Polygon J2000 53.394905 -9.626175 53.300255 -9.679547 53.221356 -9.690672 53.139074 -9.676222 53.041038 -9.623969 52.978018 -9.487269 52.997232 -9.380614 53.052461 -9.272865 53.193189 -9.20623 53.323768 -9.232877 53.399219 -9.286176 53.453319 -9.368363 53.470293 -9.473906 53.453378 -9.448363 53.46805 -9.486129 53.451193 -9.542808 Polygon J2000  53.350899 -9.499531 53.272006 -9.330667 53.18868 -9.370673 53.17742 -9.352895 53.18305 -9.372895 53.103082 -9.41066 53.180784 -9.579562 Polygon J2000  53.270904 -9.451778 53.204447 -9.481785 53.172911 -9.415117 53.240484 -9.384005 Polygon J2000  53.17742 -9.350673 53.140274 -9.274002 53.138022 -9.274002 53.175168 -9.350673\",\"data\":[{\"name\": \"meta1\",\"value\": \"obs 2\",\"type\": \"STRING\"},{\"name\": \"score\",\"value\": \"5\",\"type\": \"STRING\"}]}]}}");

