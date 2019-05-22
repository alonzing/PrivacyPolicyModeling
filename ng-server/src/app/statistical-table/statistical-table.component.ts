import {Component, OnInit} from '@angular/core';
import {PpService} from "../../pp.service";

@Component({
  selector: 'app-statistical-table',
  templateUrl: './statistical-table.component.html',
  styleUrls: ['./statistical-table.component.css']
})
export class StatisticalTableComponent implements OnInit {

  constructor(public privacyPolicyService: PpService) {
  }


  ngOnInit() {
  }

}
