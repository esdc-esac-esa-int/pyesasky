let esasky = require('./index');

let base = require('@jupyter-widgets/base');

/**
 * The widget manager provider.
 */
module.exports = {
  id: 'pyesasky',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app:any, widgets:any) {
      widgets.registerWidget({
          name: 'pyesasky',
          version: esasky.version,
          exports: esasky
      });
    },
  autoStart: true
};
