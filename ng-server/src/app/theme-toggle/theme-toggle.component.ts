import {Component, OnInit} from '@angular/core';
import {ThemeService} from "../../theme.service";

@Component({
  selector: 'app-theme-toggle',
  templateUrl: './theme-toggle.component.html',
  styleUrls: ['./theme-toggle.component.css']
})
export class ThemeToggleComponent implements OnInit {

  constructor(public themeService: ThemeService) {
  }

  ngOnInit() {
  }

}
