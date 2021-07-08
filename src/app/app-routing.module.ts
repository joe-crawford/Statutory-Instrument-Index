import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PrimaryActsComponent } from './primary-acts/primary-acts.component';
import { StatutoryInstrumentsComponent } from './statutory-instruments/statutory-instruments.component';

const routes: Routes = [
  {path: "", component: PrimaryActsComponent },
  {path: "ukpga/:year/:number", component: StatutoryInstrumentsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
