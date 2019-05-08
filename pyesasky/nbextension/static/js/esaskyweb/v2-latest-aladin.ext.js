/**
 * @author fgiordano
 * The following functions do override the CDS original ones
 * since there is a bug in their code which avoid to display
 * JPEG on top.
 */

// @API
/*
 * Creates remotely a HiPS from a FITS image URL and displays it
 */
Aladin.prototype.displayFITS = function(url, options, aladin, fov) {
    options = options || {};
    var data = {url: url};
    if (options.color) {
        data.color = true;
    }
    if (options.outputFormat) {
        data.format = options.outputFormat;
    }
    if (options.order) {
        data.order = options.order;
    }
    if (options.nocache) {
        data.nocache = options.nocache;
    }
    $.ajax({
        url: 'http://alasky.u-strasbg.fr/cgi/fits2HiPS',
        data: data,
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            if (response.status!='success') {
                alert('An error occured: ' + response.message);
                return;
            }
            var label = options.label || "FITS image";
            
            aladin.setOverlayImageLayer(aladin.createImageSurvey(label, label, response.data.url, "equatorial", response.data.meta.max_norder, {imgFormat: 'png'}));
            if (fov !== null){
            	aladin.setFoV(fov);
            }else{
            	aladin.setFoV(response.data.meta.fov);	
            }
            aladin.gotoRaDec(response.data.meta.ra, response.data.meta.dec);
            var transparency = (options && options.transparency) || 1.0;
            aladin.getOverlayImageLayer().setAlpha(transparency);

        }
    });

};

// @API
/*
 * Creates remotely a HiPS from a JPEG or PNG image with astrometry info
 * and display it
 */
Aladin.prototype.displayJPG = Aladin.prototype.displayPNG = function(url, aladin, options, fov) {
    options = options || {};
    options.color = true;
    options.label = "JPG/PNG image";
    options.outputFormat = 'png';
    this.displayFITS(url, options, aladin, fov);
};



//document.getElementById("#aladin-div-1").onclick=function(){console.log("eccolo")};

//$(aladin.view.reticleCanvas).addEventListener('mousedown', function(e) {
//  var mouse = myState.getMouse(e);
//  var mx = mouse.x;
//  var my = mouse.y;
//  console.log("MX: "+mx+" MY: "+my);
//}, true);
//A.aladin.view.catalogCanvas.addEventListener('mousedown', function(e) {
//    var mouse = myState.getMouse(e);
//    var mx = mouse.x;
//    var my = mouse.y;
//    console.log("MX: "+mx+" MY: "+my);
//}, true);