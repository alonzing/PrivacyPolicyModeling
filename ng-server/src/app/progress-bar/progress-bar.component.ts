import {Component, OnInit} from '@angular/core';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ThemeService} from "../../theme.service";

/**
 * Represents a progress bar. It is shown while waiting to a response from the server.
 */
@Component({
  selector: 'app-test',
  templateUrl: './progress-bar.component.html',
  styleUrls: ['./progress-bar.component.css']
})

export class ProgressBarComponent implements OnInit {

  constructor(public themeService: ThemeService) {
  }

  ngOnInit() {
  }

}
