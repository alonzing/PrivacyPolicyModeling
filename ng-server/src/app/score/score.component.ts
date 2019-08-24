import {Component, OnInit} from '@angular/core';
import {PpService, PrivacyPolicy} from "../../pp.service";

/**
 * Represents the score of the privacy policy as a colored badge, where the color corresponds to the score.
 */
@Component({
  selector: 'app-score',
  templateUrl: './score.component.html',
  styleUrls: ['./score.component.css']
})


export class ScoreComponent implements OnInit {
  score: number;
  isReady: boolean = false;

  constructor(public privacyPolicyService: PpService) {
  }

  ngOnInit() {
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicy: PrivacyPolicy) => {
      this.score = privacyPolicy.score;
      this.isReady = true;
    });
  }

  /**
   * Builds the class attribute for this component by picking the badge's color corresponding to the score.
   */
  getClass() {
    let badgeClass = "badge ";
    if (this.score >= 90) {
      badgeClass += "badge-success";
    } else if (this.score >= 80) {
      badgeClass += "badge-warning";
    } else {
      badgeClass += "badge-danger";
    }
    return badgeClass;
  }
}
