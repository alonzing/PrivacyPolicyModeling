import {Component, NgModule, OnInit} from '@angular/core';
import {FormControl, Validators} from '@angular/forms';
import {ParagraphRow, PpService, PrivacyPolicy} from "../../pp.service";
import {MatButtonModule} from '@angular/material/button';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {Observable} from "rxjs";
import {MatTableDataSource} from "@angular/material";

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
    this.privacyPolicyService.privacyPolicyData.asObservable().subscribe((privacyPolicyObservable: Observable<PrivacyPolicy>) => {
      privacyPolicyObservable.subscribe((privacyPolicy: PrivacyPolicy) => {
        this.privacyPolicyService.progressBar = false;
        if (privacyPolicy == null) {
          return
        }
      })
    });
    this.privacyPolicyService.getPrivacyPolicy(this.pPUrl.value);
    console.log("Submitted " + this.pPUrl.value);
  }



  ngOnInit() {
  }


}
