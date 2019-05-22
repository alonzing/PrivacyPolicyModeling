import {Component, OnInit} from '@angular/core';
import {FormControl} from '@angular/forms';
import {ParagraphRow, PpService, PrivacyPolicy} from "../../pp.service";

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
        this.removeDuplicates();
        this.privacyPolicyService.progressBar = false;
      });
  }

  removeDuplicates(){
    let currentParagraphIndex = -1;
    let modifiedParagraphs: ParagraphRow[] = [];

    for (let paragraphRow of this.privacyPolicyService.privacyPolicyData.paragraphs){
      if(paragraphRow.index > currentParagraphIndex){
        modifiedParagraphs.push(paragraphRow);
        currentParagraphIndex++;
      }
    }
    this.privacyPolicyService.privacyPolicyData.paragraphs = modifiedParagraphs;
  }

  ngOnInit() {
  }


}
