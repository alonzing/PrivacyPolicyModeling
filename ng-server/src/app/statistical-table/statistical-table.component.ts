import {Component, OnInit} from '@angular/core';
import {PpService, PrivacyPolicy, TableRow} from "../../pp.service";
import {Observable} from "rxjs";
import {MatTableDataSource} from "@angular/material";

@Component({
  selector: 'app-statistical-table',
  templateUrl: './statistical-table.component.html',
  styleUrls: ['./statistical-table.component.css']
})
export class StatisticalTableComponent implements OnInit {
  displayedColumns: string[] = ['parameter', 'value', 'categoryValue'];
  dataSource: TableRow[];
  isReady: boolean = false;

  constructor(public privacyPolicyService: PpService) {
  }


  ngOnInit() {
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicyObservable: Observable<PrivacyPolicy>) => {
      privacyPolicyObservable.subscribe((privacyPolicy: PrivacyPolicy) => {
        this.dataSource = privacyPolicy.table;
        this.isReady = true;
      })
    });
  }
}
