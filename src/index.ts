import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IFrameModel, IFrameView } from './esasky';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'pyesasky:plugin',
  requires: [IJupyterWidgetRegistry],
  description: 'ESASky Python wrapper',
  autoStart: true,
  activate: (app: JupyterFrontEnd, registry: IJupyterWidgetRegistry) => {
    console.log('JupyterLab extension pyesasky is activated!');
    registry.registerWidget({
      name: 'pyesasky',
      version: '0.1.0',
      exports: { IFrameModel, IFrameView }
    });
  }
};

export default plugin;
