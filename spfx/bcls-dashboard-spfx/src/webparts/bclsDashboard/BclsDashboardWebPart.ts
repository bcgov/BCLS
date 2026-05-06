import { Version } from '@microsoft/sp-core-library';
import {
  IPropertyPaneConfiguration,
  PropertyPaneTextField
} from '@microsoft/sp-property-pane';
import { BaseClientSideWebPart } from '@microsoft/sp-webpart-base';

import * as strings from 'BclsDashboardWebPartStrings';

export interface IBclsDashboardWebPartProps {
  dashboardRelativeUrl: string;
  frameHeight: string;
}

export default class BclsDashboardWebPart extends BaseClientSideWebPart<IBclsDashboardWebPartProps> {

  public render(): void {
    const defaultRel = 'SiteAssets/BCLS-Dashboard/dashboards/bc_dashboard_hub/html/dashboard.html';
    const configuredRel = (this.properties.dashboardRelativeUrl || defaultRel).trim();
    const cleanRel = configuredRel.replace(/^\/+/, '');

    const siteRel = (this.context.pageContext.web.serverRelativeUrl || '').replace(/\/$/, '');
    const iframeSrc = `${siteRel}/${cleanRel}`;

    const parsedHeight = parseInt(this.properties.frameHeight || '3800', 10);
    const frameHeight = Number.isFinite(parsedHeight) && parsedHeight > 600 ? parsedHeight : 3800;

    this.domElement.innerHTML = `
      <div style="width:100%;min-height:${frameHeight}px;background:#eef2f7;border:1px solid #d1d5db;border-radius:8px;overflow:hidden;">
        <iframe
          title="BCLS Dashboard"
          src="${this._escapeAttribute(iframeSrc)}"
          style="width:100%;height:${frameHeight}px;border:0;display:block;background:#ffffff;"
          loading="eager"
          referrerpolicy="no-referrer"
        ></iframe>
      </div>
    `;
  }

  private _escapeAttribute(value: string): string {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  protected onDispose(): void {
    this.domElement.innerHTML = '';
  }

  protected get dataVersion(): Version {
    return Version.parse('1.0');
  }

  protected getPropertyPaneConfiguration(): IPropertyPaneConfiguration {
    return {
      pages: [
        {
          header: {
            description: strings.PropertyPaneDescription
          },
          groups: [
            {
              groupName: strings.BasicGroupName,
              groupFields: [
                PropertyPaneTextField('dashboardRelativeUrl', {
                  label: strings.DashboardRelativeUrlLabel
                }),
                PropertyPaneTextField('frameHeight', {
                  label: strings.FrameHeightLabel
                })
              ]
            }
          ]
        }
      ]
    };
  }
}
