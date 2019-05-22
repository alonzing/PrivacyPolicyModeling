import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { AppComponent } from './app.component';
import { PpUrlSearchComponent } from './pp-url-search/pp-url-search.component';
import { StatisticalTableComponent } from './statistical-table/statistical-table.component';
import {HttpClientModule} from "@angular/common/http";
import { ScoreComponent } from './score/score.component';
import { ParagraphsTableComponent } from './paragraphs-table/paragraphs-table.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { TestComponent } from './test/test.component';
import {MatProgressBarModule} from "@angular/material/progress-bar";
import {MatButtonModule} from "@angular/material";


@NgModule({
  declarations: [
    AppComponent,
    PpUrlSearchComponent,
    StatisticalTableComponent,
    ScoreComponent,
    ParagraphsTableComponent,
    TestComponent,
  ],
  imports: [
    BrowserModule, FormsModule, HttpClientModule, ReactiveFormsModule, BrowserAnimationsModule, MatProgressBarModule, MatButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
