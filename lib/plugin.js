var esasky = require('./index');

var base = require('@jupyter-widgets/base');

/**
 * The widget manager provider.
 */
module.exports = {
  id: 'pyesasky',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'pyesasky',
          version: esasky.version,
          exports: esasky
      });
    },
  autoStart: true
};
