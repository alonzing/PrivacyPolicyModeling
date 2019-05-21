import {Component, OnInit} from '@angular/core';
import {FormControl} from '@angular/forms';
import {PpService, PrivacyPolicy} from "../../pp.service";

@Component({
  selector: 'app-pp-url-search',
  templateUrl: './pp-url-search.component.html',
  styleUrls: ['./pp-url-search.component.css']
})
export class PpUrlSearchComponent implements OnInit {
  urlFormControl = new FormControl('');

  constructor(private privacyPolicyService: PpService) {
  }

  getPrivacyPolicyData() {
    this.privacyPolicyService.progressBar = true;
    console.log("Submitted " + this.urlFormControl.value);
    this.privacyPolicyService.getPrivacyPolicy(this.urlFormControl.value).subscribe(
      (privacyPolicyData: PrivacyPolicy) => {
        this.privacyPolicyService.privacyPolicyData = privacyPolicyData;
        this.privacyPolicyService.progressBar = false;
      });
  }

  ngOnInit() {
  }


}
