import {Component, OnInit} from '@angular/core';
import {PpService, PrivacyPolicy, TableRow} from "../../pp.service";
import {ThemeService} from "../../theme.service";

/**
 * Represents a statistical table with 'Parameter', 'Value', and 'Category Value' columns.
 */
@Component({
  selector: 'app-statistical-table',
  templateUrl: './statistical-table.component.html',
  styleUrls: ['./statistical-table.component.css']
})

export class StatisticalTableComponent implements OnInit {
  displayedColumns: string[] = ['parameter', 'value', 'categoryValue'];
  dataSource: TableRow[];
  isReady: boolean = false;

  constructor(public privacyPolicyService: PpService, public themeService: ThemeService) {
  }

  ngOnInit() {
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicy: PrivacyPolicy) => {
      this.dataSource = privacyPolicy.table;
      this.isReady = true;
    });
  }
}
