import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule],
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
