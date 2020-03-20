var widgets = require('@jupyter-widgets/base');
var _ = require('underscore');

var ESASkyJSModel = widgets.DOMWidgetModel.extend({
	defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
		_model_name: 'ESASkyJSModel',
		_view_name: 'ESASkyJSView',
		_model_module: 'pyesasky',
		_view_module: 'pyesasky',
        _view_module_ids : []
	})
});

var ESASkyJSView = widgets.DOMWidgetView.extend({

	initialize: function () {
	},


	render: function () {
		var div = document.createElement("div");
		this.base_url = require('@jupyterlab/coreutils').PageConfig.getBaseUrl();
		this.base_url = require('@jupyterlab/coreutils').PageConfig.getBaseUrl();
		this.modelId = "esaskyFrame" + Math.random().toString(36).substr(2,10);
		moduleIds = this.model.get('_view_module_ids')
		moduleIds.push(this.modelId)
		this.model.set('_view_module_ids', moduleIds)
		
		//div.innerHTML = "<iframe id=" + this.modelId + " width='100%' height='800' style='border: none;' src='" + this.base_url + "nbextensions/pyesasky/esasky.html?log_level=DEBUG&hide_welcome=true&hide_sci_switch=true'</iframe>";
		div.innerHTML = "<iframe id=" + this.modelId + " width='100%' height='800' style='border: none;' src='" + this.base_url + "nbextensions/pyesasky/esasky.html?hide_welcome=true&hide_sci_switch=true'</iframe>";
		//div.innerHTML = "<iframe id=" + this.modelId + " width='100%' height='800' style='border: none;' src='http://localhost:8080/esasky-web/?log_level=DEBUG&hide_welcome=true&hide_sci_switch=true'</iframe>";
		this.el.appendChild(div);
		
		this.model.on('msg:custom' , this.handle_custom_message, this);
		this.listenTo(this.model, 'change:view_height', this.height_changed, this);

		this.oldMsgId = null
		this.oldMsgIdToFront = null
		var _this = this;
		
		window.addEventListener("message",function(e){
			var data = e.data;
			console.log("Back inside pyesasky.js");
			if(_this.oldMsgId != data.msgId){
				_this.oldMsgId = data.msgId
				_this.model.send(data,null,null);
			}
		});
		
	},	

	height_changed: function () {
		console.log("Changing view height")
		var height = this.model.get('view_height');
		modelIds = this.model.get('_view_module_ids')
		for (var i = modelIds.length-1; i >= 0; i--) {
			currActiveId = modelIds[i]; 
			if(document.getElementById(currActiveId) != null){
				document.getElementById(currActiveId).height = height;
				break;
			}
		}
	},

	handle_custom_message: function (msg) {
		modelIds = this.model.get('_view_module_ids')
		for (var i = modelIds.length-1; i >= 0; i--) {
			currActiveId = modelIds[i]; 
			if(document.getElementById(currActiveId) != null){
				break;
			}
		}
		if(this.oldMsgIdToFront != msg.msgId){
			if(this.modelId == currActiveId){
				this.oldMsgIdToFront = msg.msgId;
				console.log('Inside pyesasky.js');
				document.getElementById(this.modelId).contentWindow.postMessage(msg, this.base_url)
			}
		}
	}

});

module.exports = {
	ESASkyJSModel: ESASkyJSModel,
	ESASkyJSView: ESASkyJSView
};
