import {Component, OnInit} from '@angular/core';
import {PpService} from "../../pp.service";

@Component({
  selector: 'app-score',
  templateUrl: './score.component.html',
  styleUrls: ['./score.component.css']
})
export class ScoreComponent implements OnInit {

  constructor(private privacyPolicyService: PpService) {
  }

  ngOnInit() {
  }

  getClass() {
    let score = this.privacyPolicyService.privacyPolicyData.score;
    let badgeClass = "badge ";
    if (score >= 90) {
      badgeClass += "badge-success";
    } else if (score >= 80) {
      badgeClass += "badge-warning";
    } else {
      badgeClass += "badge-danger";
    }
    return badgeClass;

  }
}
