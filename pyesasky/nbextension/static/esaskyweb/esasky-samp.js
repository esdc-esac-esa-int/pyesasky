// //////////////////////////////////////////////////////////////////////////
//  File to connect SAMP javascript code with ESASky code 
// //////////////////////////////////////////////////////////////////////////

// //////////////////////////////////////////////////////////////////////////
// AUXILIARY METHODS AND JAVASCRIPT OBJECTS
// //////////////////////////////////////////////////////////////////////////

// Why do we put javascript code in GWT?
// Because we want to include GWT listeners between the lines of code.
// Why do we have this methods below which are used in GWT code?
// Because if we initialize these objects in the GWT code, later on the "instanceof Object" 
// calls in the samp.js methods return false (something to do with initializing javascript in GWT???) 

var baseUrl = window.location.href.toString().replace(new RegExp("[^/]*$"), "").replace("https", "http").replace("8443", "8080");

var sampClientDetails = function() {
	this.id;
	this.name;
	this.metadata = new Object();
	this.subscriptions = new Object();
};

var sampVoTableParams = function(tableId, voTableUrl, tableName) {
	this["table-id"] = tableId;
	this["url"] = voTableUrl;
	this["name"] = tableName;
};

var sampFitsImageParams = function(fitsImageId, fitsImageUrl, fitsImageName) {
	this["image-id"] = fitsImageId;
	this["url"] = fitsImageUrl;
	this["name"] = fitsImageName;
};

var sampFitsTableParams = function(fitsTableId, fitsTableUrl, fitsTableName) {
	this["table-id"] = fitsTableId;
	this["url"] = fitsTableUrl;
	this["name"] = fitsTableName;
};

var sampHighlightRowParams = function(tableId, voTableUrl, rowNumber) {
	this["table-id"] = tableId;
	this["url"] = voTableUrl;
	this["row"] = "" + rowNumber;
};

var sampSelectRowListParams = function(tableId, voTableUrl, rowList) {
	this["table-id"] = tableId;
	this["url"] = voTableUrl;
	this["row-list"] = reInitializeArray(rowList);
	// this["row-list"] = new Array("6","4","2");
};

// For some reason, js complex vars (arrays) initialized in gwt fail to work
// well with samp code... so we initialize it again.
var reInitializeArray = function(rowList) {
	var out = new Array();
	for ( var row in rowList) {
		out.push(rowList[row]);
	}
	return out;
}

var sampEsaSkySubscriptions = function() {
	this["samp.app.ping"] = {};
	this["samp.app.status"] = {};
	this["samp.hub.disconnect"] = {};
	this["samp.hub.event.shutdown"] = {};
	this["samp.hub.event.unregister"] = {};
	this["samp.hub.event.register"] = {};
	this["samp.hub.event.metadata"] = {};
	this["samp.hub.event.subscriptions"] = {};
	this["table.load.votable"] = {};	
	// this["table.highlight.row"] = {};
	// this["table.select.rowList"] = {};
};

var sampEsaSkyMetadata = function() {
	this["samp.name"] = "ESASky";
	this["samp.description"] = "ESASky";
	this["samp.icon.url"] = baseUrl + "images/favicon.png";
	this["author.name"] = "Science Archives Team";
	this["author.affiliation"] = "European Space Agency";
};

function isThere(url) {
	var req = new AJ();
	// XMLHttpRequest object
	try {
		req.open("HEAD", url, false);
		req.send(null);
		return req.status == 200 ? true : false;
	} catch (er) {
		return false;
	}
}

function AJ() {
	var obj;
	if (window.XMLHttpRequest) {
		obj = new XMLHttpRequest();
	} else if (window.ActiveXObject) {
		try {
			obj = new ActiveXObject('MSXML2.XMLHTTP.3.0');
		} catch (er) {
			try {
				obj = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (er) {
				obj = false;
			}
		}
	}
	return obj;
}

function printObject(o) {
	var out = '';
	for ( var p in o) {
		out += p + ': ' + o[p] + '\n';
	}
	alert(out);
}

var hub_status = function() {
	this.active = false;
};

var isHubActive = function(isActive) {
	hub_status.active = isActive;
};


// //////////////////////////////////////////////////////////////////////////
// END OF SAMP FUNCTIONS
// //////////////////////////////////////////////////////////////////////////
