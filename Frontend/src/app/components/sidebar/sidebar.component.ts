import { Component, OnInit } from '@angular/core';

declare const $: any;
declare interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}
export const ROUTES: RouteInfo[] = [
  { path: '/table-list', title: 'List of Candidates',  icon:'content_paste', class: '' },
  { path: '/user-profile', title: 'New Profile',  icon:'person', class: '' },
  // { path: '/user-profile/id', title: 'New Profile',  icon:'person', class: '' },
  //{ path: '/dashboard', title: 'Dashboard',  icon: 'dashboard', class: '' },    
  // { path: '/typography', title: 'Upload Resume',  icon:'library_books', class: '' },
  //{ path: '/icons', title: 'Icons',  icon:'bubble_chart', class: '' },
  // { path: '/notifications', title: 'Notifications',  icon:'notifications', class: '' },
    ];




@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  menuItems: any[];

  constructor() { }

  ngOnInit() {
    this.menuItems = ROUTES.filter(menuItem => menuItem);
  }
  isMobileMenu() {
      if ($(window).width() > 991) {
          return false;
      }
      return true;
  };
}
