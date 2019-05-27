import {Component, NgModule, OnInit} from '@angular/core';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

@Component({
  selector: 'app-test',
  templateUrl: './progress-bar.component.html',
  styleUrls: ['./progress-bar.component.css']
})

@NgModule({
  imports: [MatProgressBarModule, BrowserAnimationsModule]
})

export class ProgressBarComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
