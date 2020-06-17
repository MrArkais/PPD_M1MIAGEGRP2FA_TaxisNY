// Basic Angular
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { CommonModule } from '@angular/common';

//Component
import { IndexComponent } from './index/index.component';
import { AppComponent } from './app.component';
import { VoyageurComponent } from './voyageur/voyageur.component';
import { DatascientistComponent } from './datascientist/datascientist.component';
import { FourohfourComponent } from './fourohfour/fourohfour.component';
import { AboutComponent } from './about/about.component';
import { TeamComponent } from './team/team.component';
import { VoyageurChartComponent } from './pieChart/voyageurChart.component';
import { ScientistChartComponent } from './pieChart/scientistChart.component';

// Services
import { VoyageurService } from './services/voyageur.service';

// Imports
import { MaterialModule } from './MaterialModule';
import { Ng5SliderModule } from 'ng5-slider';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DataScientistService } from './services/datascientist.service';




const appRoutes: Routes = [
  { path: '', component: IndexComponent },
  { path: 'voyageur', component: VoyageurComponent },
  { path: 'datascientist', component: DatascientistComponent },
  { path: 'not-found', component: FourohfourComponent },
  { path: 'about', component: AboutComponent },
  { path: 'contact', component: TeamComponent },

  { path: '**', redirectTo: 'not-found' },
];

@NgModule({
  declarations: [
    AppComponent,
    IndexComponent,
    VoyageurComponent,
    DatascientistComponent,
    FourohfourComponent,
    AboutComponent,
    TeamComponent,
    VoyageurChartComponent,
    ScientistChartComponent,
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes),
    NoopAnimationsModule,
    MaterialModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    Ng5SliderModule,
    CommonModule,
    FontAwesomeModule
  ],
  providers: [VoyageurService, DataScientistService],
  bootstrap: [AppComponent],
})
export class AppModule {}
