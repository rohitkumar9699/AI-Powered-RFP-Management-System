import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './components/dashboard.component';
import { VendorsComponent } from './components/vendors.component';
import { RFpsComponent } from './components/rfps.component';
import { ProposalsComponent } from './components/proposals.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, DashboardComponent, VendorsComponent, RFpsComponent, ProposalsComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'RFP Management System';
  activeMenu = 'dashboard';

  ngOnInit() {}

  setActiveMenu(menu: string) {
    this.activeMenu = menu;
  }
}
