import {Component, OnInit} from '@angular/core';
import {PpService, PrivacyPolicy} from "../../pp.service";

@Component({
  selector: 'app-statistical-table',
  templateUrl: './statistical-table.component.html',
  styleUrls: ['./statistical-table.component.css']
})
export class StatisticalTableComponent implements OnInit {

  privacyPolicyData: PrivacyPolicy;

  constructor(private privacyPolicyService: PpService) {
  }

  getPrivacyPolicyData(): void {
    this.privacyPolicyService.getPrivacyPolicy("")
      .subscribe(privacyPolicyData => this.privacyPolicyData = privacyPolicyData);
  }

  ngOnInit() {
    // this.getPrivacyPolicyData();
  }

}
