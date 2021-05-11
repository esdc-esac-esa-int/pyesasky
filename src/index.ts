import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
//  import IJupyterWidgetRegistry from "@jupyter-widgets/base";
/**
 * Initialization data for the pyesasky extension.
 */
export * from './pyesasky';
const extension: JupyterFrontEndPlugin<void> = {
  id: 'pyesasky:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd, widgets) => {
    console.log('JupyterLab extension pyesasky is activated!');
  },
};

export default extension;
export const version = (require('../package.json') as any).version;