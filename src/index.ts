import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IFrameModel, IFrameView } from './esasky';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';
import pkg from '../package.json';

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'pyesasky:plugin',
  requires: [IJupyterWidgetRegistry],
  description: 'ESASky Python wrapper',
  autoStart: true,
  activate: (app: JupyterFrontEnd, registry: IJupyterWidgetRegistry) => {
    console.log('JupyterLab extension pyesasky is activated!');
    registry.registerWidget({
      name: 'pyesasky',
      version: pkg.version,
      exports: { IFrameModel, IFrameView }
    });
  }
};

export default plugin;
