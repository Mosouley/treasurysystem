import { MaterialModule } from './../../material/material.module';
import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Output, EventEmitter } from '@angular/core';
import { AnalyticsComponent } from '../../report/analytics/analytics.component';
import { PnlCcyComponent } from '../../report/pnl-ccy/pnl-ccy.component';
import { PnlSummaryComponent } from '../../report/pnl-summary/pnl-summary.component';
import { PositionCcyComponent } from '../../report/position-ccy/position-ccy.component';
import { RisksMetricsComponent } from '../../report/risks-metrics/risks-metrics.component';
import { BannerService } from '../../shared/services/banner.service';
import { RouterModule } from '@angular/router';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { SideNavClosedComponent } from '../side-nav-closed/side-nav-closed.component';
import { NavbarComponent } from '../navbar/navbar.component';
import { BannerComponent } from './banner.component';
import { SettingsComponent } from '../../treasuryapp/config/settings/settings.component';
import { SettingsPanelComponent } from '../settings-panel/settings-panel.component';


@Component({
  selector: 'app-dash',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    SidebarComponent,
    SideNavClosedComponent,
    NavbarComponent,
    BannerComponent,
    SettingsPanelComponent,
    MaterialModule

  ],
  templateUrl: './dash.component.html',
  styleUrls: ['./dash.component.css'],

})
export class DashComponent implements OnInit {


  numCards = Array.from(Array(10).keys());

  isSidebarOpen = true;

  isSettingsPanelOpen = false;
  // isSearchBoxOpen = false;
  isSidebarReduced = false;

  @Output () toggleSideNav: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(private bannerService: BannerService) {
   }
  ngOnInit(){}

  toggleBanner() {
    this.bannerService.toggleBanner();
  }

  toggleSidebarMenu($event: any) {
    this.isSidebarOpen = $event;
  }

  toggleSidebarReduce($event: any) {
    this.isSidebarReduced = $event;
  }
  toggleSettingsMenu($event: any) {
    this.isSettingsPanelOpen = $event;
  }
  callPnLSummary() {
    this.bannerService.setDynamicComponent(PnlSummaryComponent);
  }
  callPositionCcy() {
    this.bannerService.setDynamicComponent(PositionCcyComponent);
  }
  callPnLCcy() {
    this.bannerService.setDynamicComponent(PnlCcyComponent);
  }
  callRisksMetrics() {
    this.bannerService.setDynamicComponent(RisksMetricsComponent);
  }
  callAnalytics() {
    this.bannerService.setDynamicComponent(AnalyticsComponent);
  }

  sidebarWidthClass(): string {
    if (this.isSidebarOpen) {
      return 'transform transition-all duration-200 w-60 ease-out';
    } else {
      return '-translate-x-full transition-all duration-300 ease-out w-0';
    }
  }

  sidebarIconClass(): string {
    return this.isSidebarReduced ? 'w-12 transform place-items-center justify-center transition-all duration-300 ease-in bg-sellar-primary' : 'transform ease-out duration-300';
  }

  sidebarTransitionClass(): string {
    if (this.isSidebarOpen && this.isSidebarReduced) {
      return 'transform transition-all duration-300 sm:w-12 ease-in';
    } else {
      return 'transform-none';
    }
  }

}
