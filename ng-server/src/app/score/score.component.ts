import {Component, OnInit} from '@angular/core';
import {PpService, PrivacyPolicy} from "../../pp.service";
import {Observable} from "rxjs";

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
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicyObservable: Observable<PrivacyPolicy>) => {
      privacyPolicyObservable.subscribe((privacyPolicy: PrivacyPolicy) => {
        this.score = privacyPolicy.score;
        this.getClass();
        this.isReady = true;
      })
    });
  }

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
