import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {AppComponent} from './app.component';
import {PpUrlSearchComponent} from './pp-url-search/pp-url-search.component';
import {StatisticalTableComponent} from './statistical-table/statistical-table.component';
import {HttpClientModule} from "@angular/common/http";
import {ScoreComponent} from './score/score.component';
import {ParagraphsTableComponent} from './paragraphs-table/paragraphs-table.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ProgressBarComponent} from './progress-bar/progress-bar.component';
import {MatProgressBarModule} from "@angular/material/progress-bar";
import {
  MatButtonModule,
  MatChipsModule,
  MatFormFieldModule,
  MatInputModule,
  MatSlideToggleModule,
  MatSelectModule
} from "@angular/material";
import {MatTableModule} from '@angular/material/table';
import {ThemeToggleComponent} from './theme-toggle/theme-toggle.component';
import {CookieService} from 'ngx-cookie-service';

@NgModule({
  declarations: [
    AppComponent,
    PpUrlSearchComponent,
    StatisticalTableComponent,
    ScoreComponent,
    ParagraphsTableComponent,
    ProgressBarComponent,
    ThemeToggleComponent,
  ],
  imports: [
    BrowserModule, FormsModule, HttpClientModule, ReactiveFormsModule, BrowserAnimationsModule, MatProgressBarModule,
    MatButtonModule, MatFormFieldModule, MatInputModule, MatTableModule, MatChipsModule, MatSlideToggleModule, MatSelectModule
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
