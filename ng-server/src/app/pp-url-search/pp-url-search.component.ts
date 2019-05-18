import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
@Component({
  selector: 'app-pp-url-search',
  templateUrl: './pp-url-search.component.html',
  styleUrls: ['./pp-url-search.component.css']
})
export class PpUrlSearchComponent implements OnInit {
  url = new FormControl('');
  constructor() { }

  ngOnInit() {
  }

}
