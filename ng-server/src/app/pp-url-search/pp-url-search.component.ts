import {Component, NgModule, OnInit} from '@angular/core';
import {FormControl, Validators} from '@angular/forms';
import {ParagraphRow, PpService, PrivacyPolicy} from "../../pp.service";
import {MatButtonModule} from '@angular/material/button';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';

@Component({
  selector: 'app-pp-url-search',
  templateUrl: './pp-url-search.component.html',
  styleUrls: ['./pp-url-search.component.css']
})

@NgModule({
  imports: [MatButtonModule, BrowserAnimationsModule, MatInputModule, MatFormFieldModule]
})

export class PpUrlSearchComponent implements OnInit {

  pPUrl = new FormControl('', [
    Validators.required,
  ]);

  constructor(public privacyPolicyService: PpService) {
  }

  getPrivacyPolicyData() {
    this.privacyPolicyService.progressBar = true;
    console.log("Submitted " + this.pPUrl.value);
    this.privacyPolicyService.getPrivacyPolicy(this.pPUrl.value).subscribe(
      (privacyPolicyData: PrivacyPolicy) => {
        if (privacyPolicyData == null) {
          this.privacyPolicyService.progressBar = false;
          return
        }
        this.privacyPolicyService.privacyPolicyData = privacyPolicyData;
        this.removeDuplicates();
        this.privacyPolicyService.progressBar = false;
      });
  }

  removeDuplicates() {
    let currentParagraphIndex = -1;
    let modifiedParagraphs: ParagraphRow[] = [];

    for (let paragraphRow of this.privacyPolicyService.privacyPolicyData.paragraphs) {
      if (paragraphRow.index > currentParagraphIndex) {
        modifiedParagraphs.push(paragraphRow);
        currentParagraphIndex++;
      }
    }
    this.privacyPolicyService.privacyPolicyData.paragraphs = modifiedParagraphs;
  }

  ngOnInit() {
  }


}
