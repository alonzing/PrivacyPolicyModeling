import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { AppComponent } from './app.component';
import { PpUrlSearchComponent } from './pp-url-search/pp-url-search.component';
import { StatisticalTableComponent } from './statistical-table/statistical-table.component';
import {HttpClientModule} from "@angular/common/http";
import { SpinnerComponent } from './spinner/spinner.component';


@NgModule({
  declarations: [
    AppComponent,
    PpUrlSearchComponent,
    StatisticalTableComponent,
    SpinnerComponent,
  ],
  imports: [
    BrowserModule, FormsModule, HttpClientModule, ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
