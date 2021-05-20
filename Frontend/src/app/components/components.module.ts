import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Ng2SearchPipeModule } from "ng2-search-filter";

import { NavbarComponent } from './navbar/navbar.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { ChartsModule } from "@rinminase/ng-charts";

@NgModule({
  imports: [CommonModule, RouterModule, Ng2SearchPipeModule, ChartsModule],
  declarations: [NavbarComponent, SidebarComponent],
  exports: [NavbarComponent, SidebarComponent],
})
export class ComponentsModule {}
