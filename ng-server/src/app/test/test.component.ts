import {Component, NgModule, OnInit} from '@angular/core';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})

@NgModule({
  imports: [MatProgressBarModule, BrowserAnimationsModule]
})

export class TestComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
