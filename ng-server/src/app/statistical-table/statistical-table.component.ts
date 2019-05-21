import {Component, OnInit} from '@angular/core';
import {PpService, PrivacyPolicy} from "../../pp.service";

@Component({
  selector: 'app-statistical-table',
  templateUrl: './statistical-table.component.html',
  styleUrls: ['./statistical-table.component.css']
})
export class StatisticalTableComponent implements OnInit {

  constructor(private privacyPolicyService: PpService) {
  }


  ngOnInit() {
  }

}
