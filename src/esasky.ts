import { DOMWidgetModel, DOMWidgetView } from '@jupyter-widgets/base';

export class IFrameModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: 'IFrameModel',
      _view_name: 'IFrameView',
      _model_module: 'pyesasky',
      _view_module: 'pyesasky',
      view_module_ids: []
    };
  }
}

export class IFrameView extends DOMWidgetView {
  modelId: string = '';
  prevMsgId: string = '';
  prevMsgIdToFront: string = '';

  baseUrl: string = 'https://sky.esa.int';
  hideWelcome: boolean = true;
  hideSciSwitch: boolean = true;
  sci: boolean = true;
  hideBannerInfo: boolean = true;

  render(): void {
    this.modelId = 'esaskyFrame' + Math.random().toString(36).substring(2, 10);
    const params = new URLSearchParams({
      hide_welcome: this.hideWelcome.toString(),
      hide_sci_switch: this.hideSciSwitch.toString(),
      sci: this.sci.toString(),
      hide_banner_info: this.hideBannerInfo.toString()
    });

    const iframeSrc = `${this.baseUrl}?${params.toString()}`;

    this.model.set('_view_module_ids', [
      ...this.model.get('_view_module_ids'),
      this.modelId
    ]);

    const div = document.createElement('div');
    const iframe = document.createElement('iframe');
    iframe.setAttribute('id', this.modelId.toString());
    iframe.setAttribute('width', '100%');
    iframe.setAttribute('height', '800px');
    iframe.setAttribute('style', 'border: none');
    iframe.setAttribute('src', iframeSrc);
    iframe.onload = () => {
      if (iframe.contentWindow) {
        iframe.contentWindow.postMessage(
          { event: 'initTest', origin: 'pyesasky' },
          this.baseUrl
        );
        console.log('Init message sent');
      }
    };

    div.appendChild(iframe);
    this.el.appendChild(div);

    const observer = new MutationObserver(() => {
      this.el.style.height = 'auto';
    });
    observer.observe(this.el, { attributes: true, childList: true });

    this.model.on('msg:custom', this.handle_custom_message, this);
    this.listenTo(this.model, 'change:view_height', this.height_changed);

    window.addEventListener('message', e => {
      const data = e.data;
      console.log('Recieved message from iFrame');
      console.log('Sending message to backend');
      if (this.prevMsgId !== data.msgId) {
        this.prevMsgId = data.msgId;
        this.model.send(data);
      }
    });
  }

  height_changed(): void {
    console.log('Changing view height');
    const height = this.model.get('view_height');
    const modelIds = this.model.get('_view_module_ids');

    for (const currActiveId of modelIds.reverse()) {
      const el = document.getElementById(currActiveId);
      if (el) {
        el.style.height = height;
        break;
      }
    }
  }

  handle_custom_message(msg: any): void {
    const modelIds = this.model.get('_view_module_ids');

    const currActiveId = modelIds.find(
      (id: string) => document.getElementById(id) !== null
    );

    if (!currActiveId || this.prevMsgIdToFront === msg.msgId) {
      return;
    }

    if (this.modelId === currActiveId) {
      console.log('Sending message to iFrame');
      const iFrameElement = document.getElementById(
        this.modelId
      ) as HTMLIFrameElement;
      if (iFrameElement?.contentWindow) {
        this.prevMsgIdToFront = msg.msgId;
        iFrameElement.contentWindow.postMessage(msg, this.baseUrl);
      }
    }
  }
}
