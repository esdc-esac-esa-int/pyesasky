//  import IJupyterWidgetRegistry from "@jupyter-widgets/base";
/**
 * Initialization data for the pyesasky extension.
 */
export * from './pyesasky';
const extension = {
    id: 'pyesasky:plugin',
    autoStart: true,
    activate: (app, widgets) => {
        console.log('JupyterLab extension pyesasky is activated!');
    },
};
export default extension;
export const version = require('../package.json').version;
