var widgets = require('@jupyter-widgets/base');
var _ = require('underscore');

var ESASkyJSModel = widgets.DOMWidgetModel.extend({
	defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
		_model_name: 'ESASkyJSModel',
		_view_name: 'ESASkyJSView',
		_model_module: 'pyesasky',
		_view_module: 'pyesasky',
		_targetname: '',
		_fovDeg: 30,
		_colorPalette: 'NATIVE',
	})
});

var ESASkyJSView = widgets.DOMWidgetView.extend({

	initialize: function () {
	},


	render: function () {
		var div = document.createElement("div");
		this.base_url = require('@jupyterlab/coreutils').PageConfig.getBaseUrl();
		this.base_url = require('@jupyterlab/coreutils').PageConfig.getBaseUrl();

		//div.innerHTML = "<iframe id='esaskyFrame' width='100%' height='800' style='border: none;' src='" + this.base_url + "nbextensions/pyesasky/esasky.html?log_level=DEBUG&hide_welcome=true&hide_sci_switch=true'</iframe>";
		div.innerHTML = "<iframe id='esaskyFrame' width='100%' height='800' style='border: none;' src='" + this.base_url + "nbextensions/pyesasky/esasky.html?hide_welcome=true&hide_sci_switch=true'</iframe>";
		//div.innerHTML = "<iframe id='esaskyFrame' width='100%' height='800' style='border: none;' src='http://localhost:8080/esasky-web/?log_level=DEBUG&hide_welcome=true&hide_sci_switch=true'</iframe>";
		this.el.appendChild(div);

		this.model.on('msg:custom', this.handle_custom_message, this);

		var _this = this;
		window.addEventListener("message",function(e){
			_this.model.set('_callback',JSON.parse(JSON.parse(e.data)));
			_this.model.set('_messageSync',"Reponse received in object \"_callback\" ");
			console.log(_this)
			_this.model.save_changes();	
		});

	},	
	handle_custom_message: function (msg) {
		console.log('Inside pyesasky.js');
		document.getElementById('esaskyFrame').contentWindow.postMessage(msg)
	}

});

module.exports = {
	ESASkyJSModel: ESASkyJSModel,
	ESASkyJSView: ESASkyJSView
};
