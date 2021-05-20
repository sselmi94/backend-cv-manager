import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app.routing';
import { ComponentsModule } from './components/components.module';
import { AppComponent } from './app.component';

//import { DashboardComponent } from './dashboard/dashboard.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { TableListComponent } from './table-list/table-list.component';
import { Ng2SearchPipeModule } from 'ng2-search-filter';
import { AngularFileUploaderModule } from "angular-file-uploader";
import {Ng2OrderModule} from 'ng2-order-pipe';
import {NgxPaginationModule} from 'ngx-pagination';
import { TableFilterPipe } from './table-list/table-filter.pipe';
import { ReactiveFormsModule } from '@angular/forms';
import {BrowserModule} from '@angular/platform-browser';
import { SimpleNotificationsModule } from 'angular2-notifications';
import { ChartsModule } from "@rinminase/ng-charts";




import {
  AgmCoreModule
} from '@agm/core';
import { AdminLayoutComponent } from './layouts/admin-layout/admin-layout.component';


@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    AngularFileUploaderModule,
    ReactiveFormsModule,
    HttpClientModule,
    ComponentsModule,
    RouterModule,
    AppRoutingModule,
    Ng2SearchPipeModule,
    Ng2OrderModule,ChartsModule,
    NgxPaginationModule,
    SimpleNotificationsModule.forRoot(),
    AgmCoreModule.forRoot({
      apiKey: "YOUR_GOOGLE_MAPS_API_KEY",
    }),
  ],
  declarations: [
    AppComponent,
    AdminLayoutComponent,
    TableListComponent,
    TableFilterPipe,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
